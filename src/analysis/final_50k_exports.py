from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

from metrics.distributions import brier_for_majority_label, jensen_shannon_divergence, total_variation_distance
from metrics.sampling_compression import sample_label_distribution
from protocol.disagreement_bins import disagreement_bin
from protocol.label_schema import LABELS
from source_uncertainty.smoothing import shannon_entropy


VALID_PRIMARY = {"valid_strict_schema", "valid_after_repair", "valid_extracted_json"}
STRICT_VALID = {"valid_strict_schema"}
LOW_DIFFUSE = {"low_consensus", "diffuse"}


def load_target_ids(run_dir: Path, milestone: str) -> set[str]:
    path = run_dir / f"target_api_call_ids_{milestone}.jsonl"
    return {
        str(json.loads(line)["api_call_id"])
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def prepare_target_table(con: sqlite3.Connection, target_ids: set[str]) -> None:
    con.execute("DROP TABLE IF EXISTS temp_final_target_ids")
    con.execute("CREATE TEMP TABLE temp_final_target_ids(api_call_id TEXT PRIMARY KEY)")
    con.executemany("INSERT INTO temp_final_target_ids(api_call_id) VALUES (?)", ((i,) for i in target_ids))


def source_distribution(row: dict[str, Any], prefix: str = "source_p_") -> dict[str, float]:
    return {label: float(row[f"{prefix}{label}"]) for label in LABELS}


def parsed_distribution(row: dict[str, Any], prefix: str = "p_") -> dict[str, float] | None:
    out: dict[str, float] = {}
    for label in LABELS:
        value = row.get(f"{prefix}{label}")
        if value is None:
            return None
        out[label] = float(value)
    return out


def source_probability_for_label(row: dict[str, Any], label: str) -> float:
    return float(row[f"source_p_{label}"])


def included_primary(row: dict[str, Any]) -> bool:
    return str(row.get("validity_status")) in VALID_PRIMARY


def included_strict(row: dict[str, Any]) -> bool:
    return str(row.get("validity_status")) in STRICT_VALID


def read_analysis_rows(con: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = con.execute(
        """
        SELECT
          p.api_call_id,
          p.component_type,
          p.component_name,
          p.item_id,
          p.dataset_id,
          p.model_id,
          p.prompt_mode,
          p.sample_id,
          p.prompt_hash,
          raw.provider,
          raw.api_route,
          raw.temperature_or_null,
          raw.top_p_or_null,
          raw.reasoning_effort_or_null,
          raw.structured_output_mode,
          raw.timestamp_started,
          raw.timestamp_completed,
          raw.api_error_flag,
          raw.api_error_type,
          raw.terminal_failure_flag,
          raw.retry_count,
          raw.cost_usd_if_available,
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
          sv.count_author,
          sv.count_other,
          sv.count_everybody,
          sv.count_nobody,
          sv.count_info,
          sv.annotation_count,
          sd.p_author AS source_p_author,
          sd.p_other AS source_p_other,
          sd.p_everybody AS source_p_everybody,
          sd.p_nobody AS source_p_nobody,
          sd.p_info AS source_p_info,
          sd.majority_label AS source_majority_label,
          sd.majority_support AS source_majority_support,
          sd.majority_margin AS source_majority_margin,
          sd.entropy AS source_entropy,
          sd.entropy_normalized AS source_entropy_normalized,
          sd.disagreement_bin
        FROM planned_api_calls p
        JOIN temp_final_target_ids t ON t.api_call_id = p.api_call_id
        LEFT JOIN api_calls_raw raw ON raw.api_call_id = p.api_call_id
        LEFT JOIN parsed_outputs po ON po.api_call_id = p.api_call_id
        LEFT JOIN source_votes sv ON sv.item_id = p.item_id
        LEFT JOIN source_distributions sd ON sd.item_id = p.item_id AND sd.posterior_draw_id_or_null IS NULL
        ORDER BY p.api_call_id
        """
    ).fetchall()
    return [dict(row) for row in rows]


def write_csv(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def one_row_per_model(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["model_id"])].append(row)
    out = []
    for model_id, values in sorted(grouped.items()):
        providers = sorted({str(row.get("provider")) for row in values if row.get("provider") is not None})
        api_routes = sorted({str(row.get("api_route")) for row in values if row.get("api_route") is not None})
        starts = sorted(str(row.get("timestamp_started")) for row in values if row.get("timestamp_started"))
        ends = sorted(str(row.get("timestamp_completed")) for row in values if row.get("timestamp_completed"))
        out.append({
            "model_id": model_id,
            "provider": "; ".join(providers),
            "api_route": "; ".join(api_routes),
            "target_calls": len(values),
            "first_call_utc": starts[0] if starts else None,
            "last_call_utc": ends[-1] if ends else None,
            "temperature": unique_or_join(row.get("temperature_or_null") for row in values),
            "top_p": unique_or_join(row.get("top_p_or_null") for row in values),
            "reasoning_effort": unique_or_join(row.get("reasoning_effort_or_null") for row in values),
        })
    return out


def unique_or_join(values: Iterable[Any]) -> str | None:
    cleaned = sorted({str(value) for value in values if value is not None})
    if not cleaned:
        return None
    return "; ".join(cleaned)


def component_allocation(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["component_type"]), str(row["prompt_mode"]), str(row["disagreement_bin"]))].append(row)
    out = []
    for (component_type, prompt_mode, bin_name), values in sorted(grouped.items()):
        out.append({
            "component_type": component_type,
            "prompt_mode": prompt_mode,
            "disagreement_bin": bin_name,
            "target_calls": len(values),
            "unique_items": len({str(row["item_id"]) for row in values}),
            "models": len({str(row["model_id"]) for row in values}),
        })
    return out


def derived_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        record = {
            key: row.get(key)
            for key in (
                "api_call_id",
                "component_type",
                "item_id",
                "dataset_id",
                "model_id",
                "prompt_mode",
                "sample_id",
                "provider",
                "api_route",
                "temperature_or_null",
                "top_p_or_null",
                "reasoning_effort_or_null",
                "structured_output_mode",
                "timestamp_started",
                "timestamp_completed",
                "validity_status",
                "repair_attempted",
                "repair_successful",
                "refusal_flag",
                "malformed_flag",
                "off_schema_label_flag",
                "probability_sum",
                "chosen_label",
                "estimated_source_community_agreement",
                "moral_certainty",
                "most_likely_label",
                "source_majority_label",
                "source_majority_support",
                "source_majority_margin",
                "source_entropy",
                "source_entropy_normalized",
                "annotation_count",
                "disagreement_bin",
            )
        }
        for label in LABELS:
            record[f"source_p_{label}"] = row.get(f"source_p_{label}")
            record[f"source_count_{label}"] = row.get(f"count_{label}")
            record[f"model_p_{label}"] = row.get(f"p_{label}")
        record["primary_valid"] = included_primary(row)
        record["strict_valid"] = included_strict(row)
        record["api_error"] = bool(row.get("api_error_flag"))
        record["terminal_failure"] = bool(row.get("terminal_failure_flag"))
        out.append(record)
    return out


def bin_groups(bin_name: str) -> list[str]:
    return [bin_name, "low_diffuse"] if bin_name in LOW_DIFFUSE else [bin_name]


def smoothed_source_from_counts(row: dict[str, Any], alpha: float, smoothing_name: str) -> dict[str, Any]:
    counts = {label: float(row.get(f"count_{label}") or 0.0) for label in LABELS}
    denominator = sum(counts.values()) + alpha * len(LABELS)
    if denominator <= 0:
        return {
            "source_distribution_variant": smoothing_name,
            "source_distribution": source_distribution(row),
            "source_majority_label": row.get("source_majority_label"),
            "source_majority_support": row.get("source_majority_support"),
            "source_majority_margin": row.get("source_majority_margin"),
            "source_entropy": row.get("source_entropy"),
            "source_entropy_normalized": row.get("source_entropy_normalized"),
            "disagreement_bin": row.get("disagreement_bin"),
            "annotation_count": row.get("annotation_count"),
        }
    probs = {label: (counts[label] + alpha) / denominator for label in LABELS}
    ranked = sorted(probs.items(), key=lambda kv: (-kv[1], kv[0]))
    entropy = shannon_entropy(probs.values())
    return {
        "source_distribution_variant": smoothing_name,
        "source_distribution": probs,
        "source_majority_label": ranked[0][0],
        "source_majority_support": ranked[0][1],
        "source_majority_margin": ranked[0][1] - ranked[1][1],
        "source_entropy": entropy,
        "source_entropy_normalized": entropy / math.log2(len(LABELS)),
        "disagreement_bin": disagreement_bin(ranked[0][1]),
        "annotation_count": int(sum(counts.values())),
    }


def primary_source_view(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_distribution_variant": "jeffreys_alpha_0_5",
        "source_distribution": source_distribution(row),
        "source_majority_label": row.get("source_majority_label"),
        "source_majority_support": row.get("source_majority_support"),
        "source_majority_margin": row.get("source_majority_margin"),
        "source_entropy": row.get("source_entropy"),
        "source_entropy_normalized": row.get("source_entropy_normalized"),
        "disagreement_bin": row.get("disagreement_bin"),
        "annotation_count": row.get("annotation_count"),
    }


def endpoint_rows(
    rows: list[dict[str, Any]],
    valid_filter: str = "primary",
    *,
    source_variant: str = "jeffreys_alpha_0_5",
    subset_name: str = "all_items",
) -> dict[str, list[dict[str, Any]]]:
    valid_fn = included_strict if valid_filter == "strict" else included_primary
    if source_variant == "raw_proportion":
        source_view = lambda row: smoothed_source_from_counts(row, 0.0, "raw_proportion")
    elif source_variant == "laplace_alpha_1":
        source_view = lambda row: smoothed_source_from_counts(row, 1.0, "laplace_alpha_1")
    else:
        source_view = primary_source_view

    def keep_subset(row: dict[str, Any]) -> bool:
        view = source_view(row)
        if subset_name == "high_annotation_q75_ge_14":
            return int(view.get("annotation_count") or 0) >= 14
        if subset_name == "exclude_info_majority":
            return str(view.get("source_majority_label")) != "info"
        if subset_name == "exclude_high_info_ge_0_40":
            return float(view["source_distribution"]["info"]) < 0.40
        return True

    desc = [
        row for row in rows
        if row["component_type"] == "core_cross_format"
        and row["prompt_mode"] == "descriptive_verdict_mode"
        and valid_fn(row)
        and keep_subset(row)
        and row.get("chosen_label")
        and row.get("estimated_source_community_agreement") is not None
    ]
    dist = [
        row for row in rows
        if row["component_type"] == "core_cross_format"
        and row["prompt_mode"] == "distribution_mode"
        and valid_fn(row)
        and keep_subset(row)
        and parsed_distribution(row) is not None
    ]
    dist_by_item_model = {(row["item_id"], row["model_id"]): row for row in dist}

    h1a = []
    h1b = []
    for row in desc:
        view = source_view(row)
        label = str(row["chosen_label"])
        surplus = float(row["estimated_source_community_agreement"]) - float(view["source_distribution"][label])
        base = {
            "endpoint": "agreement_surplus",
            "valid_filter": valid_filter,
            "source_distribution_variant": source_variant,
            "subset": subset_name,
            "item_id": row["item_id"],
            "model_id": row["model_id"],
            "provider": row.get("provider"),
            "disagreement_bin": view["disagreement_bin"],
            "source_majority_label": view["source_majority_label"],
            "source_majority_support": view["source_majority_support"],
            "source_majority_margin": view["source_majority_margin"],
            "source_entropy": view["source_entropy"],
            "source_entropy_normalized": view["source_entropy_normalized"],
            "annotation_count": view["annotation_count"],
            "value": surplus,
        }
        h1a.append(base)
        dist_row = dist_by_item_model.get((row["item_id"], row["model_id"]))
        if dist_row is not None:
            distribution = parsed_distribution(dist_row)
            if distribution is not None and label in distribution:
                h1b.append({
                    "endpoint": "distribution_agreement_gap",
                    "valid_filter": valid_filter,
                    "source_distribution_variant": source_variant,
                    "subset": subset_name,
                    "item_id": row["item_id"],
                    "model_id": row["model_id"],
                    "provider": row.get("provider"),
                    "disagreement_bin": view["disagreement_bin"],
                    "source_majority_label": view["source_majority_label"],
                    "source_majority_support": view["source_majority_support"],
                    "source_majority_margin": view["source_majority_margin"],
                    "source_entropy": view["source_entropy"],
                    "source_entropy_normalized": view["source_entropy_normalized"],
                    "annotation_count": view["annotation_count"],
                    "value": float(row["estimated_source_community_agreement"]) - distribution[label],
                    "verdict_agreement": float(row["estimated_source_community_agreement"]),
                    "distribution_probability_for_verdict_label": distribution[label],
                })

    samples = [
        row for row in rows
        if row["component_type"] == "repeated_sampling"
        and row["prompt_mode"] == "sampling_mode"
        and valid_fn(row)
        and keep_subset(row)
        and row.get("chosen_label")
    ]
    sample_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in samples:
        sample_groups[(str(row["item_id"]), str(row["model_id"]))].append(row)
    h1c = []
    for (item_id, model_id), group in sample_groups.items():
        if len(group) < 2:
            continue
        first = group[0]
        view = source_view(first)
        model_dist = sample_label_distribution(str(row["chosen_label"]) for row in group)
        value = float(view["source_entropy"]) - shannon_entropy(model_dist.values())
        h1c.append({
            "endpoint": "sampling_compression",
            "valid_filter": valid_filter,
            "source_distribution_variant": source_variant,
            "subset": subset_name,
            "item_id": item_id,
            "model_id": model_id,
            "provider": first.get("provider"),
            "disagreement_bin": view["disagreement_bin"],
            "source_majority_label": view["source_majority_label"],
            "source_majority_support": view["source_majority_support"],
            "source_majority_margin": view["source_majority_margin"],
            "value": value,
            "source_entropy": float(view["source_entropy"]),
            "source_entropy_normalized": float(view["source_entropy_normalized"]),
            "annotation_count": view["annotation_count"],
            "model_sample_entropy": shannon_entropy(model_dist.values()),
            "n_samples": len(group),
        })
    return {"h1a": h1a, "h1b": h1b, "h1c": h1c}


def summarize_endpoint(endpoint: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        for group_bin in bin_groups(str(row["disagreement_bin"])):
            grouped[(group_bin, "all_models")].append(float(row["value"]))
            grouped[(group_bin, str(row["model_id"]))].append(float(row["value"]))
    return [
        {
            "endpoint": endpoint,
            "disagreement_bin": bin_name,
            "model_id": model_id,
            "n": len(values),
            "mean": mean(values),
        }
        for (bin_name, model_id), values in sorted(grouped.items())
        if values
    ]


def leave_one_model_out(endpoint: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    models = sorted({str(row["model_id"]) for row in rows})
    out = []
    for omitted in models:
        kept = [row for row in rows if str(row["model_id"]) != omitted]
        for summary in summarize_endpoint(endpoint, kept):
            if summary["model_id"] == "all_models":
                summary = dict(summary)
                summary["omitted_model_id"] = omitted
                out.append(summary)
    return out


def bootstrap_ci(
    endpoint: str,
    rows: list[dict[str, Any]],
    *,
    seed: int,
    iterations: int,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_item[str(row["item_id"])].append(row)
    item_ids = sorted(by_item)
    targets = ["low_consensus", "diffuse", "low_diffuse", "high_consensus"]
    estimates: dict[str, list[float]] = {target: [] for target in targets}
    for _ in range(iterations):
        sampled_ids = [rng.choice(item_ids) for _ in item_ids]
        sampled_rows = [row for item_id in sampled_ids for row in by_item[item_id]]
        grouped: dict[str, list[float]] = defaultdict(list)
        for row in sampled_rows:
            for group_bin in bin_groups(str(row["disagreement_bin"])):
                if group_bin in estimates:
                    grouped[group_bin].append(float(row["value"]))
        for target in targets:
            if grouped[target]:
                estimates[target].append(mean(grouped[target]))
    observed = {
        row["disagreement_bin"]: row["mean"]
        for row in summarize_endpoint(endpoint, rows)
        if row["model_id"] == "all_models"
    }
    out = []
    for target in targets:
        values = sorted(estimates[target])
        if not values:
            continue
        lo = values[int(0.025 * (len(values) - 1))]
        hi = values[int(0.975 * (len(values) - 1))]
        out.append({
            "endpoint": endpoint,
            "disagreement_bin": target,
            "observed_mean": observed.get(target),
            "bootstrap_iterations": len(values),
            "ci_95_low": lo,
            "ci_95_high": hi,
            "bootstrap_one_sided_p_positive": (sum(1 for value in values if value <= 0.0) + 1) / (len(values) + 1),
            "positive": (observed.get(target) or 0.0) > 0,
            "ci_excludes_zero": lo > 0 or hi < 0,
        })
    return out


def bootstrap_contrast_ci(
    endpoint: str,
    rows: list[dict[str, Any]],
    *,
    seed: int,
    iterations: int,
) -> list[dict[str, Any]]:
    rng = random.Random(seed + 313)
    by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_item[str(row["item_id"])].append(row)
    item_ids = sorted(by_item)
    contrasts = [
        ("low_consensus_minus_high_consensus", "low_consensus", "high_consensus"),
        ("diffuse_minus_high_consensus", "diffuse", "high_consensus"),
        ("low_diffuse_minus_high_consensus", "low_diffuse", "high_consensus"),
    ]

    def grouped_means(sampled_rows: list[dict[str, Any]]) -> dict[str, float]:
        grouped: dict[str, list[float]] = defaultdict(list)
        for row in sampled_rows:
            for group_bin in bin_groups(str(row["disagreement_bin"])):
                grouped[group_bin].append(float(row["value"]))
        return {bin_name: mean(values) for bin_name, values in grouped.items() if values}

    observed_means = grouped_means(rows)
    out = []
    for contrast_name, numerator_bin, denominator_bin in contrasts:
        if numerator_bin not in observed_means or denominator_bin not in observed_means:
            continue
        observed = observed_means[numerator_bin] - observed_means[denominator_bin]
        estimates = []
        for _ in range(iterations):
            sampled_ids = [rng.choice(item_ids) for _ in item_ids]
            sampled_rows = [row for item_id in sampled_ids for row in by_item[item_id]]
            means = grouped_means(sampled_rows)
            if numerator_bin in means and denominator_bin in means:
                estimates.append(means[numerator_bin] - means[denominator_bin])
        estimates.sort()
        if not estimates:
            continue
        out.append({
            "endpoint": endpoint,
            "contrast": contrast_name,
            "numerator_bin": numerator_bin,
            "denominator_bin": denominator_bin,
            "observed_difference": observed,
            "bootstrap_iterations": len(estimates),
            "ci_95_low": estimates[int(0.025 * (len(estimates) - 1))],
            "ci_95_high": estimates[int(0.975 * (len(estimates) - 1))],
            "bootstrap_one_sided_p_positive": (sum(1 for value in estimates if value <= 0.0) + 1) / (len(estimates) + 1),
        })
    return out


def holm_adjust(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = [
        row for row in rows
        if row["disagreement_bin"] == "low_consensus"
        and row.get("bootstrap_one_sided_p_positive") is not None
    ]
    ranked = sorted(primary, key=lambda row: float(row["bootstrap_one_sided_p_positive"]))
    adjusted_by_endpoint: dict[str, float] = {}
    running_max = 0.0
    m = len(ranked)
    for index, row in enumerate(ranked):
        adjusted = min(1.0, float(row["bootstrap_one_sided_p_positive"]) * (m - index))
        running_max = max(running_max, adjusted)
        adjusted_by_endpoint[str(row["endpoint"])] = running_max
    out = []
    for row in rows:
        if row["disagreement_bin"] == "low_consensus":
            endpoint = str(row["endpoint"])
            out.append({
                **row,
                "p_value_note": "one-sided positive-effect p estimated from item-cluster bootstrap mass <= 0",
                "holm_adjusted_p": adjusted_by_endpoint.get(endpoint),
            })
    return out


def validity_tables(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_model_mode: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    by_status = Counter()
    flags = Counter()
    for row in rows:
        by_model_mode[(str(row["model_id"]), str(row["prompt_mode"]))]["n"] += 1
        by_model_mode[(str(row["model_id"]), str(row["prompt_mode"]))][str(row.get("validity_status"))] += 1
        by_status[str(row.get("validity_status"))] += 1
        flags["repair_attempted"] += int(row.get("repair_attempted") or 0)
        flags["repair_successful"] += int(row.get("repair_successful") or 0)
        flags["refusal"] += int(row.get("refusal_flag") or 0)
        flags["malformed"] += int(row.get("malformed_flag") or 0)
        flags["off_schema_label"] += int(row.get("off_schema_label_flag") or 0)
    model_mode = []
    for (model_id, prompt_mode), counts in sorted(by_model_mode.items()):
        valid = sum(counts[status] for status in VALID_PRIMARY)
        model_mode.append({
            "model_id": model_id,
            "prompt_mode": prompt_mode,
            "n": counts["n"],
            "valid_primary": valid,
            "valid_primary_rate": valid / counts["n"] if counts["n"] else 0.0,
            "valid_strict_schema": counts["valid_strict_schema"],
            "valid_extracted_json": counts["valid_extracted_json"],
            "invalid_json": counts["invalid_json"],
            "empty_response": counts["empty_response"],
            "probability_out_of_bounds": counts["probability_out_of_bounds"],
            "probability_sum_error": counts["probability_sum_error"],
        })
    status_rows = [{"validity_status": status, "n": n} for status, n in sorted(by_status.items())]
    flag_rows = [{"flag": flag, "n": n} for flag, n in sorted(flags.items())]
    return model_mode, status_rows, flag_rows


def endpoint_sensitivity_exports(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    smoothing_rows = []
    for variant in ("raw_proportion", "jeffreys_alpha_0_5", "laplace_alpha_1"):
        endpoints = endpoint_rows(rows, "primary", source_variant=variant)
        for endpoint_key, endpoint_name in (
            ("h1a", "agreement_surplus"),
            ("h1b", "distribution_agreement_gap"),
            ("h1c", "sampling_compression"),
        ):
            for summary in summarize_endpoint(endpoint_name, endpoints[endpoint_key]):
                if summary["model_id"] == "all_models":
                    smoothing_rows.append({**summary, "source_distribution_variant": variant})

    subset_rows = []
    for subset_name in ("all_items", "high_annotation_q75_ge_14", "exclude_info_majority", "exclude_high_info_ge_0_40"):
        endpoints = endpoint_rows(rows, "primary", source_variant="jeffreys_alpha_0_5", subset_name=subset_name)
        for endpoint_key, endpoint_name in (
            ("h1a", "agreement_surplus"),
            ("h1b", "distribution_agreement_gap"),
            ("h1c", "sampling_compression"),
        ):
            for summary in summarize_endpoint(endpoint_name, endpoints[endpoint_key]):
                if summary["model_id"] == "all_models":
                    subset_rows.append({**summary, "subset": subset_name, "source_distribution_variant": "jeffreys_alpha_0_5"})
    return smoothing_rows, subset_rows


def distribution_diagnostics(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        if row["component_type"] != "core_cross_format" or row["prompt_mode"] != "distribution_mode":
            continue
        if not included_primary(row):
            continue
        model_dist = parsed_distribution(row)
        if model_dist is None:
            continue
        source_dist = source_distribution(row)
        out.append({
            "item_id": row["item_id"],
            "model_id": row["model_id"],
            "disagreement_bin": row["disagreement_bin"],
            "source_entropy": float(row["source_entropy"]),
            "source_entropy_normalized": float(row["source_entropy_normalized"]),
            "model_distribution_entropy": shannon_entropy(model_dist.values()),
            "jsd": jensen_shannon_divergence(source_dist, model_dist),
            "total_variation_distance": total_variation_distance(source_dist, model_dist),
            "brier_majority_label": brier_for_majority_label(model_dist, str(row["source_majority_label"])),
        })
    return out


def summarize_numeric(rows: list[dict[str, Any]], fields: list[str], keys: list[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key) for key in keys)].append(row)
    out = []
    for key_values, values in sorted(grouped.items()):
        record = {key: value for key, value in zip(keys, key_values, strict=True)}
        record["n"] = len(values)
        for field in fields:
            nums = [float(row[field]) for row in values if row.get(field) is not None]
            record[f"mean_{field}"] = mean(nums) if nums else None
        out.append(record)
    return out


def summarize_numeric_with_all_models(rows: list[dict[str, Any]], fields: list[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["disagreement_bin"]), str(row["model_id"]))].append(row)
        grouped[(str(row["disagreement_bin"]), "all_models")].append(row)
    out = []
    for (bin_name, model_id), values in sorted(grouped.items()):
        record = {"disagreement_bin": bin_name, "model_id": model_id, "n": len(values)}
        for field in fields:
            nums = [float(row[field]) for row in values if row.get(field) is not None]
            record[f"mean_{field}"] = mean(nums) if nums else None
        out.append(record)
    return out


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2 or len(xs) != len(ys):
        return None
    mean_x = mean(xs)
    mean_y = mean(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


def distribution_entropy_correlations(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["disagreement_bin"]), str(row["model_id"]))].append(row)
        grouped[(str(row["disagreement_bin"]), "all_models")].append(row)
    out = []
    for (bin_name, model_id), values in sorted(grouped.items()):
        xs = [float(row["source_entropy"]) for row in values]
        ys = [float(row["model_distribution_entropy"]) for row in values]
        out.append({
            "disagreement_bin": bin_name,
            "model_id": model_id,
            "n": len(values),
            "pearson_source_vs_model_distribution_entropy": pearson(xs, ys),
        })
    return out


def normative_certainty(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["component_type"] == "normative_certainty" and row["prompt_mode"] == "normative_verdict_mode":
            if included_primary(row) and row.get("moral_certainty") is not None:
                grouped[(str(row["disagreement_bin"]), str(row["model_id"]))].append(row)
    out = []
    for (bin_name, model_id), values in sorted(grouped.items()):
        out.append({
            "disagreement_bin": bin_name,
            "model_id": model_id,
            "n": len(values),
            "mean_moral_certainty": mean(float(row["moral_certainty"]) for row in values),
            "mean_source_entropy": mean(float(row["source_entropy"]) for row in values),
            "mean_source_majority_support": mean(float(row["source_majority_support"]) for row in values),
        })
    return out


def baseline_distribution_quality(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row["component_type"] == "core_cross_format":
            items.setdefault(str(row["item_id"]), row)
    if not items:
        return []
    uniform = {label: 1.0 / len(LABELS) for label in LABELS}
    global_base = {
        label: mean(float(row[f"source_p_{label}"]) for row in items.values())
        for label in LABELS
    }
    baseline_rows = []
    for item_id, row in sorted(items.items()):
        source_dist = source_distribution(row)
        majority_label = str(row["source_majority_label"])
        majority_oracle = {label: 1.0 if label == majority_label else 0.0 for label in LABELS}
        for baseline_name, baseline_dist in (
            ("uniform", uniform),
            ("global_base_rate", global_base),
            ("source_majority_oracle", majority_oracle),
        ):
            baseline_rows.append({
                "baseline": baseline_name,
                "item_id": item_id,
                "disagreement_bin": row["disagreement_bin"],
                "source_entropy": float(row["source_entropy"]),
                "baseline_entropy": shannon_entropy(baseline_dist.values()),
                "jsd": jensen_shannon_divergence(source_dist, baseline_dist),
                "total_variation_distance": total_variation_distance(source_dist, baseline_dist),
                "brier_majority_label": brier_for_majority_label(baseline_dist, majority_label),
            })
    return summarize_numeric(
        baseline_rows,
        ["source_entropy", "baseline_entropy", "jsd", "total_variation_distance", "brier_majority_label"],
        ["baseline", "disagreement_bin"],
    )


def paraphrase_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    def mode_index(component: str, prompt_mode: str) -> dict[tuple[str, str], dict[str, Any]]:
        return {
            (str(row["item_id"]), str(row["model_id"])): row
            for row in rows
            if row["component_type"] == component
            and row["prompt_mode"] == prompt_mode
            and included_primary(row)
        }

    core_desc = mode_index("core_cross_format", "descriptive_verdict_mode")
    core_dist = mode_index("core_cross_format", "distribution_mode")
    para_desc = mode_index("paraphrase_audit", "paraphrased_descriptive_verdict_mode")
    para_dist = mode_index("paraphrase_audit", "paraphrased_distribution_mode")

    paired = []
    paraphrase_effects = []
    for key, pdesc in sorted(para_desc.items()):
        pdist = para_dist.get(key)
        if pdist is None:
            continue
        label = str(pdesc.get("chosen_label"))
        p_distribution = parsed_distribution(pdist)
        if not label or p_distribution is None or pdesc.get("estimated_source_community_agreement") is None:
            continue
        para_surplus = float(pdesc["estimated_source_community_agreement"]) - source_probability_for_label(pdesc, label)
        para_gap = float(pdesc["estimated_source_community_agreement"]) - p_distribution[label]
        record = {
            "item_id": pdesc["item_id"],
            "model_id": pdesc["model_id"],
            "disagreement_bin": pdesc["disagreement_bin"],
            "paraphrase_chosen_label": label,
            "paraphrase_agreement_surplus": para_surplus,
            "paraphrase_distribution_agreement_gap": para_gap,
        }
        odesc = core_desc.get(key)
        odist = core_dist.get(key)
        if odesc is not None and odist is not None:
            original_label = str(odesc.get("chosen_label"))
            o_distribution = parsed_distribution(odist)
            if original_label and o_distribution is not None and odesc.get("estimated_source_community_agreement") is not None:
                original_surplus = float(odesc["estimated_source_community_agreement"]) - source_probability_for_label(odesc, original_label)
                original_gap = float(odesc["estimated_source_community_agreement"]) - o_distribution[original_label]
                record.update({
                    "original_chosen_label": original_label,
                    "chosen_label_stable": original_label == label,
                    "original_agreement_surplus": original_surplus,
                    "original_distribution_agreement_gap": original_gap,
                    "paraphrase_minus_original_surplus": para_surplus - original_surplus,
                    "paraphrase_minus_original_gap": para_gap - original_gap,
                })
        paired.append(record)

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in paired:
        grouped[(str(row["disagreement_bin"]), str(row["model_id"]))].append(row)
        grouped[(str(row["disagreement_bin"]), "all_models")].append(row)
    for (bin_name, model_id), values in sorted(grouped.items()):
        stable_values = [row for row in values if row.get("chosen_label_stable") is not None]
        paraphrase_effects.append({
            "disagreement_bin": bin_name,
            "model_id": model_id,
            "n": len(values),
            "mean_paraphrase_agreement_surplus": mean(float(row["paraphrase_agreement_surplus"]) for row in values),
            "mean_paraphrase_distribution_agreement_gap": mean(float(row["paraphrase_distribution_agreement_gap"]) for row in values),
            "n_original_matched": len(stable_values),
            "chosen_label_stability_rate": (
                sum(1 for row in stable_values if row.get("chosen_label_stable")) / len(stable_values)
                if stable_values else None
            ),
            "mean_paraphrase_minus_original_surplus": (
                mean(float(row["paraphrase_minus_original_surplus"]) for row in stable_values if row.get("paraphrase_minus_original_surplus") is not None)
                if stable_values else None
            ),
            "mean_paraphrase_minus_original_gap": (
                mean(float(row["paraphrase_minus_original_gap"]) for row in stable_values if row.get("paraphrase_minus_original_gap") is not None)
                if stable_values else None
            ),
        })
    return paired, paraphrase_effects


def paraphrase_bootstrap_ci(
    paired_rows: list[dict[str, Any]],
    *,
    seed: int,
    iterations: int,
) -> list[dict[str, Any]]:
    rng = random.Random(seed + 911)
    endpoints = {
        "paraphrase_agreement_surplus": "paraphrase_agreement_surplus",
        "paraphrase_distribution_agreement_gap": "paraphrase_distribution_agreement_gap",
        "paraphrase_minus_original_surplus": "paraphrase_minus_original_surplus",
        "paraphrase_minus_original_gap": "paraphrase_minus_original_gap",
    }
    by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in paired_rows:
        by_item[str(row["item_id"])].append(row)
    item_ids = sorted(by_item)
    if not item_ids:
        return []
    out = []
    for endpoint, field in endpoints.items():
        for target in ("low_consensus", "diffuse", "low_diffuse", "high_consensus"):
            observed_values = [
                float(row[field])
                for row in paired_rows
                if row.get(field) is not None
                and (row["disagreement_bin"] == target or (target == "low_diffuse" and row["disagreement_bin"] in LOW_DIFFUSE))
            ]
            if not observed_values:
                continue
            estimates = []
            for _ in range(iterations):
                sampled_ids = [rng.choice(item_ids) for _ in item_ids]
                sampled = [row for item_id in sampled_ids for row in by_item[item_id]]
                values = [
                    float(row[field])
                    for row in sampled
                    if row.get(field) is not None
                    and (row["disagreement_bin"] == target or (target == "low_diffuse" and row["disagreement_bin"] in LOW_DIFFUSE))
                ]
                if values:
                    estimates.append(mean(values))
            estimates.sort()
            if not estimates:
                continue
            out.append({
                "endpoint": endpoint,
                "disagreement_bin": target,
                "observed_mean": mean(observed_values),
                "n": len(observed_values),
                "bootstrap_iterations": len(estimates),
                "ci_95_low": estimates[int(0.025 * (len(estimates) - 1))],
                "ci_95_high": estimates[int(0.975 * (len(estimates) - 1))],
            })
    return out


def endpoint_model_ready_rows(endpoint_maps: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for rows in endpoint_maps.values():
        for row in rows:
            out.append({
                "endpoint": row.get("endpoint"),
                "value": row.get("value"),
                "item_id": row.get("item_id"),
                "model_id": row.get("model_id"),
                "provider": row.get("provider"),
                "disagreement_bin": row.get("disagreement_bin"),
                "source_distribution_variant": row.get("source_distribution_variant"),
                "valid_filter": row.get("valid_filter"),
                "subset": row.get("subset"),
                "source_majority_label": row.get("source_majority_label"),
                "source_majority_support": row.get("source_majority_support"),
                "source_majority_margin": row.get("source_majority_margin"),
                "source_entropy": row.get("source_entropy"),
                "source_entropy_normalized": row.get("source_entropy_normalized"),
                "annotation_count": row.get("annotation_count"),
                "n_samples": row.get("n_samples"),
                "model_sample_entropy": row.get("model_sample_entropy"),
                "verdict_agreement": row.get("verdict_agreement"),
                "distribution_probability_for_verdict_label": row.get("distribution_probability_for_verdict_label"),
            })
    return out


def lookup_mean(rows: list[dict[str, Any]], endpoint: str, bin_name: str) -> float | None:
    for row in rows:
        if row["endpoint"] == endpoint and row["disagreement_bin"] == bin_name and row["model_id"] == "all_models":
            return float(row["mean"])
    return None


def lookup_ci(rows: list[dict[str, Any]], endpoint: str, bin_name: str) -> tuple[float | None, float | None]:
    for row in rows:
        if row["endpoint"] == endpoint and row["disagreement_bin"] == bin_name:
            return row.get("ci_95_low"), row.get("ci_95_high")
    return None, None


def manuscript_summary_markdown(
    *,
    run_id: str,
    milestone: str,
    target_ids: int,
    endpoint_summary: list[dict[str, Any]],
    bootstrap: list[dict[str, Any]],
    contrasts: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
    flag_rows: list[dict[str, Any]],
) -> str:
    lines = [
        "# 50k Manuscript Results Summary",
        "",
        f"Run ID: `{run_id}`",
        f"Milestone: `{milestone}`",
        f"Target calls: {target_ids:,}",
        "",
        "This generated summary is derived from the offline 50k exporter. It does not include raw prompt text or raw model-output text.",
        "",
        "## Primary Endpoint Snapshot",
        "",
        "| Endpoint | Bin | Mean | 95% CI |",
        "|---|---|---:|---|",
    ]
    for endpoint in ("agreement_surplus", "distribution_agreement_gap", "sampling_compression"):
        for bin_name in ("low_consensus", "diffuse", "low_diffuse", "high_consensus"):
            value = lookup_mean(endpoint_summary, endpoint, bin_name)
            lo, hi = lookup_ci(bootstrap, endpoint, bin_name)
            value_text = "" if value is None else f"{value:.6f}"
            ci_text = "" if lo is None or hi is None else f"[{float(lo):.6f}, {float(hi):.6f}]"
            lines.append(f"| {endpoint} | {bin_name} | {value_text} | {ci_text} |")
    lines.extend([
        "",
        "## Primary Contrast Snapshot",
        "",
        "| Endpoint | Contrast | Difference | 95% CI |",
        "|---|---|---:|---|",
    ])
    for row in contrasts:
        lines.append(
            "| "
            f"{row['endpoint']} | {row['contrast']} | {float(row['observed_difference']):.6f} | "
            f"[{float(row['ci_95_low']):.6f}, {float(row['ci_95_high']):.6f}] |"
        )
    lines.extend([
        "",
        "## Validity Snapshot",
        "",
        "| Status | N |",
        "|---|---:|",
    ])
    for row in status_rows:
        lines.append(f"| {row['validity_status']} | {row['n']} |")
    lines.extend([
        "",
        "| Flag | N |",
        "|---|---:|",
    ])
    for row in flag_rows:
        lines.append(f"| {row['flag']} | {row['n']} |")
    lines.extend([
        "",
        "## Interpretation Notes",
        "",
        "- Low-consensus and diffuse bins remain positive on agreement surplus, distribution-agreement gap, and sampling compression.",
        "- High-consensus effects are smaller than low/diffuse effects for agreement surplus and sampling compression, matching the main theoretical expectation.",
        "- Distribution-agreement gap is also positive in high-consensus items, so the manuscript should emphasize relative bin differences rather than implying the effect is absent in high-consensus items.",
        "- Paraphrase matched-pair comparisons are available but limited by original/paraphrase overlap; use the paraphrase aggregate and CI tables as the main robustness evidence.",
        "- The formal recognition/contamination audit was not run and should remain a limitation unless new API calls are later approved.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export offline 50k paper analysis artifacts.")
    parser.add_argument("--run-id", default="production_milestones_cumulative_v1")
    parser.add_argument("--milestone", default="50k")
    parser.add_argument("--runs-dir", default="runs")
    parser.add_argument("--out-dir", default="post_run/analysis_exports/50k")
    parser.add_argument("--bootstrap-iterations", type=int, default=2000)
    parser.add_argument("--bootstrap-seed", type=int, default=20260621)
    args = parser.parse_args()

    run_dir = Path(args.runs_dir) / args.run_id
    out_dir = Path(args.out_dir)
    con = sqlite3.connect(run_dir / "study.sqlite")
    con.row_factory = sqlite3.Row
    target_ids = load_target_ids(run_dir, args.milestone)
    prepare_target_table(con, target_ids)
    rows = read_analysis_rows(con)

    write_csv(out_dir / "analysis_rows_50k.csv", derived_rows(rows))

    primary = endpoint_rows(rows, "primary")
    strict = endpoint_rows(rows, "strict")
    endpoint_summary = []
    model_summary = []
    leave_one = []
    bootstrap = []
    contrasts = []
    for endpoint_key, endpoint_name in (("h1a", "agreement_surplus"), ("h1b", "distribution_agreement_gap"), ("h1c", "sampling_compression")):
        endpoint_rows_primary = primary[endpoint_key]
        summary = summarize_endpoint(endpoint_name, endpoint_rows_primary)
        endpoint_summary.extend(row for row in summary if row["model_id"] == "all_models")
        model_summary.extend(row for row in summary if row["model_id"] != "all_models")
        leave_one.extend(leave_one_model_out(endpoint_name, endpoint_rows_primary))
        bootstrap.extend(
            bootstrap_ci(
                endpoint_name,
                endpoint_rows_primary,
                seed=args.bootstrap_seed,
                iterations=args.bootstrap_iterations,
            )
        )
        contrasts.extend(
            bootstrap_contrast_ci(
                endpoint_name,
                endpoint_rows_primary,
                seed=args.bootstrap_seed,
                iterations=args.bootstrap_iterations,
            )
        )

    write_csv(out_dir / "primary_endpoint_table_50k.csv", endpoint_summary)
    write_csv(out_dir / "model_level_endpoint_table_50k.csv", model_summary)
    write_csv(out_dir / "leave_one_model_out_50k.csv", leave_one)
    write_csv(out_dir / "bootstrap_endpoint_ci_50k.csv", bootstrap)
    write_csv(out_dir / "bootstrap_contrast_ci_50k.csv", contrasts)
    write_csv(out_dir / "adjusted_tests_50k.csv", holm_adjust(bootstrap))

    sensitivity_rows = []
    for endpoint_key, endpoint_name in (("h1a", "agreement_surplus"), ("h1b", "distribution_agreement_gap"), ("h1c", "sampling_compression")):
        for valid_filter, endpoint_map in (("primary", primary), ("strict", strict)):
            for row in summarize_endpoint(endpoint_name, endpoint_map[endpoint_key]):
                if row["model_id"] == "all_models":
                    sensitivity_rows.append({**row, "valid_filter": valid_filter})
    write_csv(out_dir / "validity_sensitivity_50k.csv", sensitivity_rows)

    model_mode, status_rows, flag_rows = validity_tables(rows)
    write_csv(out_dir / "validity_by_model_mode_50k.csv", model_mode)
    write_csv(out_dir / "invalid_output_summary_50k.csv", status_rows)
    write_csv(out_dir / "validity_flags_50k.csv", flag_rows)
    smoothing_sensitivity, annotation_info_sensitivity = endpoint_sensitivity_exports(rows)
    write_csv(out_dir / "smoothing_sensitivity_50k.csv", smoothing_sensitivity)
    write_csv(out_dir / "annotation_info_sensitivity_50k.csv", annotation_info_sensitivity)
    dist_diag = distribution_diagnostics(rows)
    write_csv(out_dir / "distribution_diagnostics_50k.csv", dist_diag)
    dist_diag_summary = summarize_numeric(
        dist_diag,
        [
            "source_entropy",
            "source_entropy_normalized",
            "model_distribution_entropy",
            "jsd",
            "total_variation_distance",
            "brier_majority_label",
        ],
        ["disagreement_bin", "model_id"],
    )
    write_csv(
        out_dir / "distribution_diagnostics_summary_50k.csv",
        dist_diag_summary,
    )
    write_csv(out_dir / "distribution_entropy_correlations_50k.csv", distribution_entropy_correlations(dist_diag))
    normative_summary = normative_certainty(rows)
    write_csv(out_dir / "normative_certainty_by_bin_model_50k.csv", normative_summary)
    baseline_summary = baseline_distribution_quality(rows)
    write_csv(out_dir / "baseline_distribution_quality_50k.csv", baseline_summary)
    paired_paraphrase, paraphrase_summary = paraphrase_rows(rows)
    write_csv(out_dir / "paraphrase_original_vs_rewrite_50k.csv", paired_paraphrase)
    write_csv(out_dir / "paraphrase_effects_50k.csv", paraphrase_summary)
    paraphrase_ci = paraphrase_bootstrap_ci(paired_paraphrase, seed=args.bootstrap_seed, iterations=args.bootstrap_iterations)
    write_csv(out_dir / "paraphrase_bootstrap_ci_50k.csv", paraphrase_ci)

    table_dir = out_dir / "manuscript_tables"
    figure_dir = out_dir / "figure_ready"
    model_ready_dir = out_dir / "model_ready"
    ci_by_endpoint_bin = {
        (str(row["endpoint"]), str(row["disagreement_bin"])): row
        for row in bootstrap
    }
    primary_with_ci = []
    for row in endpoint_summary:
        ci = ci_by_endpoint_bin.get((str(row["endpoint"]), str(row["disagreement_bin"])), {})
        primary_with_ci.append({
            **row,
            "ci_95_low": ci.get("ci_95_low"),
            "ci_95_high": ci.get("ci_95_high"),
            "bootstrap_iterations": ci.get("bootstrap_iterations"),
            "bootstrap_one_sided_p_positive": ci.get("bootstrap_one_sided_p_positive"),
        })
    write_csv(table_dir / "table_model_roster_50k.csv", one_row_per_model(rows))
    write_csv(table_dir / "table_component_allocation_50k.csv", component_allocation(rows))
    write_csv(table_dir / "table_primary_results_with_ci_50k.csv", primary_with_ci)
    write_csv(table_dir / "table_primary_contrasts_with_ci_50k.csv", contrasts)
    write_csv(table_dir / "table_adjusted_tests_50k.csv", holm_adjust(bootstrap))
    write_csv(table_dir / "table_validity_by_model_mode_50k.csv", model_mode)
    write_csv(table_dir / "table_invalid_output_summary_50k.csv", status_rows)
    write_csv(table_dir / "table_robustness_smoothing_50k.csv", smoothing_sensitivity)
    write_csv(table_dir / "table_robustness_annotation_info_50k.csv", annotation_info_sensitivity)
    write_csv(table_dir / "table_paraphrase_effects_50k.csv", paraphrase_summary)
    write_csv(table_dir / "table_paraphrase_ci_50k.csv", paraphrase_ci)
    write_csv(table_dir / "table_distribution_quality_50k.csv", summarize_numeric_with_all_models(
        dist_diag,
        ["source_entropy", "model_distribution_entropy", "jsd", "total_variation_distance", "brier_majority_label"],
    ))
    write_csv(table_dir / "table_baseline_distribution_quality_50k.csv", baseline_summary)
    write_csv(table_dir / "table_normative_certainty_50k.csv", normative_summary)
    for endpoint_name, filename in (
        ("agreement_surplus", "figure_agreement_surplus_by_bin_model_50k.csv"),
        ("distribution_agreement_gap", "figure_distribution_gap_by_bin_model_50k.csv"),
        ("sampling_compression", "figure_sampling_compression_by_bin_model_50k.csv"),
    ):
        write_csv(
            figure_dir / filename,
            [row for row in endpoint_summary + model_summary if row["endpoint"] == endpoint_name],
        )
    write_csv(
        figure_dir / "figure_distribution_quality_by_bin_model_50k.csv",
        summarize_numeric_with_all_models(
            dist_diag,
            ["model_distribution_entropy", "jsd", "total_variation_distance", "brier_majority_label"],
        ),
    )
    write_csv(figure_dir / "figure_paraphrase_effects_by_bin_model_50k.csv", paraphrase_summary)
    write_csv(figure_dir / "figure_validity_by_model_mode_50k.csv", model_mode)
    write_csv(model_ready_dir / "mixed_effects_endpoint_rows_50k.csv", endpoint_model_ready_rows(primary))
    write_csv(model_ready_dir / "mixed_effects_endpoint_rows_strict_valid_50k.csv", endpoint_model_ready_rows(strict))
    write_text(
        out_dir / "manuscript_results_summary_50k.md",
        manuscript_summary_markdown(
            run_id=args.run_id,
            milestone=args.milestone,
            target_ids=len(target_ids),
            endpoint_summary=endpoint_summary,
            bootstrap=bootstrap,
            contrasts=contrasts,
            status_rows=status_rows,
            flag_rows=flag_rows,
        ),
    )

    manifest = {
        "run_id": args.run_id,
        "milestone": args.milestone,
        "target_api_call_ids": len(target_ids),
        "analysis_rows": len(rows),
        "out_dir": str(out_dir),
        "bootstrap_iterations": args.bootstrap_iterations,
        "bootstrap_seed": args.bootstrap_seed,
        "artifacts": sorted(path.name for path in out_dir.glob("*.csv")),
        "summaries": sorted(path.name for path in out_dir.glob("*.md")),
        "manuscript_tables": sorted(path.name for path in table_dir.glob("*.csv")),
        "figure_ready": sorted(path.name for path in figure_dir.glob("*.csv")),
        "model_ready": sorted(path.name for path in model_ready_dir.glob("*.csv")),
    }
    write_json(out_dir / "analysis_export_manifest_50k.json", manifest)
    print(json.dumps(manifest, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
