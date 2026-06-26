# Source Data Inventory

All files listed here are release-safe derived outputs copied into `submission/source_data/`. Raw SCRUPLES anecdotes, rendered prompts containing anecdote text, raw provider/model responses, full call ledgers, full run stores, unrestricted model-ready row stores and local secrets are intentionally excluded.

## Figure-Ready Data

- `figure_ready/figure_agreement_surplus_by_bin_model_50k.csv`: plotted data for Fig. 2 agreement surplus by disagreement bin and model.
- `figure_ready/figure_distribution_gap_by_bin_model_50k.csv`: plotted data for Fig. 3 distribution-agreement gap by disagreement bin and model.
- `figure_ready/figure_distribution_quality_by_bin_model_50k.csv`: plotted data for Extended Data Fig. 1 distribution-quality diagnostics.
- `figure_ready/figure_paraphrase_effects_by_bin_model_50k.csv`: plotted data for Extended Data Fig. 2 paraphrase-audit effects.
- `figure_ready/figure_sampling_compression_by_bin_model_50k.csv`: plotted data for Fig. 4 sampling compression by disagreement bin and model.
- `figure_ready/figure_validity_by_model_mode_50k.csv`: plotted data for Extended Data Fig. 3 validity rates by model and mode.

## Manuscript And Supplementary Tables

- `manuscript_tables/table_adjusted_tests_50k.csv`: adjusted primary and contrast tests.
- `manuscript_tables/table_baseline_distribution_quality_50k.csv`: baseline distribution-quality comparison table.
- `manuscript_tables/table_component_allocation_50k.csv`: target allocation by study component.
- `manuscript_tables/table_distribution_quality_50k.csv`: distribution-quality diagnostic table.
- `manuscript_tables/table_invalid_output_summary_50k.csv`: invalid-output status summary.
- `manuscript_tables/table_model_roster_50k.csv`: model roster, providers/routes, collection windows and targets.
- `manuscript_tables/table_normative_certainty_50k.csv`: normative-certainty summary table.
- `manuscript_tables/table_paraphrase_ci_50k.csv`: paraphrase-audit confidence intervals.
- `manuscript_tables/table_paraphrase_effects_50k.csv`: paraphrase-audit effect summaries.
- `manuscript_tables/table_primary_contrasts_with_ci_50k.csv`: primary endpoint contrasts and confidence intervals.
- `manuscript_tables/table_primary_results_with_ci_50k.csv`: primary endpoint estimates and confidence intervals.
- `manuscript_tables/table_robustness_annotation_info_50k.csv`: annotation-density and `info`-label robustness table.
- `manuscript_tables/table_robustness_smoothing_50k.csv`: source-community distribution smoothing robustness table.
- `manuscript_tables/table_validity_by_model_mode_50k.csv`: validity by model and prompt mode.

## Endpoint Summaries And Diagnostics

- `endpoint_summaries/adjusted_tests_50k.csv`: adjusted test results.
- `endpoint_summaries/analysis_export_manifest_50k.json`: manifest for derived analysis export files.
- `endpoint_summaries/bootstrap_contrast_ci_50k.csv`: bootstrap contrast confidence intervals.
- `endpoint_summaries/bootstrap_endpoint_ci_50k.csv`: bootstrap endpoint confidence intervals.
- `endpoint_summaries/distribution_diagnostics_summary_50k.csv`: aggregate distribution diagnostic summary.
- `endpoint_summaries/distribution_entropy_correlations_50k.csv`: distribution entropy correlation summaries.
- `endpoint_summaries/leave_one_model_out_50k.csv`: leave-one-model-out endpoint summaries.
- `endpoint_summaries/manuscript_results_summary_50k.md`: manuscript-facing results summary.
- `endpoint_summaries/model_level_endpoint_table_50k.csv`: model-level endpoint summaries.
- `endpoint_summaries/normative_certainty_by_bin_model_50k.csv`: normative-certainty summaries by bin and model.
- `endpoint_summaries/paraphrase_bootstrap_ci_50k.csv`: paraphrase-audit bootstrap confidence intervals.
- `endpoint_summaries/paraphrase_effects_50k.csv`: paraphrase-audit effect summaries.
- `endpoint_summaries/primary_endpoint_table_50k.csv`: primary endpoint summary table.

## Robustness Summaries

- `robustness/annotation_info_sensitivity_50k.csv`: annotation-density and `info`-label sensitivity summaries.
- `robustness/baseline_distribution_quality_50k.csv`: baseline distribution-quality robustness summary.
- `robustness/smoothing_sensitivity_50k.csv`: source-community smoothing sensitivity summary.

## Validity Summaries

- `validity/invalid_output_summary_50k.csv`: invalid-output category counts.
- `validity/validity_by_model_mode_50k.csv`: validity rates by model and prompt mode.
- `validity/validity_sensitivity_50k.csv`: validity sensitivity summary.
