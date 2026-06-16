from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from protocol.label_schema import LABELS


@dataclass(frozen=True)
class SourceVotes:
    item_id: str
    dataset_id: str
    counts: dict[str, int]
    source_vote_version: str = "scruples_anecdotes_v1"

    @property
    def annotation_count(self) -> int:
        return sum(self.counts.values())


def normalize_label_scores(label_scores: Mapping[str, int | float]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for label in LABELS:
        raw_value = label_scores.get(label.upper(), label_scores.get(label, 0))
        value = int(raw_value)
        if value < 0:
            raise ValueError(f"negative source vote count for {label}")
        counts[label] = value
    return counts

