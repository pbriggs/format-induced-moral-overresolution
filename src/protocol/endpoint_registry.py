from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoint:
    name: str
    formula: str
    confirmatory: bool
    primary_subset: str


PRIMARY_ENDPOINTS: tuple[Endpoint, ...] = (
    Endpoint(
        "agreement_surplus",
        "model_estimated_source_community_agreement - source_support_for_model_chosen_label",
        True,
        "low_consensus",
    ),
    Endpoint(
        "distribution_agreement_gap",
        "verdict_mode_estimated_agreement - distribution_mode_probability_for_verdict_label",
        True,
        "low_consensus",
    ),
    Endpoint(
        "sampling_compression",
        "source_community_entropy - repeated_sample_model_entropy",
        True,
        "low_consensus",
    ),
)

SECONDARY_ENDPOINTS: tuple[str, ...] = (
    "jensen_shannon_divergence",
    "total_variation_distance",
    "brier_score_majority_label",
    "entropy_compression",
    "normative_certainty_surplus",
    "distribution_certainty_gap",
    "malformed_refusal_rate",
    "paraphrase_robustness",
    "recognition_contamination_indicator",
)

