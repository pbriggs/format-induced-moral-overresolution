from __future__ import annotations

from collections.abc import Mapping, Sequence

from source_uncertainty.smoothing import shannon_entropy


def entropy(distribution: Mapping[str, float] | Sequence[float]) -> float:
    return shannon_entropy(distribution)


def entropy_compression(source_distribution: Mapping[str, float], model_distribution: Mapping[str, float]) -> float:
    return entropy(source_distribution) - entropy(model_distribution)

