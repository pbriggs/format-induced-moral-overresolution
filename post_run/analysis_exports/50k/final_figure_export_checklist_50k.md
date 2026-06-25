# Final Figure Export Checklist: 50k NMI Manuscript

Date: 2026-06-25

Scope: Stage 3 final figure package validation. This checklist records production checks only; it does not alter numerical results, source CSVs, manuscript tables or manuscript prose.

## Expected Files

| Figure | SVG | PNG | PDF |
|---|---|---|---|
| Fig. 1 study design | [x] `post_run/analysis_exports/50k/rendered_figures/figure_study_design_50k.svg` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_study_design_50k.png` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_study_design_50k.pdf` |
| Fig. 2 agreement surplus | [x] `post_run/analysis_exports/50k/rendered_figures/figure_agreement_surplus_by_bin_model_50k.svg` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_agreement_surplus_by_bin_model_50k.png` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_agreement_surplus_by_bin_model_50k.pdf` |
| Fig. 3 distribution-agreement gap | [x] `post_run/analysis_exports/50k/rendered_figures/figure_distribution_gap_by_bin_model_50k.svg` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_distribution_gap_by_bin_model_50k.png` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_distribution_gap_by_bin_model_50k.pdf` |
| Fig. 4 sampling compression | [x] `post_run/analysis_exports/50k/rendered_figures/figure_sampling_compression_by_bin_model_50k.svg` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_sampling_compression_by_bin_model_50k.png` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_sampling_compression_by_bin_model_50k.pdf` |
| Extended Data Fig. 1 distribution quality | [x] `post_run/analysis_exports/50k/rendered_figures/figure_distribution_quality_distances_50k.svg` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_distribution_quality_distances_50k.png` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_distribution_quality_distances_50k.pdf` |
| Extended Data Fig. 2 paraphrase audit | [x] `post_run/analysis_exports/50k/rendered_figures/figure_paraphrase_audit_effects_50k.svg` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_paraphrase_audit_effects_50k.png` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_paraphrase_audit_effects_50k.pdf` |
| Extended Data Fig. 3 validity | [x] `post_run/analysis_exports/50k/rendered_figures/figure_validity_rate_by_model_50k.svg` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_validity_rate_by_model_50k.png` | [x] `post_run/analysis_exports/50k/rendered_figures/figure_validity_rate_by_model_50k.pdf` |

## Validation Checks

- [x] All expected SVG files exist.
- [x] All expected PNG files exist.
- [x] All expected PDF files exist.
- [x] SVGs are vector/editable and contain no embedded raster `<image>` tags as the main artwork.
- [x] PDF files have valid `%PDF-` headers.
- [x] PNG files have valid PNG headers and review-scale dimensions.
- [x] Fig. 1 exists in the final rendered figure folder.
- [x] Fig. 1 avoids raw SCRUPLES anecdote text.
- [x] Fig. 1 frames SCRUPLES data as source-community reference distributions, not moral truth, universal norms or representative population estimates.
- [x] Fig. 1 visually privileges distribution-agreement gap as the cleanest same-model, same-item, same-label endpoint.
- [x] Figs. 2-4 include aggregate all-model 95% CI error bars where CIs already exist.
- [x] Moderate-consensus context rows do not receive invented CIs.
- [x] Model-level points are preserved and do not receive model-level CIs.
- [x] Fig. 4 y-axis includes bits: `Sampling compression (bits)`.
- [x] Extended Data Fig. 2 uses `Distribution-agreement gap`.
- [x] Source CSVs were not changed.
- [x] Manuscript tables were not changed.
- [x] Numerical results were not changed.
- [x] Manuscript prose was not edited.
- [x] No provider calls were run.
- [x] No analysis exports were regenerated.

## Numeric Validation Summary

All all-model means in Figs. 2-4 continue to match their figure-ready CSV rows and, where CI fields exist, `table_primary_results_with_ci_50k.csv`.

| Endpoint | Bin | Mean | CI display |
|---|---|---:|---|
| Agreement surplus | high_consensus | 0.169409 | 0.145651-0.194624 |
| Agreement surplus | moderate_consensus | 0.294630 | none available |
| Agreement surplus | low_consensus | 0.370931 | 0.361206-0.381114 |
| Agreement surplus | diffuse | 0.435619 | 0.427337-0.444341 |
| Agreement surplus | low_diffuse | 0.396810 | 0.389856-0.404111 |
| Distribution-agreement gap | high_consensus | 0.182842 | 0.169762-0.196217 |
| Distribution-agreement gap | moderate_consensus | 0.221510 | none available |
| Distribution-agreement gap | low_consensus | 0.232687 | 0.224387-0.241341 |
| Distribution-agreement gap | diffuse | 0.226556 | 0.216740-0.237164 |
| Distribution-agreement gap | low_diffuse | 0.230233 | 0.223606-0.237057 |
| Sampling compression | high_consensus | 0.563708 | 0.495005-0.633547 |
| Sampling compression | moderate_consensus | 0.997936 | none available |
| Sampling compression | low_consensus | 1.264638 | 1.218425-1.309054 |
| Sampling compression | diffuse | 1.507379 | 1.452200-1.562768 |
| Sampling compression | low_diffuse | 1.361734 | 1.323687-1.399195 |

## Stage 4 Readiness

- [x] Final figure package is present.
- [x] Figure source inventory is present: `post_run/analysis_exports/50k/figure_source_inventory_50k.md`.
- [x] Final export checklist is present: `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`.
- [x] Stage 4 caption/source-data consistency review can begin.
