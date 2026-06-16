from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from protocol.label_schema import LABELS


@dataclass(frozen=True)
class BaselineOutput:
    model_id: str
    baseline_type: str
    label_probabilities: dict[str, float]
    most_likely_label: str


def _majority_label(distribution: Mapping[str, float]) -> str:
    return sorted(distribution.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def uniform_baseline(model_id: str = "baseline_uniform") -> BaselineOutput:
    probs = {label: 1.0 / len(LABELS) for label in LABELS}
    return BaselineOutput(model_id, "uniform", probs, "author")


def global_base_rate(distributions: Iterable[Mapping[str, float]], model_id: str = "baseline_global_base_rate") -> BaselineOutput:
    totals = {label: 0.0 for label in LABELS}
    n = 0
    for distribution in distributions:
        n += 1
        for label in LABELS:
            totals[label] += float(distribution[label])
    if n == 0:
        raise ValueError("at least one distribution is required")
    probs = {label: totals[label] / n for label in LABELS}
    return BaselineOutput(model_id, "global_base_rate", probs, _majority_label(probs))


def majority_only_oracle(source_distribution: Mapping[str, float], model_id: str = "baseline_majority_oracle") -> BaselineOutput:
    label = _majority_label(source_distribution)
    probs = {candidate: 1.0 if candidate == label else 0.0 for candidate in LABELS}
    return BaselineOutput(model_id, "majority_only_oracle", probs, label)


def entropy_matched_oracle(source_distribution: Mapping[str, float], model_id: str = "baseline_entropy_matched_oracle") -> BaselineOutput:
    # Conservative v1: preserve the full source distribution while declaring the majority label.
    probs = {label: float(source_distribution[label]) for label in LABELS}
    return BaselineOutput(model_id, "entropy_matched_oracle", probs, _majority_label(probs))

