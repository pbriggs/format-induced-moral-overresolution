from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import math

from protocol.disagreement_bins import disagreement_bin
from protocol.label_schema import LABELS


@dataclass(frozen=True)
class SourceDistribution:
    probabilities: dict[str, float]
    majority_label: str
    majority_support: float
    majority_margin: float
    entropy: float
    entropy_normalized: float
    disagreement_bin: str
    annotation_count: int
    smoothing_method: str
    alpha: float


def dirichlet_smooth_counts(
    counts: Mapping[str, int | float],
    alpha: float = 0.5,
    method: str = "dirichlet",
) -> SourceDistribution:
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    raw = {label: float(counts.get(label, 0.0)) for label in LABELS}
    if any(value < 0 for value in raw.values()):
        raise ValueError("counts must be non-negative")
    annotation_count = int(sum(raw.values()))
    denominator = sum(raw.values()) + alpha * len(LABELS)
    if denominator <= 0:
        raise ValueError("at least one count or positive alpha is required")
    probabilities = {label: (raw[label] + alpha) / denominator for label in LABELS}
    ranked = sorted(probabilities.items(), key=lambda kv: (-kv[1], kv[0]))
    majority_label, majority_support = ranked[0]
    majority_margin = majority_support - ranked[1][1]
    entropy = shannon_entropy(probabilities.values())
    entropy_normalized = entropy / math.log2(len(LABELS))
    return SourceDistribution(
        probabilities=probabilities,
        majority_label=majority_label,
        majority_support=majority_support,
        majority_margin=majority_margin,
        entropy=entropy,
        entropy_normalized=entropy_normalized,
        disagreement_bin=disagreement_bin(majority_support),
        annotation_count=annotation_count,
        smoothing_method=method,
        alpha=alpha,
    )


def shannon_entropy(probabilities: object) -> float:
    values = probabilities.values() if isinstance(probabilities, dict) else probabilities
    entropy = 0.0
    for p in values:
        p = float(p)
        if p < 0:
            raise ValueError("probabilities must be non-negative")
        if p:
            entropy -= p * math.log2(p)
    return entropy

