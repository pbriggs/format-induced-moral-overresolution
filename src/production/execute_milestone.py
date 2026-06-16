from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any

from parsing.validate_json import ParsedOutput, parse_and_validate
from parsing.validity_status import ValidityStatus
from production.config import ConfigurationError, load_execution_config, parse_model_ids
from production.failure_policy import circuit_breaker_decision, classify_api_failure
from production.providers import InferenceRequest, ProviderRequestError, build_adapters
from production.reporting import write_api_call_ledger, write_milestone_report
from production.run_milestone import build_parser as build_plan_parser
from production.run_milestone import run as plan_run
from production.shards import append_jsonl, first_incomplete_shard, iter_jsonl, update_shard_state, write_shard_plan
from protocol.exclusion_rules import primary_output_exclusion
from protocol.prompt_modes import PromptMode
from storage.db import connect, migrate
from utils.hashing import stable_hash


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def json_dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def _plan_args(args: argparse.Namespace) -> argparse.Namespace:
    parser = build_plan_parser()
    plan_args = parser.parse_args([])
    plan_args.milestone = args.milestone
    plan_args.run_id = args.run_id
    plan_args.out_dir = args.out_dir
    plan_args.db = args.db
    plan_args.models = args.models
    plan_args.splits = args.splits
    plan_args.seed = args.seed
    plan_args.alpha = args.alpha
    return plan_args


def _executable_requests(pending: list[dict[str, Any]], allow_prework_blocked: bool) -> list[dict[str, Any]]:
    if allow_prework_blocked:
        return pending
    return [request for request in pending if not request.get("prework_required")]


def _load_milestone_pending(out_dir: Path, milestone: str) -> list[dict[str, Any]]:
    path = out_dir / f"pending_api_calls_{milestone}.jsonl"
    pending: list[dict[str, Any]] = []
    if not path.exists():
        return pending
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                pending.append(json.loads(line))
    return pending


def _load_target_call_ids(out_dir: Path, milestone: str) -> set[str] | None:
    path = out_dir / f"target_api_call_ids_{milestone}.jsonl"
    if not path.exists():
        return None
    call_ids: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                call_ids.add(str(json.loads(line)["api_call_id"]))
    return call_ids


def parsed_output_is_invalid_for_primary_summary(status: ValidityStatus) -> bool:
    return not primary_output_exclusion(status).include_primary


def _recent_api_failures(connection: sqlite3.Connection, run_id: str, limit: int = 50) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT http_status_code, api_error_type
        FROM api_calls_raw
        WHERE run_id = ? AND api_error_flag = 1
        ORDER BY timestamp_completed DESC
        LIMIT ?
        """,
        (run_id, limit),
    ).fetchall()
    return [dict(row) for row in rows]


def _insert_attempt(
    connection: sqlite3.Connection,
    request: dict[str, Any],
    *,
    provider: str,
    api_route: str,
    attempt_index: int,
    started: str,
    completed: str,
    raw_response: str | None = None,
    response_headers_json: str | None = None,
    http_status_code: int | None = None,
    api_error_type: str | None = None,
    error_response_body: str | None = None,
    transport_error_message: str | None = None,
    retry_after_seconds: float | None = None,
) -> None:
    attempt_id = stable_hash([request["api_call_id"], attempt_index, completed])
    connection.execute(
        """
        INSERT OR REPLACE INTO api_call_attempts (
          attempt_id, api_call_id, run_id, model_id, provider, api_route,
          prompt_mode, attempt_index, request_json, raw_response, response_headers_json,
          http_status_code, api_error_type, error_response_body, transport_error_message,
          retry_after_seconds, timestamp_started, timestamp_completed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            attempt_id,
            request["api_call_id"],
            request["run_id"],
            request["model_id"],
            provider,
            api_route,
            request["prompt_mode"],
            attempt_index,
            json_dumps(request),
            raw_response,
            response_headers_json,
            http_status_code,
            api_error_type,
            error_response_body,
            transport_error_message,
            retry_after_seconds,
            started,
            completed,
        ),
    )


def _insert_success(
    connection: sqlite3.Connection,
    request: dict[str, Any],
    *,
    provider: str,
    api_route: str,
    envelope: Any,
    started: str,
    completed: str,
    retry_count: int,
) -> None:
    connection.execute(
        """
        INSERT OR REPLACE INTO api_calls_raw (
          api_call_id, run_id, milestone, call_type, is_pilot, is_confirmatory,
          item_id, dataset_id, model_id, provider, api_route,
          prompt_mode, prompt_hash, prompt_paraphrase_id, label_order, sample_id,
          temperature_or_null, structured_output_mode, request_json, raw_response,
          provider_response_id, finish_reason_or_null, timestamp_started,
          timestamp_completed, api_error_flag, http_status_code, response_headers_json,
          retry_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
        """,
        (
            request["api_call_id"],
            request["run_id"],
            request.get("target_milestone") or request.get("introduced_milestone"),
            request.get("call_type") or request.get("component_type"),
            1 if request.get("is_pilot") else 0,
            1 if request.get("is_confirmatory") else 0,
            request["item_id"],
            request["dataset_id"],
            request["model_id"],
            provider,
            api_route,
            request["prompt_mode"],
            request["prompt_hash"],
            request.get("prompt_paraphrase_id"),
            json_dumps(request.get("label_order")),
            request.get("sample_id"),
            0.0,
            request.get("response_schema"),
            json_dumps(envelope.request_payload),
            envelope.raw_text,
            envelope.response_payload.get("id") if isinstance(envelope.response_payload, dict) else None,
            envelope.finish_reason,
            started,
            completed,
            envelope.status_code,
            json_dumps(envelope.response_headers),
            retry_count,
        ),
    )


def _insert_error(
    connection: sqlite3.Connection,
    request: dict[str, Any],
    *,
    provider: str,
    api_route: str,
    error: ProviderRequestError,
    started: str,
    completed: str,
    retry_count: int,
) -> str:
    failure = classify_api_failure(
        http_status_code=error.status_code,
        error_type="transport_error" if error.transport_error_message else None,
        retry_after_seconds=error.retry_after_seconds,
    )
    connection.execute(
        """
        INSERT OR REPLACE INTO api_calls_raw (
          api_call_id, run_id, milestone, call_type, is_pilot, is_confirmatory,
          item_id, dataset_id, model_id, provider, api_route,
          prompt_mode, prompt_hash, prompt_paraphrase_id, label_order, sample_id,
          request_json, api_error_flag, api_error_type, http_status_code,
          response_headers_json, error_response_body, transport_error_message,
          retry_after_seconds, terminal_failure_flag, retry_count, timestamp_started,
          timestamp_completed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request["api_call_id"],
            request["run_id"],
            request.get("target_milestone") or request.get("introduced_milestone"),
            request.get("call_type") or request.get("component_type"),
            1 if request.get("is_pilot") else 0,
            1 if request.get("is_confirmatory") else 0,
            request["item_id"],
            request["dataset_id"],
            request["model_id"],
            provider,
            api_route,
            request["prompt_mode"],
            request["prompt_hash"],
            request.get("prompt_paraphrase_id"),
            json_dumps(request.get("label_order")),
            request.get("sample_id"),
            json_dumps(request),
            failure.kind.value,
            error.status_code,
            json_dumps(error.response_headers),
            error.error_response_body,
            error.transport_error_message,
            error.retry_after_seconds,
            1 if failure.terminal else 0,
            retry_count,
            started,
            completed,
        ),
    )
    return failure.kind.value


def _insert_parsed_output(connection: sqlite3.Connection, request: dict[str, Any], parsed: ParsedOutput) -> None:
    parsed_json = parsed.parsed_json or {}
    probs = parsed_json.get("label_probabilities", {}) if isinstance(parsed_json, dict) else {}
    connection.execute(
        """
        INSERT OR REPLACE INTO parsed_outputs (
          api_call_id, run_id, item_id, dataset_id, model_id, prompt_mode,
          validity_status, repair_attempted, repair_successful, refusal_flag,
          malformed_flag, off_schema_label_flag, probability_sum, chosen_label,
          estimated_source_community_agreement, moral_certainty, p_author,
          p_other, p_everybody, p_nobody, p_info, most_likely_label,
          recognition_status, recognition_confidence, parsed_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request["api_call_id"],
            request["run_id"],
            request["item_id"],
            request["dataset_id"],
            request["model_id"],
            request["prompt_mode"],
            parsed.status.value,
            1 if parsed.status in {ValidityStatus.INVALID_JSON, ValidityStatus.EMPTY_RESPONSE} else 0,
            1 if parsed.status == ValidityStatus.OFF_SCHEMA_LABEL else 0,
            parsed.probability_sum,
            parsed_json.get("chosen_label"),
            parsed_json.get("estimated_source_community_agreement"),
            parsed_json.get("moral_certainty"),
            probs.get("author"),
            probs.get("other"),
            probs.get("everybody"),
            probs.get("nobody"),
            probs.get("info"),
            parsed_json.get("most_likely_label"),
            parsed_json.get("recognition_status"),
            parsed_json.get("confidence"),
            json_dumps(parsed_json) if parsed.parsed_json is not None else None,
        ),
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    plan_summary = plan_run(_plan_args(args))
    model_ids = parse_model_ids(args.models)
    execution_config = load_execution_config(model_ids, mock_provider=args.mock_provider)
    adapters = build_adapters(execution_config.providers)

    out_dir = Path(args.out_dir) / args.run_id
    db_path = Path(args.db) if args.db else out_dir / "study.sqlite"
    connection = connect(db_path)
    migrate(connection)
    pending = _load_milestone_pending(out_dir, args.milestone)
    target_api_call_ids = _load_target_call_ids(out_dir, args.milestone)
    executable = _executable_requests(pending, args.allow_prework_blocked)
    if args.max_calls is not None:
        executable = executable[: args.max_calls]

    shard_dir = out_dir / "execution_shards" / args.milestone
    shard_paths = write_shard_plan(shard_dir, executable, args.shard_count)
    shard_path = first_incomplete_shard(shard_paths)
    completed = 0
    failed = 0
    invalid = 0
    skipped = 0
    abort_reason = ""
    recent_failures: deque[dict[str, Any]] = deque(_recent_api_failures(connection, args.run_id), maxlen=50)

    if shard_path is None:
        connection.close()
        return {"status": "already_complete", "milestone": args.milestone, "plan_summary": plan_summary}

    update_shard_state(shard_path, status="running", started_at=utc_now())
    attempts_path = shard_path.with_suffix(".attempts.jsonl")
    events_path = shard_path.with_suffix(".events.jsonl")
    for request_record in iter_jsonl(shard_path):
        request = dict(request_record)
        already_done = connection.execute(
            """
            SELECT 1 FROM api_calls_raw
            WHERE api_call_id = ? AND ((api_error_flag = 0 AND raw_response IS NOT NULL) OR terminal_failure_flag = 1)
            """,
            (request["api_call_id"],),
        ).fetchone()
        if already_done:
            skipped += 1
            continue

        breaker = circuit_breaker_decision(
            recent_failures,
            execution_config.max_recent_retryable_errors,
            execution_config.max_recent_server_errors,
            execution_config.max_recent_rate_limits,
        )
        if breaker.abort:
            abort_reason = breaker.reason
            append_jsonl(events_path, {"event": "circuit_breaker_abort", "reason": abort_reason, "at": utc_now()})
            break

        provider = execution_config.model_to_provider[str(request["model_id"])]
        adapter = adapters[provider]
        inference_request = InferenceRequest(
            prompt=str(request["prompt"]),
            model_id=str(request["model_id"]),
            prompt_mode=str(request["prompt_mode"]),
            response_schema=str(request.get("response_schema") or request["prompt_mode"]),
        )
        started = utc_now()
        try:
            envelope = adapter.run_single_turn(inference_request)
        except ProviderRequestError as exc:
            completed_at = utc_now()
            error_type = _insert_error(
                connection,
                request,
                provider=provider,
                api_route=adapter.endpoint,
                error=exc,
                started=started,
                completed=completed_at,
                retry_count=max(0, execution_config.max_attempts_per_call - 1),
            )
            _insert_attempt(
                connection,
                request,
                provider=provider,
                api_route=adapter.endpoint,
                attempt_index=1,
                started=started,
                completed=completed_at,
                http_status_code=exc.status_code,
                response_headers_json=json_dumps(exc.response_headers),
                api_error_type=error_type,
                error_response_body=exc.error_response_body,
                transport_error_message=exc.transport_error_message,
                retry_after_seconds=exc.retry_after_seconds,
            )
            append_jsonl(
                attempts_path,
                {
                    "api_call_id": request["api_call_id"],
                    "status": "error",
                    "api_error_type": error_type,
                    "http_status_code": exc.status_code,
                    "error_response_body": exc.error_response_body,
                    "transport_error_message": exc.transport_error_message,
                    "retry_after_seconds": exc.retry_after_seconds,
                    "timestamp_started": started,
                    "timestamp_completed": completed_at,
                },
            )
            connection.commit()
            failed += 1
            recent_failures.append({"http_status_code": exc.status_code, "api_error_type": error_type})
            continue

        completed_at = utc_now()
        _insert_success(
            connection,
            request,
            provider=provider,
            api_route=envelope.endpoint,
            envelope=envelope,
            started=started,
            completed=completed_at,
            retry_count=0,
        )
        _insert_attempt(
            connection,
            request,
            provider=provider,
            api_route=envelope.endpoint,
            attempt_index=1,
            started=started,
            completed=completed_at,
            raw_response=envelope.raw_text,
            response_headers_json=json_dumps(envelope.response_headers),
            http_status_code=envelope.status_code,
        )
        parsed = parse_and_validate(envelope.raw_text, PromptMode(str(request["prompt_mode"])))
        _insert_parsed_output(connection, request, parsed)
        if parsed_output_is_invalid_for_primary_summary(parsed.status):
            invalid += 1
            append_jsonl(events_path, {"event": "unexpected_response_schema", "api_call_id": request["api_call_id"], "status": parsed.status.value, "at": utc_now()})
        append_jsonl(
            attempts_path,
            {
                "api_call_id": request["api_call_id"],
                "status": "success",
                "http_status_code": envelope.status_code,
                "raw_response": envelope.raw_text,
                "timestamp_started": started,
                "timestamp_completed": completed_at,
            },
        )
        connection.commit()
        completed += 1

    status = "aborted" if abort_reason else "failed" if failed else "passed"
    update_shard_state(shard_path, status=status, completed_calls=completed, failed_calls=failed, skipped_calls=skipped, invalid_outputs=invalid, abort_reason=abort_reason)
    summary = {
        "status": status,
        "milestone": args.milestone,
        "run_id": args.run_id,
        "db_path": str(db_path),
        "shard": str(shard_path),
        "completed_calls": completed,
        "failed_calls": failed,
        "skipped_completed_calls": skipped,
        "invalid_outputs": invalid,
        "abort_reason": abort_reason,
        "plan_summary": plan_summary,
    }
    ledger_export = write_api_call_ledger(connection, args.run_id, args.milestone, out_dir, target_api_call_ids=target_api_call_ids)
    report_export = write_milestone_report(connection, args.run_id, args.milestone, out_dir, target_api_call_ids=target_api_call_ids)
    summary["call_ledger_export"] = ledger_export
    summary["milestone_report_export"] = {
        "json_path": report_export["json_path"],
        "md_path": report_export["md_path"],
    }
    (out_dir / f"execution_summary_{args.milestone}.json").write_text(
        json.dumps(summary, sort_keys=True, indent=2),
        encoding="utf-8",
    )
    connection.close()
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Execute a resume-safe production milestone shard.")
    parser.add_argument("--milestone", required=True, choices=("1", "10", "50", "3k", "6k", "13k", "25k", "35k", "50k"))
    parser.add_argument("--run-id", default="production_milestones_cumulative_v1")
    parser.add_argument("--out-dir", default="runs")
    parser.add_argument("--db")
    parser.add_argument("--models", required=True, help="Exactly five comma-separated frozen model IDs.")
    parser.add_argument("--splits", default="train,dev,test")
    parser.add_argument("--seed", type=int, default=20260615)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--shard-count", type=int, default=20)
    parser.add_argument("--max-calls", type=int)
    parser.add_argument("--mock-provider", action="store_true")
    parser.add_argument("--allow-prework-blocked", action="store_true")
    return parser


def main() -> None:
    try:
        summary = run(build_parser().parse_args())
    except ConfigurationError as exc:
        raise SystemExit(f"Configuration error: {exc}") from exc
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
