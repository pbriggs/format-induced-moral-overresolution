from __future__ import annotations

from collections.abc import Mapping


def source_support_for_label(source_distribution: Mapping[str, float], chosen_label: str) -> float:
    try:
        return float(source_distribution[chosen_label])
    except KeyError as exc:
        raise ValueError(f"source distribution is missing chosen label {chosen_label!r}") from exc


def agreement_surplus(
    estimated_source_community_agreement: float,
    source_distribution: Mapping[str, float],
    chosen_label: str,
) -> float:
    return float(estimated_source_community_agreement) - source_support_for_label(source_distribution, chosen_label)


def normative_certainty_surplus(
    moral_certainty: float,
    source_distribution: Mapping[str, float],
    chosen_label: str,
) -> float:
    return float(moral_certainty) - source_support_for_label(source_distribution, chosen_label)

