from __future__ import annotations

from collections.abc import Mapping


def distribution_agreement_gap(
    verdict_mode_estimated_agreement: float,
    distribution_mode_probabilities: Mapping[str, float],
    verdict_label: str,
) -> float:
    return float(verdict_mode_estimated_agreement) - float(distribution_mode_probabilities[verdict_label])


def distribution_certainty_gap(
    verdict_mode_moral_certainty: float,
    distribution_mode_probabilities: Mapping[str, float],
    verdict_label: str,
) -> float:
    return float(verdict_mode_moral_certainty) - float(distribution_mode_probabilities[verdict_label])

