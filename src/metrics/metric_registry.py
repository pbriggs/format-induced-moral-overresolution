from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricSpec:
    name: str
    direction: str
    confirmatory: bool


METRIC_REGISTRY: tuple[MetricSpec, ...] = (
    MetricSpec("agreement_surplus", "positive means estimated agreement exceeds source support", True),
    MetricSpec("distribution_agreement_gap", "positive means verdict agreement exceeds distribution probability", True),
    MetricSpec("sampling_compression", "positive means repeated samples are lower entropy than source", True),
    MetricSpec("jensen_shannon_divergence", "larger means worse distributional alignment", False),
    MetricSpec("total_variation_distance", "larger means worse distributional alignment", False),
    MetricSpec("brier_score_majority_label", "larger means worse majority-label probability score", False),
    MetricSpec("entropy_compression", "positive means model distribution is sharper than source", False),
    MetricSpec("normative_certainty_surplus", "positive means moral certainty exceeds source support", False),
    MetricSpec("distribution_certainty_gap", "positive means moral certainty exceeds distribution probability", False),
)


def metric_names() -> tuple[str, ...]:
    return tuple(metric.name for metric in METRIC_REGISTRY)

