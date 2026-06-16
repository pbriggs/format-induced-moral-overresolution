from __future__ import annotations

from collections.abc import Mapping
import random

from protocol.label_schema import LABELS


def dirichlet_posterior_draws(
    counts: Mapping[str, int | float],
    alpha: float = 0.5,
    n_draws: int = 1000,
    seed: int | None = None,
) -> list[dict[str, float]]:
    if n_draws < 1:
        raise ValueError("n_draws must be positive")
    rng = random.Random(seed)
    parameters = [float(counts.get(label, 0.0)) + alpha for label in LABELS]
    if any(value <= 0 for value in parameters):
        raise ValueError("all Dirichlet parameters must be positive")
    draws: list[dict[str, float]] = []
    for _ in range(n_draws):
        samples = [rng.gammavariate(param, 1.0) for param in parameters]
        total = sum(samples)
        draws.append({label: sample / total for label, sample in zip(LABELS, samples, strict=True)})
    return draws

