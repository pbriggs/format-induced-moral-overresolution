from __future__ import annotations


def disagreement_bin(majority_support: float) -> str:
    if not 0.0 <= majority_support <= 1.0:
        raise ValueError("majority_support must be in [0, 1]")
    if majority_support >= 0.80:
        return "high_consensus"
    if majority_support >= 0.65:
        return "moderate_consensus"
    if majority_support >= 0.50:
        return "low_consensus"
    return "diffuse"

