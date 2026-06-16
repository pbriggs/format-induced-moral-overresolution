from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping

from protocol.call_milestones import CallMilestone, MilestoneDecision, get_call_milestone


def validity_rates(rows: Iterable[Mapping[str, object]]) -> dict[tuple[str, str], dict[str, float]]:
    counts: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        key = (str(row["model_id"]), str(row["prompt_mode"]))
        counts[key]["total"] += 1
        status = str(row["validity_status"])
        if status in {"valid_strict_schema", "valid_after_repair", "valid_extracted_json"}:
            counts[key]["valid_primary"] += 1
        if bool(row.get("refusal_flag", False)):
            counts[key]["refusal"] += 1
        if bool(row.get("malformed_flag", False)):
            counts[key]["malformed"] += 1
    rates: dict[tuple[str, str], dict[str, float]] = {}
    for key, values in counts.items():
        total = values["total"]
        rates[key] = {
            "valid_primary_rate": values["valid_primary"] / total,
            "refusal_rate": values["refusal"] / total,
            "malformed_rate": values["malformed"] / total,
            "n": float(total),
        }
    return rates


def overall_validity_rate(rates: Mapping[tuple[str, str], Mapping[str, float]]) -> float:
    valid = 0.0
    total = 0.0
    for value in rates.values():
        n = float(value["n"])
        valid += float(value["valid_primary_rate"]) * n
        total += n
    return valid / total if total else 0.0


def go_no_go(rates: Mapping[tuple[str, str], Mapping[str, float]], min_valid_primary_rate: float = 0.95) -> dict[str, object]:
    failing = [
        {"model_id": key[0], "prompt_mode": key[1], "valid_primary_rate": value["valid_primary_rate"]}
        for key, value in rates.items()
        if value["valid_primary_rate"] < min_valid_primary_rate
    ]
    return {"proceed": not failing, "failing_validity_cells": failing}


def milestone_validity_check(
    rows: Iterable[Mapping[str, object]],
    milestone: str | CallMilestone,
) -> dict[str, object]:
    resolved = get_call_milestone(milestone) if isinstance(milestone, str) else milestone
    rates = validity_rates(rows)
    thresholds = resolved.continue_thresholds
    min_cell_rate = thresholds.per_model_mode_validity_min or thresholds.overall_validity_min
    cell_check = go_no_go(rates, min_valid_primary_rate=min_cell_rate)
    overall_rate = overall_validity_rate(rates)
    return {
        "milestone": resolved.name,
        "overall_validity_rate": overall_rate,
        "overall_validity_threshold": thresholds.overall_validity_min,
        "per_model_mode_validity_threshold": min_cell_rate,
        "validity_rates": rates,
        "proceed": bool(cell_check["proceed"]) and overall_rate >= thresholds.overall_validity_min,
        "failing_validity_cells": cell_check["failing_validity_cells"],
    }


def evaluate_milestone_alignment(
    milestone: str | CallMilestone,
    observed: Mapping[str, object],
) -> dict[str, object]:
    resolved = get_call_milestone(milestone) if isinstance(milestone, str) else milestone
    thresholds = resolved.continue_thresholds
    failures: list[str] = []
    revisions: list[str] = []

    def number(name: str) -> float | None:
        value = observed.get(name)
        return None if value is None else float(value)

    def integer(name: str) -> int | None:
        value = observed.get(name)
        return None if value is None else int(value)

    overall_rate = number("overall_validity_rate")
    if overall_rate is not None and overall_rate < thresholds.overall_validity_min:
        failures.append("JSON validity is below the milestone threshold")

    min_cell_rate = number("min_model_mode_validity_rate")
    if (
        thresholds.per_model_mode_validity_min is not None
        and min_cell_rate is not None
        and min_cell_rate < thresholds.per_model_mode_validity_min
    ):
        failures.append("at least one model/mode validity cell is below threshold")

    if observed.get("distribution_outputs_item_sensitive") is False:
        failures.append("distribution mode is not item-sensitive")
    if observed.get("agreement_estimates_interpretable") is False:
        failures.append("verdict/agreement mode is not producing interpretable agreement estimates")

    positive_gap_models = integer("positive_gap_models")
    if (
        thresholds.positive_gap_models_min is not None
        and positive_gap_models is not None
        and positive_gap_models < thresholds.positive_gap_models_min
    ):
        failures.append("too few models show a positive distribution-agreement gap")

    positive_surplus_models = integer("positive_surplus_models")
    if (
        thresholds.positive_surplus_models_min is not None
        and positive_surplus_models is not None
        and positive_surplus_models < thresholds.positive_surplus_models_min
    ):
        failures.append("too few models show a positive agreement surplus")

    low_diffuse_gap = number("low_diffuse_distribution_agreement_gap_mean")
    if thresholds.low_diffuse_gap_min is not None and low_diffuse_gap is not None:
        if low_diffuse_gap < 0:
            failures.append("low-consensus/diffuse distribution-agreement gap is negative")
        elif low_diffuse_gap < thresholds.low_diffuse_gap_min:
            revisions.append("low-consensus/diffuse distribution-agreement gap is positive but below the continue threshold")

    low_diffuse_surplus = number("low_diffuse_agreement_surplus_mean")
    if thresholds.low_diffuse_surplus_min is not None and low_diffuse_surplus is not None:
        if low_diffuse_surplus < 0:
            failures.append("low-consensus/diffuse agreement surplus is negative")
        elif low_diffuse_surplus < thresholds.low_diffuse_surplus_min:
            revisions.append("low-consensus/diffuse agreement surplus is positive but below the continue threshold")

    if thresholds.require_low_diffuse_gt_high_consensus:
        high_gap = number("high_consensus_distribution_agreement_gap_mean")
        if low_diffuse_gap is not None and high_gap is not None and low_diffuse_gap <= high_gap:
            failures.append("contested-item gap is not larger than the high-consensus gap")

    positive_sampling_models = integer("positive_sampling_compression_models")
    if (
        thresholds.positive_sampling_models_min is not None
        and positive_sampling_models is not None
        and positive_sampling_models < thresholds.positive_sampling_models_min
    ):
        revisions.append("repeated sampling is weaker than the milestone target")

    if thresholds.require_paraphrase_preserves_direction and observed.get("paraphrase_preserves_direction") is False:
        failures.append("paraphrased items reverse or undermine the main effect direction")

    if failures:
        decision = MilestoneDecision.STOP
    elif revisions:
        decision = MilestoneDecision.REVISE
    else:
        decision = MilestoneDecision.CONTINUE

    return {
        "milestone": resolved.name,
        "decision": decision.value,
        "failures": failures,
        "revision_reasons": revisions,
        "observed": dict(observed),
    }
