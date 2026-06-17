from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3
from typing import Any

from parsing.validate_json import parse_and_validate
from parsing.validity_status import ValidityStatus
from production.config import ConfigurationError, getenv, load_execution_config, parse_model_ids
from production.execute_milestone import json_dumps
from production.providers import InferenceRequest, build_adapters
from production.run_milestone import pending_requests, write_jsonl
from prompts.prompt_hashing import prompt_hash
from prompts.prompt_templates import render_prompt
from protocol.prompt_modes import PromptMode
from storage.db import connect, migrate
from utils.hashing import stable_hash


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_target_call_ids(run_dir: Path, milestone: str) -> set[str] | None:
    path = run_dir / f"target_api_call_ids_{milestone}.jsonl"
    if not path.exists():
        return None
    target_ids: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                target_ids.add(str(json.loads(line)["api_call_id"]))
    return target_ids


def _blocked_paraphrase_rows(
    connection: sqlite3.Connection,
    run_id: str,
    milestone: str,
    target_api_call_ids: set[str] | None,
) -> list[sqlite3.Row]:
    rows = connection.execute(
        """
        SELECT p.api_call_id, p.item_id, p.request_json, i.item_text
        FROM planned_api_calls p
        JOIN items i ON i.item_id = p.item_id
        WHERE p.run_id = ?
          AND p.milestone = ?
          AND p.prompt_mode IN (?, ?)
        ORDER BY p.item_id, p.api_call_id
        """,
        (
            run_id,
            milestone,
            PromptMode.PARAPHRASED_DISTRIBUTION.value,
            PromptMode.PARAPHRASED_DESCRIPTIVE_VERDICT.value,
        ),
    ).fetchall()
    blocked: list[sqlite3.Row] = []
    for row in rows:
        if target_api_call_ids is not None and str(row["api_call_id"]) not in target_api_call_ids:
            continue
        request = json.loads(str(row["request_json"]))
        if request.get("prework_required"):
            blocked.append(row)
    return blocked


def _existing_paraphrase(connection: sqlite3.Connection, paraphrase_pair_id: str) -> str | None:
    row = connection.execute(
        "SELECT paraphrased_text FROM paraphrase_pairs WHERE paraphrase_pair_id = ?",
        (paraphrase_pair_id,),
    ).fetchone()
    return str(row["paraphrased_text"]) if row else None


def _generate_paraphrase(adapter: Any, helper_model_id: str, item_text: str) -> str:
    prompt = (
        render_prompt(PromptMode.PARAPHRASE_GENERATION, item_text, ())
        + "\n\nThe JSON string value must not contain literal newline characters; keep the paraphrase as one paragraph."
    )
    envelope = adapter.run_single_turn(
        InferenceRequest(
            prompt=prompt,
            model_id=helper_model_id,
            prompt_mode=PromptMode.PARAPHRASE_GENERATION.value,
            response_schema=PromptMode.PARAPHRASE_GENERATION.value,
        )
    )
    parsed = parse_and_validate(envelope.raw_text, PromptMode.PARAPHRASE_GENERATION)
    if parsed.status == ValidityStatus.VALID_STRICT_SCHEMA and parsed.parsed_json:
        return str(parsed.parsed_json["paraphrased_situation"]).strip()
    coerced = _coerce_paraphrase_text(envelope.raw_text)
    if coerced is None:
        raise RuntimeError(f"invalid paraphrase helper output: {parsed.status.value}; raw={envelope.raw_text[:500]!r}")
    return coerced


def _coerce_paraphrase_text(raw_text: str) -> str | None:
    match = re.search(r'"paraphrased_situation"\s*:\s*"(.*)"\s*\}\s*$', raw_text, flags=re.DOTALL)
    if not match:
        return None
    text = match.group(1)
    text = text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    text = text.replace('\\"', '"').replace("\\/", "/").replace("\\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) >= 20 else None


def _update_item_requests(
    connection: sqlite3.Connection,
    rows: list[sqlite3.Row],
    paraphrased_text: str,
) -> int:
    updated = 0
    for row in rows:
        request = json.loads(str(row["request_json"]))
        prompt_mode = PromptMode(str(request["prompt_mode"]))
        rendered_prompt = render_prompt(prompt_mode, paraphrased_text, request["label_order"])
        rendered_hash = prompt_hash(rendered_prompt)
        request["prompt"] = rendered_prompt
        request["prompt_hash"] = rendered_hash
        request["prework_required"] = []
        connection.execute(
            """
            UPDATE planned_api_calls
            SET prompt_hash = ?, request_json = ?
            WHERE api_call_id = ?
            """,
            (rendered_hash, json_dumps(request), row["api_call_id"]),
        )
        updated += 1
    return updated


def run(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = Path(args.out_dir) / args.run_id
    db_path = Path(args.db) if args.db else run_dir / "study.sqlite"
    helper_model_id = args.helper_model or getenv("PARAPHRASE_HELPER_MODEL_ID", "grok-4.3") or "grok-4.3"
    model_ids = parse_model_ids(args.models)
    if helper_model_id not in model_ids:
        raise ConfigurationError(f"Paraphrase helper model {helper_model_id!r} must be included in STUDY_MODEL_IDS")
    execution_config = load_execution_config(model_ids, mock_provider=args.mock_provider)
    helper_provider = execution_config.model_to_provider[helper_model_id]
    adapter = build_adapters(execution_config.providers)[helper_provider]

    connection = connect(db_path)
    migrate(connection)
    target_api_call_ids = _load_target_call_ids(run_dir, args.milestone)
    generated = 0
    reused = 0
    updated_calls = 0
    try:
        blocked_rows = _blocked_paraphrase_rows(connection, args.run_id, args.milestone, target_api_call_ids)
        rows_by_item: dict[str, list[sqlite3.Row]] = {}
        for row in blocked_rows:
            rows_by_item.setdefault(str(row["item_id"]), []).append(row)
        for item_index, (item_id, item_rows) in enumerate(rows_by_item.items(), start=1):
            if args.max_items is not None and item_index > args.max_items:
                break
            first_request = json.loads(str(item_rows[0]["request_json"]))
            prompt_paraphrase_id = str(first_request.get("prompt_paraphrase_id") or "p00")
            paraphrase_pair_id = stable_hash(["paraphrase_pair", args.run_id, args.milestone, item_id, prompt_paraphrase_id])
            paraphrased_text = _existing_paraphrase(connection, paraphrase_pair_id)
            if paraphrased_text is None:
                paraphrased_text = _generate_paraphrase(adapter, helper_model_id, str(item_rows[0]["item_text"]))
                connection.execute(
                    """
                    INSERT INTO paraphrase_pairs (
                      paraphrase_pair_id, item_id, original_text, paraphrased_text, helper_model_id, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (paraphrase_pair_id, item_id, str(item_rows[0]["item_text"]), paraphrased_text, helper_model_id, utc_now()),
                )
                generated += 1
            else:
                reused += 1
            updated_calls += _update_item_requests(connection, item_rows, paraphrased_text)
            connection.commit()
            print(
                f"[{utc_now()}] materialized_paraphrase item={item_index}/{len(rows_by_item)} "
                f"item_id={item_id} updated_calls={updated_calls}",
                flush=True,
            )
        pending = pending_requests(connection, args.run_id, args.milestone, target_api_call_ids=target_api_call_ids)
        write_jsonl(run_dir / f"pending_api_calls_{args.milestone}.jsonl", pending)
    finally:
        connection.close()
    return {
        "run_id": args.run_id,
        "milestone": args.milestone,
        "db_path": str(db_path),
        "helper_model_id": helper_model_id,
        "generated_paraphrases": generated,
        "reused_paraphrases": reused,
        "updated_blocked_calls": updated_calls,
        "pending_jsonl": str(run_dir / f"pending_api_calls_{args.milestone}.jsonl"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Materialize paraphrase-audit prework and unblock planned calls.")
    parser.add_argument("--milestone", required=True, choices=("3k", "6k", "13k", "25k", "35k", "50k"))
    parser.add_argument("--run-id", default="production_milestones_cumulative_v1")
    parser.add_argument("--out-dir", default="runs")
    parser.add_argument("--db")
    parser.add_argument("--models", required=True, help="Exactly five comma-separated model IDs.")
    parser.add_argument("--helper-model")
    parser.add_argument("--max-items", type=int)
    parser.add_argument("--mock-provider", action="store_true")
    return parser


def main() -> None:
    try:
        summary = run(build_parser().parse_args())
    except ConfigurationError as exc:
        raise SystemExit(f"Configuration error: {exc}") from exc
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
