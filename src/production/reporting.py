from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import sqlite3
from typing import Any

from metrics.agreement_surplus import agreement_surplus
from metrics.distribution_gap import distribution_agreement_gap
from metrics.sampling_compression import sampling_compression
from pilot.pilot_diagnostics import evaluate_milestone_alignment, milestone_validity_check
from protocol.label_schema import LABELS
from protocol.prompt_modes import PromptMode


def json_dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def _json_loads(raw: str | None) -> Any:
    if raw is None or raw == "":
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _target_call_ids(
    connection: sqlite3.Connection,
    run_id: str,
    milestone: str,
    target_api_call_ids: set[str] | None = None,
) -> set[str]:
    if target_api_call_ids is not None:
        return set(target_api_call_ids)
    rows = connection.execute(
        "SELECT api_call_id FROM planned_api_calls WHERE run_id = ? AND milestone = ?",
        (run_id, milestone),
    ).fetchall()
    return {str(row["api_call_id"]) for row in rows}


def api_call_ledger_rows(
    connection: sqlite3.Connection,
    run_id: str,
    milestone: str,
    target_api_call_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    target_ids = _target_call_ids(connection, run_id, milestone, target_api_call_ids)
    if target_api_call_ids is not None and not target_ids:
        return []
    target_filter = "p.run_id = ? AND p.milestone = ?"
    params: tuple[Any, ...] = (run_id, milestone)
    if target_api_call_ids is not None:
        placeholders = ",".join("?" for _ in target_ids)
        target_filter = f"p.run_id = ? AND p.api_call_id IN ({placeholders})"
        params = (run_id, *tuple(target_ids))
    rows = connection.execute(
        f"""
        SELECT
          p.api_call_id AS planned_call_id,
          p.run_id,
          p.milestone,
          p.component_type AS call_type,
          p.item_id,
          p.dataset_id,
          p.model_id,
          p.prompt_mode,
          p.assignment_hash,
          p.sample_id,
          p.prompt_hash AS rendered_prompt_hash,
          p.request_json AS planned_request_json,
          p.status AS planned_status,
          p.created_at AS planned_created_at,
          i.split,
          i.source_item_id,
          i.item_length_chars,
          sv.count_author,
          sv.count_other,
          sv.count_everybody,
          sv.count_nobody,
          sv.count_info,
          sv.annotation_count,
          sv.source_vote_version,
          sd.source_distribution_version,
          sd.p_author AS source_p_author,
          sd.p_other AS source_p_other,
          sd.p_everybody AS source_p_everybody,
          sd.p_nobody AS source_p_nobody,
          sd.p_info AS source_p_info,
          sd.entropy AS source_entropy,
          sd.entropy_normalized AS source_entropy_normalized,
          sd.majority_label AS source_majority_label,
          sd.majority_support AS source_majority_support,
          sd.majority_margin AS source_majority_margin,
          sd.disagreement_bin,
          pa.label_order AS canonical_label_order,
          pa.prompt_paraphrase_id,
          pa.seed AS item_order_seed,
          raw.provider,
          raw.api_route,
          raw.temperature_or_null,
          raw.top_p_or_null,
          raw.seed_if_available,
          raw.structured_output_mode,
          raw.request_json AS provider_request_json,
          raw.raw_response,
          raw.finish_reason_or_null,
          raw.input_tokens,
          raw.output_tokens,
          raw.cost_usd_if_available,
          raw.timestamp_started,
          raw.timestamp_completed,
          raw.api_error_flag,
          raw.api_error_type,
          raw.http_status_code,
          raw.retry_count,
          raw.error_response_body,
          raw.transport_error_message,
          raw.terminal_failure_flag,
          po.validity_status,
          po.repair_attempted,
          po.repair_successful,
          po.refusal_flag,
          po.malformed_flag,
          po.off_schema_label_flag,
          po.probability_sum,
          po.chosen_label,
          po.estimated_source_community_agreement,
          po.moral_certainty,
          po.p_author,
          po.p_other,
          po.p_everybody,
          po.p_nobody,
          po.p_info,
          po.most_likely_label,
          po.recognition_status,
          po.recognition_confidence,
          ex.exclusion_rule,
          ex.reason AS exclusion_reason
        FROM planned_api_calls p
        LEFT JOIN items i ON i.item_id = p.item_id
        LEFT JOIN source_votes sv ON sv.item_id = p.item_id
        LEFT JOIN source_distributions sd ON sd.item_id = p.item_id AND sd.posterior_draw_id_or_null IS NULL
        LEFT JOIN prompt_assignments pa ON pa.assignment_hash = p.assignment_hash
        LEFT JOIN api_calls_raw raw ON raw.api_call_id = p.api_call_id
        LEFT JOIN parsed_outputs po ON po.api_call_id = p.api_call_id
        LEFT JOIN exclusion_log ex ON ex.api_call_id = p.api_call_id
        WHERE {target_filter}
        ORDER BY p.api_call_id
        """,
        params,
    ).fetchall()
    ledger: list[dict[str, Any]] = []
    for row in rows:
        record = dict(row)
        request = _json_loads(record.pop("planned_request_json", None)) or {}
        provider_request = _json_loads(record.get("provider_request_json"))
        record["is_pilot"] = bool(request.get("is_pilot"))
        record["is_confirmatory"] = bool(request.get("is_confirmatory"))
        record["max_tokens"] = provider_request.get("max_tokens") if isinstance(provider_request, dict) else None
        record["final_usable_status"] = _final_usable_status(record)
        record["included_in_primary"] = _included_in_primary(record)
        record["source_distribution_json"] = json_dumps({label: record.get(f"source_p_{label}") for label in LABELS})
        record["parsed_distribution_json"] = json_dumps({label: record.get(f"p_{label}") for label in LABELS})
        ledger.append(record)
    return ledger


def _final_usable_status(record: dict[str, Any]) -> str:
    if record.get("api_error_flag"):
        return "api_error_terminal" if record.get("terminal_failure_flag") else "api_error_retryable"
    status = record.get("validity_status")
    if status in {"valid_strict_schema", "valid_after_repair", "valid_extracted_json"}:
        return "usable"
    if status:
        return str(status)
    return "not_attempted"


def _included_in_primary(record: dict[str, Any]) -> bool:
    return record.get("validity_status") in {"valid_strict_schema", "valid_after_repair", "valid_extracted_json"} and not record.get("exclusion_rule")


def write_api_call_ledger(
    connection: sqlite3.Connection,
    run_id: str,
    milestone: str,
    out_dir: Path,
    target_api_call_ids: set[str] | None = None,
) -> dict[str, Any]:
    rows = api_call_ledger_rows(connection, run_id, milestone, target_api_call_ids=target_api_call_ids)
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = out_dir / f"call_ledger_{milestone}.jsonl"
    csv_path = out_dir / f"call_ledger_{milestone}.csv"
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json_dumps(row) + "\n")
    fieldnames = sorted({key for row in rows for key in row})
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return {"rows": len(rows), "jsonl_path": str(jsonl_path), "csv_path": str(csv_path)}


def build_milestone_report(
    connection: sqlite3.Connection,
    run_id: str,
    milestone: str,
    target_api_call_ids: set[str] | None = None,
) -> dict[str, Any]:
    target_ids = _target_call_ids(connection, run_id, milestone, target_api_call_ids)
    attempted = _attempted_counts(connection, target_ids)
    validity_rows = _validity_rows(connection, target_ids)
    validity_check = _json_safe_validity_check(milestone_validity_check(validity_rows, milestone)) if validity_rows else None
    observed = _observed_alignment(connection, target_ids, milestone)
    decision = evaluate_milestone_alignment(milestone, observed) if observed else None
    return {
        "run_id": run_id,
        "milestone": milestone,
        "calls_attempted_and_completed": attempted,
        "retry_rate": _retry_rate(connection, target_ids),
        "json_validity_by_model_and_mode": _validity_by_model_mode(validity_rows),
        "malformed_refusal_off_schema_rate": _malformed_refusal_off_schema_rate(validity_rows),
        "distribution_entropy_by_disagreement_bin": _distribution_entropy_by_bin(connection, target_ids),
        "agreement_surplus_by_bin_model": _agreement_surplus_by_bin_model(connection, target_ids),
        "distribution_agreement_gap_by_bin_model": _distribution_agreement_gap_by_bin_model(connection, target_ids),
        "sampling_compression_if_available": _sampling_compression_by_model(connection, target_ids),
        "paraphrase_label_order_check": _paraphrase_label_order_check(connection, target_ids),
        "decision": decision
        or {
            "milestone": milestone,
            "decision": "pending_insufficient_outputs",
            "failures": [],
            "revision_reasons": [],
            "observed": observed,
        },
        "validity_gate": validity_check,
    }


def write_milestone_report(
    connection: sqlite3.Connection,
    run_id: str,
    milestone: str,
    out_dir: Path,
    target_api_call_ids: set[str] | None = None,
) -> dict[str, Any]:
    report = build_milestone_report(connection, run_id, milestone, target_api_call_ids=target_api_call_ids)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"milestone_report_{milestone}.json"
    md_path = out_dir / f"milestone_report_{milestone}.md"
    json_path.write_text(json.dumps(report, sort_keys=True, indent=2), encoding="utf-8")
    md_path.write_text(_render_milestone_report_md(report), encoding="utf-8")
    return {"json_path": str(json_path), "md_path": str(md_path), "report": report}


def _attempted_counts(connection: sqlite3.Connection, target_ids: set[str]) -> dict[str, int]:
    if not target_ids:
        return {"planned": 0, "attempted": 0, "completed_successful": 0, "api_errors": 0, "terminal_failures": 0}
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"""
        SELECT api_error_flag, terminal_failure_flag, raw_response
        FROM api_calls_raw
        WHERE api_call_id IN ({placeholders})
        """,
        tuple(target_ids),
    ).fetchall()
    return {
        "planned": len(target_ids),
        "attempted": len(rows),
        "completed_successful": sum(1 for row in rows if not row["api_error_flag"] and row["raw_response"]),
        "api_errors": sum(1 for row in rows if row["api_error_flag"]),
        "terminal_failures": sum(1 for row in rows if row["terminal_failure_flag"]),
    }


def _retry_rate(connection: sqlite3.Connection, target_ids: set[str]) -> dict[str, float | int]:
    if not target_ids:
        return {"attempted_calls": 0, "calls_with_retry": 0, "retry_rate": 0.0}
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"SELECT retry_count FROM api_calls_raw WHERE api_call_id IN ({placeholders})",
        tuple(target_ids),
    ).fetchall()
    with_retry = sum(1 for row in rows if int(row["retry_count"] or 0) > 0)
    return {"attempted_calls": len(rows), "calls_with_retry": with_retry, "retry_rate": with_retry / len(rows) if rows else 0.0}


def _validity_rows(connection: sqlite3.Connection, target_ids: set[str]) -> list[dict[str, Any]]:
    if not target_ids:
        return []
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"""
        SELECT model_id, prompt_mode, validity_status, refusal_flag, malformed_flag, off_schema_label_flag
        FROM parsed_outputs
        WHERE api_call_id IN ({placeholders})
        """,
        tuple(target_ids),
    ).fetchall()
    return [dict(row) for row in rows]


def _validity_by_model_mode(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for row in rows:
        key = (str(row["model_id"]), str(row["prompt_mode"]))
        counts[key]["total"] += 1
        counts[key][str(row["validity_status"])] += 1
    out = []
    for (model_id, prompt_mode), counter in sorted(counts.items()):
        total = counter["total"]
        valid = counter["valid_strict_schema"] + counter["valid_after_repair"] + counter["valid_extracted_json"]
        out.append({"model_id": model_id, "prompt_mode": prompt_mode, "n": total, "valid_rate": valid / total if total else 0.0})
    return out


def _json_safe_validity_check(check: dict[str, Any]) -> dict[str, Any]:
    safe = dict(check)
    rates = safe.get("validity_rates")
    if isinstance(rates, dict):
        safe["validity_rates"] = [
            {"model_id": key[0], "prompt_mode": key[1], **dict(value)}
            for key, value in sorted(rates.items())
        ]
    return safe


def _malformed_refusal_off_schema_rate(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    total = len(rows)
    return {
        "n": total,
        "malformed_rate": sum(1 for row in rows if row.get("malformed_flag")) / total if total else 0.0,
        "refusal_rate": sum(1 for row in rows if row.get("refusal_flag")) / total if total else 0.0,
        "off_schema_rate": sum(1 for row in rows if row.get("off_schema_label_flag")) / total if total else 0.0,
    }


def _distribution_entropy_by_bin(connection: sqlite3.Connection, target_ids: set[str]) -> list[dict[str, Any]]:
    if not target_ids:
        return []
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"""
        SELECT DISTINCT sd.disagreement_bin, p.item_id, sd.entropy, sd.entropy_normalized
        FROM planned_api_calls p
        JOIN source_distributions sd ON sd.item_id = p.item_id AND sd.posterior_draw_id_or_null IS NULL
        WHERE p.api_call_id IN ({placeholders})
        """,
        tuple(target_ids),
    ).fetchall()
    by_bin: dict[str, list[sqlite3.Row]] = defaultdict(list)
    for row in rows:
        by_bin[str(row["disagreement_bin"])].append(row)
    return [
        {
            "disagreement_bin": bin_name,
            "n_items": len(values),
            "mean_entropy": sum(float(row["entropy"]) for row in values) / len(values),
            "mean_entropy_normalized": sum(float(row["entropy_normalized"]) for row in values) / len(values),
        }
        for bin_name, values in sorted(by_bin.items())
        if values
    ]


def _source_distribution(row: sqlite3.Row) -> dict[str, float]:
    return {label: float(row[f"source_p_{label}"]) for label in LABELS}


def _agreement_surplus_by_bin_model(connection: sqlite3.Connection, target_ids: set[str]) -> list[dict[str, Any]]:
    if not target_ids:
        return []
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"""
        SELECT p.model_id, sd.disagreement_bin, sd.p_author AS source_p_author,
               sd.p_other AS source_p_other, sd.p_everybody AS source_p_everybody,
               sd.p_nobody AS source_p_nobody, sd.p_info AS source_p_info,
               po.chosen_label, po.estimated_source_community_agreement
        FROM planned_api_calls p
        JOIN parsed_outputs po ON po.api_call_id = p.api_call_id
        JOIN source_distributions sd ON sd.item_id = p.item_id AND sd.posterior_draw_id_or_null IS NULL
        WHERE p.api_call_id IN ({placeholders})
          AND p.prompt_mode IN (?, ?)
          AND po.chosen_label IS NOT NULL
          AND po.estimated_source_community_agreement IS NOT NULL
        """,
        (*tuple(target_ids), PromptMode.DESCRIPTIVE_VERDICT.value, PromptMode.PARAPHRASED_DESCRIPTIVE_VERDICT.value),
    ).fetchall()
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["disagreement_bin"]), str(row["model_id"]))].append(
            agreement_surplus(float(row["estimated_source_community_agreement"]), _source_distribution(row), str(row["chosen_label"]))
        )
    return _mean_records(grouped, "agreement_surplus_mean")


def _distribution_agreement_gap_by_bin_model(connection: sqlite3.Connection, target_ids: set[str]) -> list[dict[str, Any]]:
    if not target_ids:
        return []
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"""
        SELECT vd.model_id, sd.disagreement_bin, vd.item_id, vd.chosen_label,
               vd.estimated_source_community_agreement,
               dist.p_author, dist.p_other, dist.p_everybody, dist.p_nobody, dist.p_info
        FROM (
          SELECT p.item_id, p.model_id, po.chosen_label, po.estimated_source_community_agreement
          FROM planned_api_calls p
          JOIN parsed_outputs po ON po.api_call_id = p.api_call_id
          WHERE p.api_call_id IN ({placeholders})
            AND p.prompt_mode = ?
        ) vd
        JOIN (
          SELECT p.item_id, p.model_id, po.p_author, po.p_other, po.p_everybody, po.p_nobody, po.p_info
          FROM planned_api_calls p
          JOIN parsed_outputs po ON po.api_call_id = p.api_call_id
          WHERE p.api_call_id IN ({placeholders})
            AND p.prompt_mode = ?
        ) dist ON dist.item_id = vd.item_id AND dist.model_id = vd.model_id
        JOIN source_distributions sd ON sd.item_id = vd.item_id AND sd.posterior_draw_id_or_null IS NULL
        WHERE vd.chosen_label IS NOT NULL AND vd.estimated_source_community_agreement IS NOT NULL
        """,
        (*tuple(target_ids), PromptMode.DESCRIPTIVE_VERDICT.value, *tuple(target_ids), PromptMode.DISTRIBUTION.value),
    ).fetchall()
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        distribution = {label: float(row[f"p_{label}"]) for label in LABELS}
        grouped[(str(row["disagreement_bin"]), str(row["model_id"]))].append(
            distribution_agreement_gap(float(row["estimated_source_community_agreement"]), distribution, str(row["chosen_label"]))
        )
    return _mean_records(grouped, "distribution_agreement_gap_mean")


def _sampling_compression_by_model(connection: sqlite3.Connection, target_ids: set[str]) -> list[dict[str, Any]]:
    if not target_ids:
        return []
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"""
        SELECT p.item_id, p.model_id, sd.disagreement_bin,
               sd.p_author AS source_p_author, sd.p_other AS source_p_other,
               sd.p_everybody AS source_p_everybody, sd.p_nobody AS source_p_nobody,
               sd.p_info AS source_p_info, po.chosen_label
        FROM planned_api_calls p
        JOIN parsed_outputs po ON po.api_call_id = p.api_call_id
        JOIN source_distributions sd ON sd.item_id = p.item_id AND sd.posterior_draw_id_or_null IS NULL
        WHERE p.api_call_id IN ({placeholders})
          AND p.prompt_mode = ?
          AND po.chosen_label IS NOT NULL
        """,
        (*tuple(target_ids), PromptMode.SAMPLING.value),
    ).fetchall()
    by_pair: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (str(row["item_id"]), str(row["model_id"]), str(row["disagreement_bin"]))
        entry = by_pair.setdefault(key, {"source": _source_distribution(row), "labels": []})
        entry["labels"].append(str(row["chosen_label"]))
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for (_item_id, model_id, bin_name), entry in by_pair.items():
        if len(entry["labels"]) >= 2:
            grouped[(bin_name, model_id)].append(sampling_compression(entry["source"], entry["labels"]))
    return _mean_records(grouped, "sampling_compression_mean")


def _mean_records(grouped: dict[tuple[str, str], list[float]], field: str) -> list[dict[str, Any]]:
    return [
        {"disagreement_bin": bin_name, "model_id": model_id, "n": len(values), field: sum(values) / len(values)}
        for (bin_name, model_id), values in sorted(grouped.items())
        if values
    ]


def _paraphrase_label_order_check(connection: sqlite3.Connection, target_ids: set[str]) -> dict[str, Any]:
    if not target_ids:
        return {"status": "not_available", "paraphrase_outputs": 0, "unique_label_orders": 0}
    placeholders = ",".join("?" for _ in target_ids)
    rows = connection.execute(
        f"""
        SELECT p.prompt_mode, pa.label_order, po.validity_status
        FROM planned_api_calls p
        LEFT JOIN prompt_assignments pa ON pa.assignment_hash = p.assignment_hash
        LEFT JOIN parsed_outputs po ON po.api_call_id = p.api_call_id
        WHERE p.api_call_id IN ({placeholders})
        """,
        tuple(target_ids),
    ).fetchall()
    paraphrase = [
        row for row in rows if str(row["prompt_mode"]) in {PromptMode.PARAPHRASED_DISTRIBUTION.value, PromptMode.PARAPHRASED_DESCRIPTIVE_VERDICT.value}
    ]
    valid_paraphrase = [row for row in paraphrase if row["validity_status"] in {"valid_strict_schema", "valid_after_repair", "valid_extracted_json"}]
    unique_orders = {str(row["label_order"]) for row in rows if row["label_order"]}
    return {
        "status": "available" if paraphrase else "not_available",
        "paraphrase_outputs": len(paraphrase),
        "valid_paraphrase_outputs": len(valid_paraphrase),
        "unique_label_orders": len(unique_orders),
    }


def _observed_alignment(connection: sqlite3.Connection, target_ids: set[str], milestone: str) -> dict[str, Any]:
    validity_rows = _validity_rows(connection, target_ids)
    if not validity_rows:
        return {}
    validity = milestone_validity_check(validity_rows, milestone)
    surplus = _agreement_surplus_by_bin_model(connection, target_ids)
    gaps = _distribution_agreement_gap_by_bin_model(connection, target_ids)
    sampling = _sampling_compression_by_model(connection, target_ids)
    low_bins = {"low_consensus", "diffuse"}
    low_gap_values = [row["distribution_agreement_gap_mean"] for row in gaps if row["disagreement_bin"] in low_bins]
    high_gap_values = [row["distribution_agreement_gap_mean"] for row in gaps if row["disagreement_bin"] == "high_consensus"]
    low_surplus_values = [row["agreement_surplus_mean"] for row in surplus if row["disagreement_bin"] in low_bins]
    return {
        "overall_validity_rate": validity["overall_validity_rate"],
        "min_model_mode_validity_rate": min((row["valid_rate"] for row in _validity_by_model_mode(validity_rows)), default=0.0),
        "positive_gap_models": len({row["model_id"] for row in gaps if row["distribution_agreement_gap_mean"] > 0}),
        "positive_surplus_models": len({row["model_id"] for row in surplus if row["agreement_surplus_mean"] > 0}),
        "low_diffuse_distribution_agreement_gap_mean": sum(low_gap_values) / len(low_gap_values) if low_gap_values else None,
        "high_consensus_distribution_agreement_gap_mean": sum(high_gap_values) / len(high_gap_values) if high_gap_values else None,
        "low_diffuse_agreement_surplus_mean": sum(low_surplus_values) / len(low_surplus_values) if low_surplus_values else None,
        "positive_sampling_compression_models": len({row["model_id"] for row in sampling if row["sampling_compression_mean"] > 0}),
    }


def _render_milestone_report_md(report: dict[str, Any]) -> str:
    lines = [
        f"# Milestone Report: {report['milestone']}",
        "",
        f"- Run ID: `{report['run_id']}`",
        f"- Decision: `{report['decision']['decision']}`",
        "",
        "## 1. Calls Attempted And Completed",
        "```json",
        json.dumps(report["calls_attempted_and_completed"], sort_keys=True, indent=2),
        "```",
        "## 2. Retry Rate",
        "```json",
        json.dumps(report["retry_rate"], sort_keys=True, indent=2),
        "```",
        "## 3. JSON Validity By Model And Mode",
        "```json",
        json.dumps(report["json_validity_by_model_and_mode"], sort_keys=True, indent=2),
        "```",
        "## 4. Malformed / Refusal / Off-Schema Rate",
        "```json",
        json.dumps(report["malformed_refusal_off_schema_rate"], sort_keys=True, indent=2),
        "```",
        "## 5. Distribution Entropy By Disagreement Bin",
        "```json",
        json.dumps(report["distribution_entropy_by_disagreement_bin"], sort_keys=True, indent=2),
        "```",
        "## 6. Agreement Surplus By Bin / Model",
        "```json",
        json.dumps(report["agreement_surplus_by_bin_model"], sort_keys=True, indent=2),
        "```",
        "## 7. Distribution-Agreement Gap By Bin / Model",
        "```json",
        json.dumps(report["distribution_agreement_gap_by_bin_model"], sort_keys=True, indent=2),
        "```",
        "## 8. Sampling Compression If Available",
        "```json",
        json.dumps(report["sampling_compression_if_available"], sort_keys=True, indent=2),
        "```",
        "## 9. Paraphrase / Label-Order Check",
        "```json",
        json.dumps(report["paraphrase_label_order_check"], sort_keys=True, indent=2),
        "```",
        "## 10. Continue / Revise / Stop Decision",
        "```json",
        json.dumps(report["decision"], sort_keys=True, indent=2),
        "```",
        "",
    ]
    return "\n".join(lines)
