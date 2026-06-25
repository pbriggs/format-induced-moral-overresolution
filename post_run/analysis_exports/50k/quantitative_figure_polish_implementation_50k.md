# Quantitative Figure Polish Implementation, 50k

## 1. Global Findings

- The original quantitative figures were scientifically consistent but visually uneven: main endpoint legends were too dominant, titles were large, support figures had similar visual weight to main figures, and the validity bar chart risked exaggerating near-ceiling differences.
- Fig. 1 was not edited in this pass; its restrained schematic style remains broadly compatible with the quantitative set.

## 2. Figure-by-Figure Recommendations

- Main endpoint figures: retain aggregate bars, aggregate CIs, and model-level points; harmonize figure size, titles, axes, markers, colors, legends, and grid styling.
- Distribution-quality diagnostics: keep as a quieter support line figure.
- Paraphrase audit: keep as a quieter support grouped-bar figure and retain the label `Distribution-agreement gap`.
- Validity: replace the truncated bar chart with a dot/lollipop support display to reduce visual exaggeration while preserving the same averaged model values.

## 3. Exact Changes Made

- Added shared quantitative styling helpers in `src/analysis/render_final_figures.py`.
- Standardized quantitative typography, muted colors, light horizontal gridlines, minimal spines, tick sizes, and export behavior.
- Coordinated the three main endpoint figures with:
  - common double-column width;
  - muted aggregate bars;
  - consistent model color and marker mapping;
  - lighter aggregate CI error bars;
  - compact legend outside the data region;
  - unrotated/wrapped disagreement-bin labels.
- Made support figures visually subordinate with smaller titles, muted colors, compact legends, and lighter line/bar styling.
- Converted `figure_validity_rate_by_model_50k` from a truncated bar chart to a dot/lollipop display with exact percentage labels.

## 4. Modest Redesign

- `figure_validity_rate_by_model_50k` was redesigned as a display-format polish change only.
- The same source CSV, model roster, and averaged validity rates are used.
- No data, analysis, interpretation, or claims changed.

## 5. Numerical Validation Summary

- Figs. 2-4 aggregate means match the figure-ready CSV rows.
- Figs. 2-4 aggregate CIs are read from `table_primary_results_with_ci_50k.csv`; no new CI values are computed.
- Model-level points are read directly from the figure-ready CSVs; no model-level CIs were added.
- Support figures are rendered directly from their figure-ready CSVs.
- See `quantitative_figure_numerical_validation_50k.txt` for row counts, CI coverage, PNG dimensions/DPI, SVG raster checks, and PDF header checks.

## 6. Source Files Confirmed Unchanged

- `post_run/analysis_exports/50k/figure_ready`
- `post_run/analysis_exports/50k/manuscript_tables`
- `article`

## 7. Rendered Files Regenerated

- `figure_agreement_surplus_by_bin_model_50k.{svg,png,pdf}`
- `figure_distribution_gap_by_bin_model_50k.{svg,png,pdf}`
- `figure_sampling_compression_by_bin_model_50k.{svg,png,pdf}`
- `figure_distribution_quality_distances_50k.{svg,png,pdf}`
- `figure_paraphrase_audit_effects_50k.{svg,png,pdf}`
- `figure_validity_rate_by_model_50k.{svg,png,pdf}`

## 8. Remaining Manual Polish Recommendations

- No manual Inkscape polish is required for correctness.
- Optional manual polish could fine-tune legend placement in the main endpoint figures if the journal production layout imposes a tighter vertical slot.
