from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


BIN_ORDER = ["high_consensus", "moderate_consensus", "low_consensus", "diffuse", "low_diffuse"]
BIN_LABELS = {
    "high_consensus": "High",
    "moderate_consensus": "Moderate",
    "low_consensus": "Low",
    "diffuse": "Diffuse",
    "low_diffuse": "Low + diffuse",
}
MODEL_MARKERS = ["o", "s", "^", "D", "P", "X"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, Any], key: str) -> float | None:
    value = row.get(key)
    if value in (None, ""):
        return None
    return float(value)


def ordered_bins(rows: list[dict[str, Any]]) -> list[str]:
    present = {str(row["disagreement_bin"]) for row in rows}
    ordered = [bin_name for bin_name in BIN_ORDER if bin_name in present]
    ordered.extend(sorted(present - set(ordered)))
    return ordered


def save(fig: plt.Figure, out_dir: Path, stem: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_dir / f"{stem}.png", dpi=220)
    fig.savefig(out_dir / f"{stem}.svg")
    plt.close(fig)


def plot_endpoint(path: Path, out_dir: Path, stem: str, title: str, ylabel: str) -> None:
    rows = read_csv(path)
    bins = ordered_bins(rows)
    all_rows = {row["disagreement_bin"]: row for row in rows if row["model_id"] == "all_models"}
    model_rows = [row for row in rows if row["model_id"] != "all_models"]
    models = sorted({row["model_id"] for row in model_rows})
    xs = list(range(len(bins)))
    means = [as_float(all_rows.get(bin_name, {}), "mean") or 0.0 for bin_name in bins]

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.bar(xs, means, color="#476A6F", width=0.62, label="All models")
    for model_index, model_id in enumerate(models):
        values = []
        value_xs = []
        by_bin = {row["disagreement_bin"]: row for row in model_rows if row["model_id"] == model_id}
        for index, bin_name in enumerate(bins):
            value = as_float(by_bin.get(bin_name, {}), "mean")
            if value is not None:
                value_xs.append(index + (model_index - (len(models) - 1) / 2) * 0.045)
                values.append(value)
        ax.scatter(
            value_xs,
            values,
            s=34,
            marker=MODEL_MARKERS[model_index % len(MODEL_MARKERS)],
            label=model_id,
            alpha=0.82,
        )
    ax.axhline(0, color="#222222", linewidth=0.8)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(xs, [BIN_LABELS.get(bin_name, bin_name) for bin_name in bins], rotation=18, ha="right")
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=7, ncols=2, frameon=False)
    save(fig, out_dir, stem)


def plot_distribution_quality(path: Path, out_dir: Path) -> None:
    rows = [row for row in read_csv(path) if row["model_id"] == "all_models"]
    bins = ordered_bins(rows)
    by_bin = {row["disagreement_bin"]: row for row in rows}
    xs = list(range(len(bins)))

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.plot(xs, [as_float(by_bin[bin_name], "mean_jsd") for bin_name in bins], marker="o", label="JSD")
    ax.plot(
        xs,
        [as_float(by_bin[bin_name], "mean_total_variation_distance") for bin_name in bins],
        marker="s",
        label="Total variation",
    )
    ax.set_title("Distribution-Mode Alignment Diagnostics")
    ax.set_ylabel("Distance from source distribution")
    ax.set_xticks(xs, [BIN_LABELS.get(bin_name, bin_name) for bin_name in bins], rotation=18, ha="right")
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    save(fig, out_dir, "figure_distribution_quality_distances_50k")


def plot_paraphrase(path: Path, out_dir: Path) -> None:
    rows = [row for row in read_csv(path) if row["model_id"] == "all_models"]
    bins = ordered_bins(rows)
    by_bin = {row["disagreement_bin"]: row for row in rows}
    xs = list(range(len(bins)))
    width = 0.34

    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    ax.bar(
        [x - width / 2 for x in xs],
        [as_float(by_bin[bin_name], "mean_paraphrase_agreement_surplus") or 0.0 for bin_name in bins],
        width=width,
        label="Agreement surplus",
        color="#476A6F",
    )
    ax.bar(
        [x + width / 2 for x in xs],
        [as_float(by_bin[bin_name], "mean_paraphrase_distribution_agreement_gap") or 0.0 for bin_name in bins],
        width=width,
        label="Distribution gap",
        color="#C17C5B",
    )
    ax.axhline(0, color="#222222", linewidth=0.8)
    ax.set_title("Paraphrase Audit Effects")
    ax.set_ylabel("Mean effect")
    ax.set_xticks(xs, [BIN_LABELS.get(bin_name, bin_name) for bin_name in bins], rotation=18, ha="right")
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    save(fig, out_dir, "figure_paraphrase_audit_effects_50k")


def plot_validity(path: Path, out_dir: Path) -> None:
    rows = read_csv(path)
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(row["model_id"], []).append(float(row["valid_primary_rate"]))
    models = sorted(grouped)
    rates = [sum(grouped[model]) / len(grouped[model]) for model in models]

    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.bar(range(len(models)), rates, color="#476A6F", width=0.62)
    ax.set_ylim(0.94, 1.002)
    ax.set_title("Primary-Validity Rate by Model")
    ax.set_ylabel("Mean valid rate across prompt modes")
    ax.set_xticks(range(len(models)), models, rotation=20, ha="right")
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, out_dir, "figure_validity_rate_by_model_50k")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render final 50k manuscript figures from figure-ready CSVs.")
    parser.add_argument("--in-dir", default="post_run/analysis_exports/50k/figure_ready")
    parser.add_argument("--out-dir", default="post_run/analysis_exports/50k/rendered_figures")
    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    plot_endpoint(
        in_dir / "figure_agreement_surplus_by_bin_model_50k.csv",
        out_dir,
        "figure_agreement_surplus_by_bin_model_50k",
        "Agreement Surplus by Disagreement Bin",
        "Mean agreement surplus",
    )
    plot_endpoint(
        in_dir / "figure_distribution_gap_by_bin_model_50k.csv",
        out_dir,
        "figure_distribution_gap_by_bin_model_50k",
        "Distribution-Agreement Gap by Disagreement Bin",
        "Mean distribution-agreement gap",
    )
    plot_endpoint(
        in_dir / "figure_sampling_compression_by_bin_model_50k.csv",
        out_dir,
        "figure_sampling_compression_by_bin_model_50k",
        "Sampling Compression by Disagreement Bin",
        "Source entropy minus sample entropy",
    )
    plot_distribution_quality(in_dir / "figure_distribution_quality_by_bin_model_50k.csv", out_dir)
    plot_paraphrase(in_dir / "figure_paraphrase_effects_by_bin_model_50k.csv", out_dir)
    plot_validity(in_dir / "figure_validity_by_model_mode_50k.csv", out_dir)
    print(f"rendered figures: {out_dir}")


if __name__ == "__main__":
    main()
