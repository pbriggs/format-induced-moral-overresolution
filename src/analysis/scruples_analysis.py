from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import asdict
import csv
from pathlib import Path

from data.scruples_loader import ScruplesAnalysisRow, analysis_rows, iter_scruples_anecdotes
from models.baselines.predictors import BaselineOutput, global_base_rate


def load_source_analysis_rows(
    root: str | Path = "data/scruples/anecdotes",
    splits: Iterable[str] | None = None,
    alpha: float = 0.5,
) -> list[ScruplesAnalysisRow]:
    return list(analysis_rows(iter_scruples_anecdotes(root=root, splits=splits), alpha=alpha))


def summarize_source_rows(rows: Iterable[ScruplesAnalysisRow]) -> dict[str, object]:
    rows = list(rows)
    split_counts = Counter(row.split for row in rows)
    bin_counts = Counter(row.disagreement_bin for row in rows)
    label_counts = Counter(row.source_majority_label for row in rows)
    annotation_counts = [row.annotation_count for row in rows]
    return {
        "n_items": len(rows),
        "split_counts": dict(sorted(split_counts.items())),
        "disagreement_bin_counts": dict(sorted(bin_counts.items())),
        "source_majority_label_counts": dict(sorted(label_counts.items())),
        "mean_annotation_count": sum(annotation_counts) / len(annotation_counts) if annotation_counts else 0.0,
    }


def global_source_baseline(rows: Iterable[ScruplesAnalysisRow]) -> BaselineOutput:
    return global_base_rate(row.source_distribution() for row in rows)


def write_source_analysis_csv(rows: Iterable[ScruplesAnalysisRow], path: str | Path) -> None:
    rows = list(rows)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys()) if rows else list(ScruplesAnalysisRow.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def grouped_mean_entropy(rows: Iterable[ScruplesAnalysisRow], group_field: str = "disagreement_bin") -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        key = str(getattr(row, group_field))
        totals[key] += row.source_entropy
        counts[key] += 1
    return {key: totals[key] / counts[key] for key in sorted(counts)}

