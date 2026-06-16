from __future__ import annotations

from dataclasses import dataclass

LABELS: tuple[str, ...] = ("author", "other", "everybody", "nobody", "info")

LABEL_DEFINITIONS: dict[str, str] = {
    "author": "the author / narrator was in the wrong",
    "other": "the other party was in the wrong",
    "everybody": "everybody / both sides were in the wrong",
    "nobody": "nobody was in the wrong",
    "info": "not enough information / cannot tell",
}


@dataclass(frozen=True)
class LabelSchema:
    version: str
    labels: tuple[str, ...]
    definitions: dict[str, str]


CANONICAL_SCHEMA = LabelSchema("scruples_five_label_v1", LABELS, LABEL_DEFINITIONS)


def require_label(label: str) -> str:
    normalized = label.strip().lower()
    if normalized not in LABELS:
        raise ValueError(f"unknown label {label!r}; expected one of {LABELS}")
    return normalized


def empty_distribution(value: float = 0.0) -> dict[str, float]:
    return {label: float(value) for label in LABELS}

