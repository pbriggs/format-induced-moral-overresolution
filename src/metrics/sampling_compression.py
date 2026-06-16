from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping

from protocol.label_schema import LABELS
from source_uncertainty.smoothing import shannon_entropy


def sample_label_distribution(labels: Iterable[str]) -> dict[str, float]:
    counts = Counter(labels)
    total = sum(counts.values())
    if total == 0:
        raise ValueError("at least one sampled label is required")
    unknown = set(counts) - set(LABELS)
    if unknown:
        raise ValueError(f"unknown sampled labels: {sorted(unknown)}")
    return {label: counts[label] / total for label in LABELS}


def sampling_compression(source_distribution: Mapping[str, float], sampled_labels: Iterable[str]) -> float:
    return shannon_entropy(source_distribution.values()) - shannon_entropy(sample_label_distribution(sampled_labels).values())

