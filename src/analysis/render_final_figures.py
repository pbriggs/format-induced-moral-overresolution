from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.transforms import Bbox


BIN_ORDER = ["high_consensus", "moderate_consensus", "low_consensus", "diffuse", "low_diffuse"]
BIN_LABELS = {
    "high_consensus": "High",
    "moderate_consensus": "Moderate",
    "low_consensus": "Low",
    "diffuse": "Diffuse",
    "low_diffuse": "Low + diffuse",
}
MODEL_MARKERS = ["o", "s", "^", "D", "P", "X"]
MODEL_COLORS = ["#4F7895", "#B07C64", "#6F956B", "#9A7893", "#7C8494", "#8C765B"]
QUANT_STYLE = {
    "background": "#FFFFFF",
    "bar": "#5F7D80",
    "bar_light": "#DCE6E5",
    "ci": "#2F383A",
    "grid": "#E6E8E8",
    "spine": "#8A9395",
    "ink": "#172124",
    "muted": "#596466",
    "support_blue": "#5A86A9",
    "support_orange": "#C58A66",
}
PALETTE = {
    "source": "#DCEDEA",
    "mode": "#F3EBD8",
    "endpoint": "#E5E7F4",
    "endpoint_focus": "#DDEFE8",
    "support": "#EEEEEE",
    "ink": "#172124",
    "muted": "#536064",
    "bar": "#476A6F",
    "orange": "#C17C5B",
    "blue": "#4D6B9A",
}


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
    if not fig.get_constrained_layout():
        fig.tight_layout()
    fig.savefig(out_dir / f"{stem}.png", dpi=300)
    fig.savefig(out_dir / f"{stem}.svg")
    fig.savefig(out_dir / f"{stem}.pdf")
    plt.close(fig)


def format_bin_label(bin_name: str) -> str:
    label = BIN_LABELS.get(bin_name, bin_name)
    return "Low +\ndiffuse" if label == "Low + diffuse" else label


def style_quant_ax(ax: Axes, *, title: str, ylabel: str, title_size: float = 9.3) -> None:
    ax.set_title(title, fontsize=title_size, fontweight="regular", color=QUANT_STYLE["ink"], pad=10)
    ax.set_ylabel(ylabel, fontsize=8.2, color=QUANT_STYLE["ink"])
    ax.tick_params(axis="both", labelsize=7.3, colors=QUANT_STYLE["ink"], length=3, width=0.6)
    ax.grid(axis="y", color=QUANT_STYLE["grid"], linewidth=0.55)
    ax.grid(axis="x", visible=False)
    ax.spines[["top", "right"]].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(QUANT_STYLE["spine"])
        ax.spines[side].set_linewidth(0.6)
    ax.set_facecolor(QUANT_STYLE["background"])


def model_color(model_index: int) -> str:
    return MODEL_COLORS[model_index % len(MODEL_COLORS)]


def ci_lookup(path: Path) -> dict[tuple[str, str], dict[str, float]]:
    out: dict[tuple[str, str], dict[str, float]] = {}
    for row in read_csv(path):
        if row.get("model_id") != "all_models":
            continue
        lo = as_float(row, "ci_95_low")
        hi = as_float(row, "ci_95_high")
        mean_value = as_float(row, "mean")
        if lo is None or hi is None or mean_value is None:
            continue
        out[(str(row["endpoint"]), str(row["disagreement_bin"]))] = {
            "mean": mean_value,
            "lo": lo,
            "hi": hi,
        }
    return out


def draw_box(
    ax: Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    title: str,
    lines: list[str],
    facecolor: str,
    edgecolor: str = "#56676B",
    linewidth: float = 1.25,
    title_size: int = 9,
    body_size: int = 7.8,
    line_spacing: float = 0.027,
) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            zorder=2,
        )
    )
    ax.text(x + 0.018, y + h - 0.038, title, fontsize=title_size, fontweight="bold", color=PALETTE["ink"], va="top", zorder=3)
    for i, line in enumerate(lines):
        ax.text(x + 0.018, y + h - 0.073 - line_spacing * i, line, fontsize=body_size, color=PALETTE["ink"], va="top", zorder=3)


def arrow(ax: Axes, start: tuple[float, float], end: tuple[float, float], *, color: str = "#3A4649", lw: float = 1.5) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "->", "color": color, "lw": lw, "shrinkA": 2, "shrinkB": 2},
        zorder=1,
    )


def panel_label(ax: Axes, x: float, y: float, label: str) -> None:
    ax.text(x, y, label, fontsize=13, fontweight="bold", color=PALETTE["ink"], va="top")


def draw_grid_box(
    ax: Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    title: str,
    lines: list[str],
    facecolor: str,
    edgecolor: str = "#788587",
    linewidth: float = 0.8,
    title_size: float = 8.0,
    body_size: float = 6.8,
    line_spacing: float = 0.16,
    title_gap: float = 0.30,
    pad_x: float = 0.07,
    pad_y: float = 0.20,
    rounding_size: float = 0.0,
) -> tuple[FancyBboxPatch, list[plt.Text]]:
    boxstyle = "square,pad=0.010" if rounding_size <= 0 else f"round,pad=0.010,rounding_size={rounding_size}"
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=boxstyle,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=2,
    )
    ax.add_patch(patch)
    texts = [
        ax.text(
            x + pad_x * w,
            y + h - pad_y * h,
            title,
            fontsize=title_size,
            fontweight="bold",
            color=PALETTE["ink"],
            va="top",
            zorder=3,
        )
    ]
    body_top = y + h - (pad_y + title_gap) * h
    for i, line in enumerate(lines):
        texts.append(
            ax.text(
                x + pad_x * w,
                body_top - line_spacing * h * i,
                line,
                fontsize=body_size,
                color=PALETTE["ink"],
                va="top",
                zorder=3,
            )
        )
    return patch, texts


def panel_header(ax: Axes, label: str, title: str, *, color: str = PALETTE["ink"]) -> None:
    ax.text(0.0, 1.0, label, fontsize=11.0, fontweight="bold", color=color, va="top")
    ax.text(0.035, 0.982, title, fontsize=8.7, fontweight="bold", color=color, va="top")


def add_panel_arrow(
    ax: Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = "#6D777A",
    lw: float = 0.75,
) -> tuple[tuple[float, float], tuple[float, float]]:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "->", "color": color, "lw": lw, "shrinkA": 4, "shrinkB": 4, "mutation_scale": 7},
        zorder=1,
    )
    return start, end


def _bbox_overlap(a: Bbox, b: Bbox) -> bool:
    return a.x0 < b.x1 and a.x1 > b.x0 and a.y0 < b.y1 and a.y1 > b.y0


def write_study_design_layout_qa(
    fig: plt.Figure,
    out_dir: Path,
    box_texts: list[tuple[FancyBboxPatch, list[plt.Text]]],
    arrows: list[tuple[Axes, tuple[float, float], tuple[float, float]]],
) -> None:
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    visible_texts = [text for text in fig.findobj(plt.Text) if text.get_visible() and text.get_text().strip()]
    text_boxes = [(text, text.get_window_extent(renderer).expanded(1.02, 1.08)) for text in visible_texts]

    text_overlaps: list[str] = []
    for i, (left_text, left_box) in enumerate(text_boxes):
        for right_text, right_box in text_boxes[i + 1 :]:
            if _bbox_overlap(left_box, right_box):
                text_overlaps.append(f"{left_text.get_text()}  ||  {right_text.get_text()}")

    border_collisions: list[str] = []
    min_padding_px = 3.0
    for patch, texts in box_texts:
        patch_box = patch.get_window_extent(renderer)
        for text in texts:
            text_box = text.get_window_extent(renderer)
            distances = [
                text_box.x0 - patch_box.x0,
                patch_box.x1 - text_box.x1,
                text_box.y0 - patch_box.y0,
                patch_box.y1 - text_box.y1,
            ]
            if min(distances) < min_padding_px:
                border_collisions.append(text.get_text())

    arrow_text_hits: list[str] = []
    for ax, start, end in arrows:
        sx, sy = ax.transData.transform(start)
        ex, ey = ax.transData.transform(end)
        for _, text_box in text_boxes:
            padded = text_box.expanded(1.08, 1.20)
            for step in range(1, 30):
                t = step / 30
                px = sx + (ex - sx) * t
                py = sy + (ey - sy) * t
                if padded.contains(px, py):
                    arrow_text_hits.append("arrow intersects visible text bounding box")
                    break
            if arrow_text_hits and arrow_text_hits[-1] == "arrow intersects visible text bounding box":
                break

    report = [
        "figure_study_design_50k layout QA",
        "text_text_overlaps: " + str(len(text_overlaps)),
        "text_box_border_collisions: " + str(len(border_collisions)),
        "arrow_text_collisions_sampled: " + str(len(arrow_text_hits)),
        "manual_visual_check: required after render",
    ]
    if text_overlaps:
        report.append("text_text_overlap_examples:")
        report.extend(text_overlaps[:10])
    if border_collisions:
        report.append("text_box_border_collision_examples:")
        report.extend(border_collisions[:10])
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "figure_study_design_50k_layout_qa.txt").write_text("\n".join(report) + "\n", encoding="utf-8")


def plot_study_design(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_colors = {
        "background": "#FCFBF8",
        "source": "#EDF6F3",
        "mode": "#F7F1E5",
        "endpoint": "#F0F1F6",
        "endpoint_focus": "#EAF5F1",
        "focus": "#4B8674",
        "edge": "#D8DEDE",
        "ink": "#172124",
        "muted": "#5C6668",
    }
    bar_colors = ["#7AA1BF", "#C79278", "#88AB83", "#AD8AA5", "#9EA3AF"]

    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 7.0}):
        fig = plt.figure(figsize=(7.09, 6.95), facecolor=fig_colors["background"])
        _plot_study_design_grid(fig, out_dir, fig_colors, bar_colors)


def _plot_study_design_grid(fig: plt.Figure, out_dir: Path, fig_colors: dict[str, str], bar_colors: list[str]) -> None:
    grid = fig.add_gridspec(
        4,
        1,
        height_ratios=[0.42, 1.31, 2.00, 1.50],
        left=0.06,
        right=0.96,
        top=0.955,
        bottom=0.055,
        hspace=0.36,
    )
    title_ax = fig.add_subplot(grid[0])
    panel_a = fig.add_subplot(grid[1])
    panel_b = fig.add_subplot(grid[2])
    panel_c = fig.add_subplot(grid[3])
    for ax in (title_ax, panel_a, panel_b, panel_c):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(fig_colors["background"])

    title_ax.text(
        0.0,
        0.55,
        "Study design for testing cross-format uncertainty transfer",
        fontsize=10.4,
        fontweight="bold",
        color=fig_colors["ink"],
        va="center",
    )

    box_texts: list[tuple[FancyBboxPatch, list[plt.Text]]] = []
    arrows: list[tuple[Axes, tuple[float, float], tuple[float, float]]] = []

    panel_header(panel_a, "a", "Source-community distributions and bins", color=fig_colors["ink"])
    box_texts.append(
        draw_grid_box(
            panel_a,
            0.03,
            0.15,
            0.47,
            0.68,
            title="Five-label vote distribution",
            lines=["Reference distribution;", "not moral truth or universal norms."],
            facecolor=fig_colors["source"],
            edgecolor=fig_colors["source"],
            linewidth=0.0,
            title_size=7.7,
            body_size=6.45,
            line_spacing=0.15,
            title_gap=0.28,
        )
    )
    labels = ["author", "other", "everybody", "nobody", "info"]
    values = [0.28, 0.18, 0.24, 0.16, 0.14]
    left = 0.03 + (0.47 - 0.345) / 2
    bar_y = 0.235
    bar_h = 0.088
    bar_total = 0.345
    for label, value, color in zip(labels, values, bar_colors):
        width = value * bar_total
        panel_a.add_patch(Rectangle((left, bar_y), width, bar_h, facecolor=color, edgecolor=fig_colors["background"], linewidth=0.6, zorder=3))
        panel_a.text(left + width / 2, bar_y - 0.030, label, fontsize=6.0, ha="center", va="top", color=fig_colors["ink"], zorder=3)
        left += width
    box_texts.append(
        draw_grid_box(
            panel_a,
            0.56,
            0.15,
            0.41,
            0.68,
            title="Disagreement-bin logic",
            lines=[
                "High: top label ≥ 0.80",
                "Moderate: 0.65 to < 0.80",
                "Low: 0.50 to < 0.65",
                "Diffuse/no-clear: top label < 0.50",
            ],
            facecolor="#FCFBF8",
            edgecolor=fig_colors["edge"],
            linewidth=0.55,
            title_size=7.7,
            body_size=6.15,
            line_spacing=0.12,
            title_gap=0.28,
        )
    )
    panel_a.text(
        0.035,
        0.000,
        "Low-consensus is primary; diffuse/no-clear is secondary.",
        fontsize=6.45,
        color=fig_colors["muted"],
        va="bottom",
    )

    panel_header(panel_b, "b", "Same item × same model across prompt formats", color=fig_colors["ink"])
    box_texts.append(
        draw_grid_box(
            panel_b,
            0.04,
            0.43,
            0.28,
            0.30,
            title="Matched item × model",
            lines=["same SCRUPLES item", "same evaluated model"],
            facecolor="#FCFBF8",
            edgecolor=fig_colors["edge"],
            linewidth=0.55,
            title_size=7.65,
            body_size=6.55,
            line_spacing=0.22,
            title_gap=0.34,
        )
    )
    panel_b.text(
        0.04,
        0.305,
        "Fresh, stateless calls; verdict/agreement does not see",
        fontsize=6.45,
        color=fig_colors["muted"],
        va="top",
    )
    panel_b.text(0.04, 0.225, "the distribution answer.", fontsize=6.45, color=fig_colors["muted"], va="top")

    format_boxes = [
        (0.58, 0.69, "Distribution mode", ["estimates five-label probabilities"]),
        (0.58, 0.43, "Verdict/agreement mode", ["label + agreement estimate"]),
        (0.58, 0.17, "Repeated forced-choice", ["fresh labels for the same item × model"]),
    ]
    arrow_starts = [(0.32, 0.65), (0.32, 0.58), (0.32, 0.51)]
    for (x, y, title, lines), start in zip(format_boxes, arrow_starts):
        arrows.append((panel_b, start, add_panel_arrow(panel_b, start, (x, y + 0.095), color="#6D777A", lw=0.75)[1]))
        box_texts.append(
            draw_grid_box(
                panel_b,
                x,
                y,
                0.38,
                0.19,
                title=title,
                lines=lines,
                facecolor=fig_colors["mode"],
                edgecolor=fig_colors["mode"],
                linewidth=0.0,
                title_size=7.5,
                body_size=6.55,
                line_spacing=0.22,
                title_gap=0.40,
            )
        )

    panel_header(panel_c, "c", "Primary endpoint definitions", color=fig_colors["ink"])
    box_texts.append(
        draw_grid_box(
            panel_c,
            0.015,
            0.24,
            0.285,
            0.46,
            title="Agreement surplus",
            lines=["verdict agreement − source support"],
            facecolor=fig_colors["endpoint"],
            edgecolor=fig_colors["endpoint"],
            linewidth=0.0,
            title_size=7.45,
            body_size=6.35,
            title_gap=0.36,
        )
    )
    box_texts.append(
        draw_grid_box(
            panel_c,
            0.34,
            0.22,
            0.34,
            0.50,
            title="Distribution-agreement gap",
            lines=[
                "verdict agreement − distribution probability",
                "same model, item and selected label",
            ],
            facecolor=fig_colors["endpoint_focus"],
            edgecolor=fig_colors["endpoint_focus"],
            linewidth=0.0,
            title_size=7.55,
            body_size=6.35,
            line_spacing=0.18,
            title_gap=0.35,
        )
    )
    panel_c.text(
        0.51,
        0.115,
        "Cleanest cross-format coherence test",
        fontsize=6.55,
        fontweight="bold",
        color=fig_colors["focus"],
        ha="center",
        va="center",
    )
    box_texts.append(
        draw_grid_box(
            panel_c,
            0.72,
            0.24,
            0.26,
            0.46,
            title="Sampling compression",
            lines=["source entropy −", "repeated-output entropy (bits)"],
            facecolor=fig_colors["endpoint"],
            edgecolor=fig_colors["endpoint"],
            linewidth=0.0,
            title_size=7.3,
            body_size=6.25,
            line_spacing=0.18,
            title_gap=0.34,
        )
    )

    write_study_design_layout_qa(fig, out_dir, box_texts, arrows)
    stem = "figure_study_design_50k"
    fig.savefig(out_dir / f"{stem}.png", dpi=300)
    fig.savefig(out_dir / f"{stem}.svg")
    fig.savefig(out_dir / f"{stem}.pdf")
    plt.close(fig)


def plot_endpoint(path: Path, ci_path: Path, out_dir: Path, stem: str, title: str, ylabel: str) -> None:
    rows = read_csv(path)
    bins = ordered_bins(rows)
    all_rows = {row["disagreement_bin"]: row for row in rows if row["model_id"] == "all_models"}
    model_rows = [row for row in rows if row["model_id"] != "all_models"]
    models = sorted({row["model_id"] for row in model_rows})
    xs = list(range(len(bins)))
    means = [as_float(all_rows.get(bin_name, {}), "mean") or 0.0 for bin_name in bins]
    endpoint = str(rows[0]["endpoint"]) if rows else ""
    ci_by_key = ci_lookup(ci_path)

    fig, ax = plt.subplots(figsize=(7.09, 4.55), layout="constrained")
    fig.patch.set_facecolor(QUANT_STYLE["background"])
    ax.bar(xs, means, color=QUANT_STYLE["bar"], width=0.58, label="All models", alpha=0.95, zorder=2)
    for index, bin_name in enumerate(bins):
        ci = ci_by_key.get((endpoint, bin_name))
        if ci is None:
            continue
        mean_value = means[index]
        ax.errorbar(
            index,
            mean_value,
            yerr=[[mean_value - ci["lo"]], [ci["hi"] - mean_value]],
            fmt="none",
            ecolor=QUANT_STYLE["ci"],
            elinewidth=0.9,
            capsize=3,
            capthick=0.9,
            zorder=4,
        )
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
            color=model_color(model_index),
            label=model_id,
            alpha=0.88,
            linewidths=0.55,
            edgecolors="#FFFFFF",
            zorder=5,
        )
    ax.axhline(0, color=QUANT_STYLE["spine"], linewidth=0.55)
    ax.set_xticks(xs, [format_bin_label(bin_name) for bin_name in bins])
    style_quant_ax(ax, title=title, ylabel=ylabel)
    ax.legend(
        fontsize=6.8,
        ncols=3,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        borderaxespad=0,
        handletextpad=0.55,
        columnspacing=1.35,
        labelspacing=0.45,
        markerscale=1.15,
    )
    save(fig, out_dir, stem)


def plot_distribution_quality(path: Path, out_dir: Path) -> None:
    rows = [row for row in read_csv(path) if row["model_id"] == "all_models"]
    bins = ordered_bins(rows)
    by_bin = {row["disagreement_bin"]: row for row in rows}
    xs = list(range(len(bins)))

    fig, ax = plt.subplots(figsize=(6.7, 3.9))
    fig.patch.set_facecolor(QUANT_STYLE["background"])
    ax.plot(
        xs,
        [as_float(by_bin[bin_name], "mean_jsd") for bin_name in bins],
        marker="o",
        markersize=4,
        linewidth=1.25,
        color=QUANT_STYLE["support_blue"],
        label="JSD",
    )
    ax.plot(
        xs,
        [as_float(by_bin[bin_name], "mean_total_variation_distance") for bin_name in bins],
        marker="s",
        markersize=4,
        linewidth=1.25,
        color=QUANT_STYLE["support_orange"],
        label="Total variation",
    )
    ax.set_xticks(xs, [format_bin_label(bin_name) for bin_name in bins])
    style_quant_ax(ax, title="Distribution-mode alignment diagnostics", ylabel="Distance from source distribution", title_size=8.9)
    ax.legend(frameon=False, fontsize=6.8, loc="upper left", handlelength=1.8)
    save(fig, out_dir, "figure_distribution_quality_distances_50k")


def plot_paraphrase(path: Path, out_dir: Path) -> None:
    rows = [row for row in read_csv(path) if row["model_id"] == "all_models"]
    bins = ordered_bins(rows)
    by_bin = {row["disagreement_bin"]: row for row in rows}
    xs = list(range(len(bins)))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.9, 3.9))
    fig.patch.set_facecolor(QUANT_STYLE["background"])
    ax.bar(
        [x - width / 2 for x in xs],
        [as_float(by_bin[bin_name], "mean_paraphrase_agreement_surplus") or 0.0 for bin_name in bins],
        width=width,
        label="Agreement surplus",
        color=QUANT_STYLE["bar"],
        alpha=0.88,
    )
    ax.bar(
        [x + width / 2 for x in xs],
        [as_float(by_bin[bin_name], "mean_paraphrase_distribution_agreement_gap") or 0.0 for bin_name in bins],
        width=width,
        label="Distribution-agreement gap",
        color=QUANT_STYLE["support_orange"],
        alpha=0.82,
    )
    ax.axhline(0, color=QUANT_STYLE["spine"], linewidth=0.55)
    ax.set_xticks(xs, [format_bin_label(bin_name) for bin_name in bins])
    style_quant_ax(ax, title="Paraphrase audit effects", ylabel="Mean effect", title_size=8.9)
    ax.legend(frameon=False, fontsize=6.8, loc="upper left", ncols=2, handlelength=1.6, columnspacing=1.1)
    save(fig, out_dir, "figure_paraphrase_audit_effects_50k")


def plot_validity(path: Path, out_dir: Path) -> None:
    rows = read_csv(path)
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(row["model_id"], []).append(float(row["valid_primary_rate"]))
    models = sorted(grouped)
    rates = [sum(grouped[model]) / len(grouped[model]) for model in models]

    fig, ax = plt.subplots(figsize=(7.09, 3.8))
    fig.patch.set_facecolor(QUANT_STYLE["background"])
    xs = list(range(len(models)))
    baseline = 0.94
    for x, rate in zip(xs, rates):
        ax.vlines(x, baseline, rate, color=QUANT_STYLE["bar_light"], linewidth=3.2, zorder=1)
    ax.scatter(xs, rates, s=36, color=QUANT_STYLE["bar"], edgecolors="#FFFFFF", linewidths=0.6, zorder=3)
    for x, rate in zip(xs, rates):
        ax.text(x, rate + 0.0014, f"{rate:.1%}", ha="center", va="bottom", fontsize=6.6, color=QUANT_STYLE["muted"])
    ax.set_ylim(0.94, 1.006)
    ax.set_xticks(xs, models, rotation=15, ha="right")
    style_quant_ax(ax, title="Primary-validity rate by model", ylabel="Mean valid rate across prompt modes", title_size=8.9)
    save(fig, out_dir, "figure_validity_rate_by_model_50k")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render final 50k manuscript figures from figure-ready CSVs.")
    parser.add_argument("--in-dir", default="post_run/analysis_exports/50k/figure_ready")
    parser.add_argument("--out-dir", default="post_run/analysis_exports/50k/rendered_figures")
    parser.add_argument("--table-dir", default="post_run/analysis_exports/50k/manuscript_tables")
    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    table_dir = Path(args.table_dir)
    ci_path = table_dir / "table_primary_results_with_ci_50k.csv"
    plot_study_design(out_dir)
    plot_endpoint(
        in_dir / "figure_agreement_surplus_by_bin_model_50k.csv",
        ci_path,
        out_dir,
        "figure_agreement_surplus_by_bin_model_50k",
        "Agreement Surplus by Disagreement Bin",
        "Mean agreement surplus",
    )
    plot_endpoint(
        in_dir / "figure_distribution_gap_by_bin_model_50k.csv",
        ci_path,
        out_dir,
        "figure_distribution_gap_by_bin_model_50k",
        "Distribution-Agreement Gap by Disagreement Bin",
        "Mean distribution-agreement gap",
    )
    plot_endpoint(
        in_dir / "figure_sampling_compression_by_bin_model_50k.csv",
        ci_path,
        out_dir,
        "figure_sampling_compression_by_bin_model_50k",
        "Sampling Compression by Disagreement Bin",
        "Sampling compression (bits)",
    )
    plot_distribution_quality(in_dir / "figure_distribution_quality_by_bin_model_50k.csv", out_dir)
    plot_paraphrase(in_dir / "figure_paraphrase_effects_by_bin_model_50k.csv", out_dir)
    plot_validity(in_dir / "figure_validity_by_model_mode_50k.csv", out_dir)
    print(f"rendered figures: {out_dir}")


if __name__ == "__main__":
    main()
