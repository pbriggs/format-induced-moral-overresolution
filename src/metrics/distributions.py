from __future__ import annotations

import math
from collections.abc import Mapping

from protocol.label_schema import LABELS


def align_distribution(distribution: Mapping[str, float]) -> list[float]:
    values = [float(distribution[label]) for label in LABELS]
    if any(value < 0 for value in values):
        raise ValueError("probabilities must be non-negative")
    total = sum(values)
    if total <= 0:
        raise ValueError("distribution must have positive mass")
    return [value / total for value in values]


def total_variation_distance(p: Mapping[str, float], q: Mapping[str, float]) -> float:
    pv = align_distribution(p)
    qv = align_distribution(q)
    return 0.5 * sum(abs(a - b) for a, b in zip(pv, qv, strict=True))


def kl_divergence(p_values: list[float], q_values: list[float]) -> float:
    total = 0.0
    for p, q in zip(p_values, q_values, strict=True):
        if p:
            if q <= 0:
                return math.inf
            total += p * math.log2(p / q)
    return total


def jensen_shannon_divergence(p: Mapping[str, float], q: Mapping[str, float]) -> float:
    pv = align_distribution(p)
    qv = align_distribution(q)
    midpoint = [(a + b) / 2 for a, b in zip(pv, qv, strict=True)]
    return 0.5 * kl_divergence(pv, midpoint) + 0.5 * kl_divergence(qv, midpoint)


def brier_for_majority_label(model_distribution: Mapping[str, float], majority_label: str) -> float:
    pv = align_distribution(model_distribution)
    target = [1.0 if label == majority_label else 0.0 for label in LABELS]
    return sum((p - t) ** 2 for p, t in zip(pv, target, strict=True)) / len(LABELS)

