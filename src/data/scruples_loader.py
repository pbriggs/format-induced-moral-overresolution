from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from data.source_votes import SourceVotes, normalize_label_scores
from protocol.label_schema import CANONICAL_SCHEMA, LABELS
from source_uncertainty.smoothing import SourceDistribution, dirichlet_smooth_counts

DEFAULT_SCRUPLES_ANECDOTES_DIR = Path("data/scruples/anecdotes")
SPLIT_FILES = {
    "train": "train.scruples-anecdotes.jsonl",
    "dev": "dev.scruples-anecdotes.jsonl",
    "test": "test.scruples-anecdotes.jsonl",
}


@dataclass(frozen=True)
class ScruplesAnecdote:
    item_id: str
    dataset_id: str
    source_item_id: str
    post_id: str | None
    title: str
    text: str
    post_type: str
    split: str
    label_scores: dict[str, int]
    majority_label: str
    raw: dict[str, Any]

    @property
    def item_text(self) -> str:
        if self.title.strip():
            return f"{self.title.strip()}\n\n{self.text.strip()}"
        return self.text.strip()

    @property
    def annotation_count(self) -> int:
        return sum(self.label_scores.values())

    def source_votes(self) -> SourceVotes:
        return SourceVotes(self.item_id, self.dataset_id, self.label_scores)


@dataclass(frozen=True)
class ScruplesAnalysisRow:
    item_id: str
    dataset_id: str
    split: str
    source_item_id: str
    post_id: str | None
    item_text: str
    source_distribution_version: str
    source_p_author: float
    source_p_other: float
    source_p_everybody: float
    source_p_nobody: float
    source_p_info: float
    source_majority_label: str
    source_majority_support: float
    source_majority_margin: float
    source_entropy: float
    source_entropy_normalized: float
    annotation_count: int
    disagreement_bin: str
    item_length_chars: int
    canonical_label_schema_version: str

    def source_distribution(self) -> dict[str, float]:
        return {
            "author": self.source_p_author,
            "other": self.source_p_other,
            "everybody": self.source_p_everybody,
            "nobody": self.source_p_nobody,
            "info": self.source_p_info,
        }


def available_splits(root: str | Path = DEFAULT_SCRUPLES_ANECDOTES_DIR) -> list[str]:
    root = Path(root)
    return [split for split, filename in SPLIT_FILES.items() if (root / filename).exists()]


def iter_scruples_anecdotes(
    root: str | Path = DEFAULT_SCRUPLES_ANECDOTES_DIR,
    splits: Iterable[str] | None = None,
) -> Iterator[ScruplesAnecdote]:
    root = Path(root)
    selected_splits = list(splits) if splits is not None else list(SPLIT_FILES)
    for split in selected_splits:
        if split not in SPLIT_FILES:
            raise ValueError(f"unknown SCRUPLES split {split!r}; expected one of {tuple(SPLIT_FILES)}")
        path = root / SPLIT_FILES[split]
        if not path.exists():
            raise FileNotFoundError(f"SCRUPLES split file not found: {path}")
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                raw = json.loads(line)
                yield parse_scruples_record(raw, split=split, line_number=line_number)


def load_scruples_anecdotes(
    root: str | Path = DEFAULT_SCRUPLES_ANECDOTES_DIR,
    splits: Iterable[str] | None = None,
) -> list[ScruplesAnecdote]:
    return list(iter_scruples_anecdotes(root=root, splits=splits))


def parse_scruples_record(raw: Mapping[str, Any], split: str, line_number: int | None = None) -> ScruplesAnecdote:
    label_scores = normalize_label_scores(raw["label_scores"])
    majority_label = str(raw["label"]).strip().lower()
    if majority_label not in LABELS:
        location = f" at line {line_number}" if line_number is not None else ""
        raise ValueError(f"unknown SCRUPLES majority label {raw['label']!r}{location}")
    item_id = f"scruples_anecdotes::{split}::{raw['id']}"
    return ScruplesAnecdote(
        item_id=item_id,
        dataset_id="scruples_anecdotes_v1",
        source_item_id=str(raw["id"]),
        post_id=raw.get("post_id"),
        title=str(raw.get("title") or ""),
        text=str(raw.get("text") or ""),
        post_type=str(raw.get("post_type") or ""),
        split=split,
        label_scores=label_scores,
        majority_label=majority_label,
        raw=dict(raw),
    )


def analysis_rows(
    anecdotes: Iterable[ScruplesAnecdote],
    alpha: float = 0.5,
    source_distribution_version: str | None = None,
) -> Iterator[ScruplesAnalysisRow]:
    version = source_distribution_version or f"dirichlet_alpha_{alpha:g}_scruples_anecdotes_v1"
    for anecdote in anecdotes:
        source_distribution = dirichlet_smooth_counts(anecdote.label_scores, alpha=alpha)
        yield make_analysis_row(anecdote, source_distribution, version)


def make_analysis_row(
    anecdote: ScruplesAnecdote,
    source_distribution: SourceDistribution,
    source_distribution_version: str,
) -> ScruplesAnalysisRow:
    probs = source_distribution.probabilities
    return ScruplesAnalysisRow(
        item_id=anecdote.item_id,
        dataset_id=anecdote.dataset_id,
        split=anecdote.split,
        source_item_id=anecdote.source_item_id,
        post_id=anecdote.post_id,
        item_text=anecdote.item_text,
        source_distribution_version=source_distribution_version,
        source_p_author=probs["author"],
        source_p_other=probs["other"],
        source_p_everybody=probs["everybody"],
        source_p_nobody=probs["nobody"],
        source_p_info=probs["info"],
        source_majority_label=source_distribution.majority_label,
        source_majority_support=source_distribution.majority_support,
        source_majority_margin=source_distribution.majority_margin,
        source_entropy=source_distribution.entropy,
        source_entropy_normalized=source_distribution.entropy_normalized,
        annotation_count=source_distribution.annotation_count,
        disagreement_bin=source_distribution.disagreement_bin,
        item_length_chars=len(anecdote.item_text),
        canonical_label_schema_version=CANONICAL_SCHEMA.version,
    )
