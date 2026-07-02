# Source Data Dictionary (Submission Package)

This file defines CSV columns and units for the release-safe source-data package in `submission/source_data/`.

Scope:
- Derived outputs only.
- Excludes raw SCRUPLES anecdotes, rendered prompts with anecdote text, raw provider responses, and full run stores.

## Unit and coding conventions

- Proportions/rates: unitless in `[0, 1]` unless noted.
- Entropy: bits.
- Distances (JSD, total variation, Brier): unitless.
- Counts (`n`, `target_calls`, `unique_items`, `bootstrap_iterations`): integers.
- Timestamps: ISO-8601 UTC strings.
- Confidence-interval bounds (`ci_95_low`, `ci_95_high`): same unit as the estimate.
- Endpoint scale:
  - `agreement_surplus`, `distribution_agreement_gap`: proportion scale (unitless, often reported as percentage points in prose).
  - `repeated_forced_choice_concentration`: bits.

## File-to-schema map

### Schema A: endpoint means by bin/model
Columns: `disagreement_bin, endpoint, mean, model_id, n`

Files:
- `endpoint_summaries/primary_endpoint_table_50k.csv`
- `endpoint_summaries/model_level_endpoint_table_50k.csv`
- `figure_ready/figure_agreement_surplus_by_bin_model_50k.csv`
- `figure_ready/figure_distribution_gap_by_bin_model_50k.csv`
- `figure_ready/figure_sampling_compression_by_bin_model_50k.csv`

### Schema B: endpoint means with smoothing/annotation sensitivity labels
Columns: `disagreement_bin, endpoint, mean, model_id, n, source_distribution_variant`

Files:
- `manuscript_tables/table_robustness_smoothing_50k.csv`
- `robustness/smoothing_sensitivity_50k.csv`

### Schema C: endpoint means with smoothing/annotation + subset labels
Columns: `disagreement_bin, endpoint, mean, model_id, n, source_distribution_variant, subset`

Files:
- `manuscript_tables/table_robustness_annotation_info_50k.csv`
- `robustness/annotation_info_sensitivity_50k.csv`

### Schema D: endpoint bootstrap CIs by bin
Columns: `bootstrap_iterations, bootstrap_one_sided_p_positive, ci_95_high, ci_95_low, ci_excludes_zero, disagreement_bin, endpoint, observed_mean, positive`

Files:
- `endpoint_summaries/bootstrap_endpoint_ci_50k.csv`

### Schema E: adjusted tests table
Columns: `bootstrap_iterations, bootstrap_one_sided_p_positive, ci_95_high, ci_95_low, ci_excludes_zero, disagreement_bin, endpoint, holm_adjusted_p, observed_mean, p_value_note, positive`

Files:
- `endpoint_summaries/adjusted_tests_50k.csv`
- `manuscript_tables/table_adjusted_tests_50k.csv`

### Schema F: endpoint contrast bootstrap CIs
Columns: `bootstrap_iterations, bootstrap_one_sided_p_positive, ci_95_high, ci_95_low, contrast, denominator_bin, endpoint, numerator_bin, observed_difference`

Files:
- `endpoint_summaries/bootstrap_contrast_ci_50k.csv`
- `manuscript_tables/table_primary_contrasts_with_ci_50k.csv`

### Schema G: primary results with CI (includes all-model row)
Columns: `bootstrap_iterations, bootstrap_one_sided_p_positive, ci_95_high, ci_95_low, disagreement_bin, endpoint, mean, model_id, n`

Files:
- `manuscript_tables/table_primary_results_with_ci_50k.csv`

### Schema H: distribution diagnostics by bin/model
Columns: `disagreement_bin, mean_brier_majority_label, mean_jsd, mean_model_distribution_entropy, mean_source_entropy, mean_total_variation_distance, model_id, n`

Files:
- `manuscript_tables/table_distribution_quality_50k.csv`
- `figure_ready/figure_distribution_quality_by_bin_model_50k.csv`

### Schema I: distribution diagnostics summary (adds normalized source entropy)
Columns: `disagreement_bin, mean_brier_majority_label, mean_jsd, mean_model_distribution_entropy, mean_source_entropy, mean_source_entropy_normalized, mean_total_variation_distance, model_id, n`

Files:
- `endpoint_summaries/distribution_diagnostics_summary_50k.csv`

### Schema J: entropy correlation summary
Columns: `disagreement_bin, model_id, n, pearson_source_vs_model_distribution_entropy`

Files:
- `endpoint_summaries/distribution_entropy_correlations_50k.csv`

### Schema K: baseline distribution quality
Columns: `baseline, disagreement_bin, mean_baseline_entropy, mean_brier_majority_label, mean_jsd, mean_source_entropy, mean_total_variation_distance, n`

Files:
- `manuscript_tables/table_baseline_distribution_quality_50k.csv`
- `robustness/baseline_distribution_quality_50k.csv`

### Schema L: paraphrase effects summary
Columns: `chosen_label_stability_rate, disagreement_bin, mean_paraphrase_agreement_surplus, mean_paraphrase_distribution_agreement_gap, mean_paraphrase_minus_original_gap, mean_paraphrase_minus_original_surplus, model_id, n, n_original_matched`

Files:
- `endpoint_summaries/paraphrase_effects_50k.csv`
- `figure_ready/figure_paraphrase_effects_by_bin_model_50k.csv`
- `manuscript_tables/table_paraphrase_effects_50k.csv`

### Schema M: paraphrase bootstrap CIs
Columns: `bootstrap_iterations, ci_95_high, ci_95_low, disagreement_bin, endpoint, n, observed_mean`

Files:
- `endpoint_summaries/paraphrase_bootstrap_ci_50k.csv`
- `manuscript_tables/table_paraphrase_ci_50k.csv`

### Schema N: normative-certainty summary by bin/model
Columns: `disagreement_bin, mean_moral_certainty, mean_source_entropy, mean_source_majority_support, model_id, n`

Files:
- `endpoint_summaries/normative_certainty_by_bin_model_50k.csv`
- `manuscript_tables/table_normative_certainty_50k.csv`

### Schema O: leave-one-model-out summary
Columns: `disagreement_bin, endpoint, mean, model_id, n, omitted_model_id`

Files:
- `endpoint_summaries/leave_one_model_out_50k.csv`

### Schema P: validity by model and prompt mode
Columns: `empty_response, invalid_json, model_id, n, probability_out_of_bounds, probability_sum_error, prompt_mode, valid_extracted_json, valid_primary, valid_primary_rate, valid_strict_schema`

Files:
- `figure_ready/figure_validity_by_model_mode_50k.csv`
- `manuscript_tables/table_validity_by_model_mode_50k.csv`
- `validity/validity_by_model_mode_50k.csv`

### Schema Q: invalid output summary
Columns: `n, validity_status`

Files:
- `manuscript_tables/table_invalid_output_summary_50k.csv`
- `validity/invalid_output_summary_50k.csv`

### Schema R: model roster and collection window
Columns: `api_route, first_call_utc, last_call_utc, model_id, provider, reasoning_effort, target_calls, temperature, top_p`

Files:
- `manuscript_tables/table_model_roster_50k.csv`

### Schema S: component allocation
Columns: `component_type, disagreement_bin, models, prompt_mode, target_calls, unique_items`

Files:
- `manuscript_tables/table_component_allocation_50k.csv`

### Schema T: validity sensitivity by filter
Columns: `disagreement_bin, endpoint, mean, model_id, n, valid_filter`

Files:
- `validity/validity_sensitivity_50k.csv`

## Column glossary

| Column | Definition | Unit / allowed values |
|---|---|---|
| `api_route` | API endpoint used for route provenance. | URL string |
| `baseline` | Baseline comparator used in distribution-quality checks. | categorical (`uniform`, `global_base_rate`, `source_majority_oracle`, etc.) |
| `bootstrap_iterations` | Number of bootstrap replicates. | count |
| `bootstrap_one_sided_p_positive` | One-sided bootstrap p-value for positive-effect direction. | unitless in `[0,1]` |
| `chosen_label_stability_rate` | Matched original-vs-paraphrase chosen-label agreement rate. | proportion `[0,1]` |
| `ci_95_high` | Upper 95% bootstrap confidence bound. | same unit as endpoint/estimate |
| `ci_95_low` | Lower 95% bootstrap confidence bound. | same unit as endpoint/estimate |
| `ci_excludes_zero` | Indicator that CI does not include zero. | boolean (`true/false`) |
| `component_type` | Study component grouping for target allocation. | categorical |
| `contrast` | Contrast label for numerator minus denominator bins. | text label |
| `denominator_bin` | Disagreement bin in denominator for contrast. | categorical bin label |
| `disagreement_bin` | Item disagreement stratum. | categorical (`high_consensus`, `moderate_consensus`, `low_consensus`, `diffuse`, `low_diffuse`) |
| `empty_response` | Count of empty responses for model/mode slice. | count |
| `endpoint` | Endpoint identifier. | categorical (`agreement_surplus`, `distribution_agreement_gap`, `repeated_forced_choice_concentration`) |
| `first_call_utc` | First call timestamp in final roster. | ISO-8601 UTC |
| `holm_adjusted_p` | Holm-adjusted p-value across primary endpoints. | unitless in `[0,1]` |
| `invalid_json` | Count of invalid-JSON outputs for model/mode slice. | count |
| `last_call_utc` | Last call timestamp in final roster. | ISO-8601 UTC |
| `mean` | Mean endpoint estimate for grouping. | unitless for surplus/gap; bits for concentration |
| `mean_baseline_entropy` | Mean entropy under baseline comparator distribution. | bits |
| `mean_brier_majority_label` | Mean Brier score against source-majority label coding. | unitless |
| `mean_jsd` | Mean Jensen-Shannon divergence between model and source distributions. | unitless |
| `mean_model_distribution_entropy` | Mean entropy of model distribution-mode outputs. | bits |
| `mean_moral_certainty` | Mean model-reported moral certainty (secondary measure). | proportion `[0,1]` |
| `mean_paraphrase_agreement_surplus` | Mean agreement surplus in paraphrased subset. | unitless proportion-scale |
| `mean_paraphrase_distribution_agreement_gap` | Mean distribution-agreement gap in paraphrased subset. | unitless proportion-scale |
| `mean_paraphrase_minus_original_gap` | Mean difference (paraphrase minus original) for distribution-agreement gap. | unitless proportion-scale |
| `mean_paraphrase_minus_original_surplus` | Mean difference (paraphrase minus original) for agreement surplus. | unitless proportion-scale |
| `mean_source_entropy` | Mean entropy of source-community distribution. | bits |
| `mean_source_entropy_normalized` | Mean source entropy normalized by log2(5). | unitless in `[0,1]` |
| `mean_source_majority_support` | Mean support for source-majority label. | proportion `[0,1]` |
| `mean_total_variation_distance` | Mean total variation distance between model and source distributions. | unitless |
| `model_id` | Frozen model identifier. | text |
| `models` | Number of evaluated models represented in allocation row. | count |
| `n` | Number of rows/units underlying summary for grouping. | count |
| `n_original_matched` | Number of original rows matched to paraphrase rows in overlap subset. | count |
| `numerator_bin` | Disagreement bin in numerator for contrast. | categorical bin label |
| `observed_difference` | Observed contrast estimate (`numerator_bin - denominator_bin`). | same unit as endpoint |
| `observed_mean` | Observed mean used in CI/p-value summaries. | same unit as endpoint |
| `omitted_model_id` | Model omitted in leave-one-model-out summary row. | text |
| `p_value_note` | Reporting note (e.g., finite bootstrap floor). | text |
| `positive` | Indicator that observed estimate is positive. | boolean (`true/false`) |
| `probability_out_of_bounds` | Count of outputs with probability entries outside `[0,1]`. | count |
| `probability_sum_error` | Count of outputs failing allowed probability-sum tolerance. | count |
| `prompt_mode` | Prompt mode for validity summaries. | categorical |
| `provider` | Provider label for route provenance. | text |
| `reasoning_effort` | Recorded provider/model reasoning-effort field. | text or blank |
| `source_distribution_variant` | Source-distribution variant for sensitivity checks. | categorical (`raw`, `jeffreys`, `laplace`, etc.) |
| `subset` | Analysis subset label used in robustness summaries. | categorical |
| `target_calls` | Number of target calls planned/allocated for row grouping. | count |
| `temperature` | Decoding temperature used in roster entry. | unitless |
| `top_p` | Top-p setting from roster entry (may be blank/null). | unitless in `[0,1]` or blank |
| `unique_items` | Number of unique items represented in allocation row. | count |
| `valid_extracted_json` | Count of outputs accepted via extracted-JSON path. | count |
| `valid_filter` | Validity filter applied to derive sensitivity summary row. | categorical |
| `valid_primary` | Count of primary-valid outputs for model/mode slice. | count |
| `valid_primary_rate` | Primary-valid rate (`valid_primary / n`). | proportion `[0,1]` |
| `valid_strict_schema` | Count of outputs accepted via strict schema. | count |
| `validity_status` | Invalid/valid category label in summary table. | categorical |
