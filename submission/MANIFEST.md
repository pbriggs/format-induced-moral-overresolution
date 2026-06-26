# Submission Package Manifest

This package is a simple article-style LaTeX review build generated from the canonical manuscript source:

- `article/nmi_moral_overresolution_draft_50k_v5.md`

## Manuscript And LaTeX

- `cover_letter.pdf`
- `cover_letter.tex`
- `manuscript.md`
- `supplementary_information.md`
- `latex/main.tex`
- `latex/supplementary_information.tex`
- `latex/sync_markdown_to_tex.py`
- `latex/sync_build_open.bat`
- `latex/build.ps1`
- `latex/build_and_open.bat`
- `latex/latexmkrc`
- `latex/main.pdf`
- `latex/supplementary_information.pdf`

## Final Figure PDFs

- `figures/final/figure_study_design_50k.pdf`
- `figures/final/figure_agreement_surplus_by_bin_model_50k.pdf`
- `figures/final/figure_distribution_gap_by_bin_model_50k.pdf`
- `figures/final/figure_sampling_compression_by_bin_model_50k.pdf`
- `figures/final/figure_distribution_quality_distances_50k.pdf`
- `figures/final/figure_paraphrase_audit_effects_50k.pdf`
- `figures/final/figure_validity_rate_by_model_50k.pdf`

## Editable Figure SVGs

- `figures/editable/figure_study_design_50k.svg`
- `figures/editable/figure_agreement_surplus_by_bin_model_50k.svg`
- `figures/editable/figure_distribution_gap_by_bin_model_50k.svg`
- `figures/editable/figure_sampling_compression_by_bin_model_50k.svg`
- `figures/editable/figure_distribution_quality_distances_50k.svg`
- `figures/editable/figure_paraphrase_audit_effects_50k.svg`
- `figures/editable/figure_validity_rate_by_model_50k.svg`

## Figure Source Files

- `figures/src/render_final_figures.py`
- `figures/src/figure_source_inventory_50k.md`
- `figures/src/final_figure_export_checklist_50k.md`

## Source Data

Inventory:

- `source_data/INVENTORY.md`

Figure-ready CSVs:

- `source_data/figure_ready/figure_agreement_surplus_by_bin_model_50k.csv`
- `source_data/figure_ready/figure_distribution_gap_by_bin_model_50k.csv`
- `source_data/figure_ready/figure_distribution_quality_by_bin_model_50k.csv`
- `source_data/figure_ready/figure_paraphrase_effects_by_bin_model_50k.csv`
- `source_data/figure_ready/figure_sampling_compression_by_bin_model_50k.csv`
- `source_data/figure_ready/figure_validity_by_model_mode_50k.csv`

Manuscript-table CSVs:

- `source_data/manuscript_tables/table_adjusted_tests_50k.csv`
- `source_data/manuscript_tables/table_baseline_distribution_quality_50k.csv`
- `source_data/manuscript_tables/table_component_allocation_50k.csv`
- `source_data/manuscript_tables/table_distribution_quality_50k.csv`
- `source_data/manuscript_tables/table_invalid_output_summary_50k.csv`
- `source_data/manuscript_tables/table_model_roster_50k.csv`
- `source_data/manuscript_tables/table_normative_certainty_50k.csv`
- `source_data/manuscript_tables/table_paraphrase_ci_50k.csv`
- `source_data/manuscript_tables/table_paraphrase_effects_50k.csv`
- `source_data/manuscript_tables/table_primary_contrasts_with_ci_50k.csv`
- `source_data/manuscript_tables/table_primary_results_with_ci_50k.csv`
- `source_data/manuscript_tables/table_robustness_annotation_info_50k.csv`
- `source_data/manuscript_tables/table_robustness_smoothing_50k.csv`
- `source_data/manuscript_tables/table_validity_by_model_mode_50k.csv`

Endpoint and diagnostic summaries:

- `source_data/endpoint_summaries/adjusted_tests_50k.csv`
- `source_data/endpoint_summaries/analysis_export_manifest_50k.json`
- `source_data/endpoint_summaries/bootstrap_contrast_ci_50k.csv`
- `source_data/endpoint_summaries/bootstrap_endpoint_ci_50k.csv`
- `source_data/endpoint_summaries/distribution_diagnostics_summary_50k.csv`
- `source_data/endpoint_summaries/distribution_entropy_correlations_50k.csv`
- `source_data/endpoint_summaries/leave_one_model_out_50k.csv`
- `source_data/endpoint_summaries/manuscript_results_summary_50k.md`
- `source_data/endpoint_summaries/model_level_endpoint_table_50k.csv`
- `source_data/endpoint_summaries/normative_certainty_by_bin_model_50k.csv`
- `source_data/endpoint_summaries/paraphrase_bootstrap_ci_50k.csv`
- `source_data/endpoint_summaries/paraphrase_effects_50k.csv`
- `source_data/endpoint_summaries/primary_endpoint_table_50k.csv`

Robustness summaries:

- `source_data/robustness/annotation_info_sensitivity_50k.csv`
- `source_data/robustness/baseline_distribution_quality_50k.csv`
- `source_data/robustness/smoothing_sensitivity_50k.csv`

Validity summaries:

- `source_data/validity/invalid_output_summary_50k.csv`
- `source_data/validity/validity_by_model_mode_50k.csv`
- `source_data/validity/validity_sensitivity_50k.csv`

## Restricted-Material Boundary

This package intentionally does not include raw SCRUPLES anecdotes, rendered prompts containing anecdote text, raw provider/model responses, full call ledgers, full run stores, `analysis_rows_50k.csv`, `distribution_diagnostics_50k.csv`, `paraphrase_original_vs_rewrite_50k.csv`, or model-ready row stores. Included source data are derived, release-facing summaries, figure-ready CSVs and manuscript-table CSVs.

## Verification Notes

- `submission/manuscript.md` was refreshed from `article/nmi_moral_overresolution_draft_50k_v5.md` and is hash-identical to the canonical manuscript source as of the Phase 3 packaging audit.
- Table 1 is presented as one main display item with internal panels `a, Model roster and collection windows` and `b, Target allocation by study component`.
- The build uses manual numbered references in the manuscript file; no `references.bib` file was found in the package.
- `submission/` is not matched by `.gitignore` in the current repository configuration.
