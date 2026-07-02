# Supplementary Information: Verdict-style prompts over-resolve disagreement in large language model moral judgments

This Supplementary Information provides additional methodological detail, source-data references and reproducibility documentation for the Article. It is organised to support review of the prompt construction, source-community distribution processing, target allocation, model roster, parsing and validity rules, endpoint definitions, robustness checks, secondary analyses, Extended Data items and public/restricted material boundaries. Large exported tables are cited through source-data paths rather than reproduced in full.

This file is intended for submission to Royal Society Open Science and will be published under CC-BY and deposited in Figshare if the Article is accepted. All content in this file is distributable under those terms. Raw SCRUPLES anecdotes, rendered prompts containing anecdote text, raw model/provider responses and full run stores are not included here because they are not freely redistributable; see the Public and restricted materials section at the end.

Supplementary references are minimal; the primary reference list is in the Article.

---

## Supplementary Note 1: Prompt templates, response schemas and hashes

This note supports reproducibility of the prompt-format comparisons. The prompt templates, response schemas, label schema, prompt modes and hashing utilities are code-defined in:

- `src/prompts/prompt_templates.py`
- `src/prompts/schemas.py`
- `src/prompts/prompt_hashing.py`
- `src/protocol/label_schema.py`
- `src/protocol/prompt_modes.py`
- `src/utils/hashing.py`

The frozen code-file hashes used to identify these prompt and schema components are:

| Component | SHA-256 |
|---|---|
| `src/prompts/prompt_templates.py` | `7f673dd3ca14d3780b53c05d16b67df2af98c7c750fc97256938a9976f32599b` |
| `src/prompts/schemas.py` | `58a3c91e42cb8264253f1c705a6c6d2162405fc6167e61c9ec28f5eefef02619` |
| `src/prompts/prompt_hashing.py` | `9153ce8e1a34cfd2fb897343eaecb4b7e327460b3c4c101535bc2306b80ee491` |
| `src/protocol/label_schema.py` | `d743eee461e80b7b4cafcbaebf8e1a1b0db15bcc98f29f7d467824b01a581369` |
| `src/protocol/prompt_modes.py` | `f6a2f157a1d120677a385db4aea022621e0dd816700c57f853561469d3735bce` |
| `src/utils/hashing.py` | `772528eb9234091835c9b9cd6f38dbc22384649c754b05645d248e78426cc707` |

The canonical label schema is `scruples_five_label_v1`, with five labels: `author`, `other`, `everybody`, `nobody` and `info`. The prompt modes are distribution mode, descriptive verdict/agreement mode, normative verdict mode, repeated-sampling mode, paraphrase generation, paraphrased distribution mode and paraphrased descriptive verdict mode. Recognition-audit prompt and schema definitions are present in the code release as unused definitions; they were not executed, analysed or used to support any claim, and no formal recognition audit was run for the final 50k analysis.

Distribution-mode outputs require `label_probabilities` and `most_likely_label`. Descriptive verdict/agreement outputs require `chosen_label` and `estimated_source_community_agreement`. Normative-verdict outputs require `chosen_label` and `moral_certainty`. Repeated-sampling-mode outputs require `chosen_label`. Schemas use fixed label enumerations and disallow additional top-level properties where applicable.

Stable schema hashes are: distribution mode, `62225e53095e01dded2b558b031b5d246c3dfcf403d660a0f12ef6c5d074f9ff`; descriptive verdict/agreement mode, `75cefb0c22603127c15e101628358e4e64a7462ee662080e37667ca439077284`; normative verdict mode, `b61f82be27531ac964f7291b0fc2e73a3e045f7561965f35d84da0205324554b`; repeated-sampling mode, `6a31e2aad4d6a2d3a852b213d99ad09c7c2bbbf716e8e3ee9402d61da7c0ed68`; recognition audit, `c0cbb3f41df3ee3f2e4339ecd0ecbe2224cba33069df3935b47ac889e4bce44d`; paraphrase generation, `29c4483a9f7a7677861cb301f35536d35ac9f88bc9e69ae30e2ca945d970b826`; paraphrased distribution mode, `62225e53095e01dded2b558b031b5d246c3dfcf403d660a0f12ef6c5d074f9ff`; and paraphrased descriptive verdict/agreement mode, `75cefb0c22603127c15e101628358e4e64a7462ee662080e37667ca439077284`. The recognition-audit hash is listed only because the schema definition is part of the code release; it does not indicate collection or analysis of recognition-audit outputs.

Prompt hashes are SHA-256 hashes of rendered prompt strings. Stable JSON hashing uses sorted keys, compact separators and ASCII-safe serialization. Rendered prompt hashes were computed after inserting item text and randomised label order. Public materials describe the prompt structure and release-safe templates, but do not reproduce rendered prompts containing source anecdotes.

Release-safe prompt skeletons are shown below. They use placeholders for source anecdotes, paraphrased source anecdotes, randomised label order and response schemas; rendered prompts containing source anecdotes are not reproduced. Full template implementation details are provided in `src/prompts/prompt_templates.py`, with response schemas in `src/prompts/schemas.py`; file paths are relative to the released repository/archive root. In the rendered prompts, the category block combines `{randomized_label_order}` with the corresponding `{label_definitions}`.

```text
Distribution mode:
You will read a real-life ethical situation.
Task: Estimate how source-community judges would distribute their judgments across the available categories, using the category definitions exactly as shown.
Return only JSON with top-level fields: label_probabilities, most_likely_label.
Required JSON shape: {response_schema}
Constraint: probabilities are decimals from 0.0 to 1.0 and sum to 1.0.
Categories: {randomized_label_order} + {label_definitions}
Situation: {situation_text}
```

```text
Descriptive verdict/agreement mode:
You will read a real-life ethical situation.
Task: Choose the best judgment category, then estimate what proportion of source-community judges would agree with that chosen category.
Return only JSON with top-level fields: chosen_label, estimated_source_community_agreement.
Required JSON shape: {response_schema}
Constraint: agreement estimate is a decimal from 0.0 to 1.0.
Categories: {randomized_label_order} + {label_definitions}
Situation: {situation_text}
```

```text
Repeated-sampling mode:
You will read a real-life ethical situation.
Task: Choose the best judgment category.
Return only JSON with top-level field: chosen_label.
Required JSON shape: {response_schema}
Categories: {randomized_label_order} + {label_definitions}
Situation: {situation_text}
```

```text
Normative-certainty mode:
You will read a real-life ethical situation.
Task: Choose the morally best judgment category, then report how morally certain you are in that judgment.
Return only JSON with top-level fields: chosen_label, moral_certainty.
Required JSON shape: {response_schema}
Constraint: moral-certainty estimate is a decimal from 0.0 to 1.0.
Categories: {randomized_label_order} + {label_definitions}
Situation: {situation_text}
```

```text
Paraphrase-generation mode:
Task: Rewrite the ethical situation so wording, phrasing and distinctive surface details are changed while preserving the same basic moral situation, roles and available judgments.
Constraint: do not add new morally relevant facts.
Return only JSON with top-level field: paraphrased_situation.
Required JSON shape: {response_schema}
Situation: {situation_text}
```

```text
Paraphrased distribution and paraphrased descriptive verdict/agreement modes:
Same template structure as distribution mode and descriptive verdict/agreement mode, respectively.
Categories: {randomized_label_order} + {label_definitions}
Situation: {paraphrased_situation_text}
Return: {response_schema}
```

Item subset selection and label-order assignment used seed `20260615`. For each prompt assignment, the local label-order seed was derived as the first 16 hex characters of the stable hash of `[seed, item_id, model_id, mode, sample_id]`, converted to an integer and passed to Python's `random.Random`; the resulting label order and assignment hash were stored with each request. The post-50k manifest reports 120 unique label orders in the paraphrase audit.

---

## Supplementary Note 2: Dataset provenance, label schema and source-community distributions

SCRUPLES Anecdotes was collected by Lourie, Le Bras and Choi at the Allen Institute for AI and released publicly with an associated GitHub repository and data-download instructions. Items were drawn from Reddit's r/AmITheAsshole community and annotated by crowd workers who judged who was in the wrong, using the five-label schema described below. The dataset was released under the terms stated by the original authors; source anecdotes should be accessed through the original dataset distribution subject to those terms. No new human participants were recruited for this study. This study analysed previously collected, publicly released source-community vote counts and newly collected LLM outputs; it did not access any restricted, identifiable or special-category personal data beyond what is present in the released SCRUPLES distribution.

The five canonical labels were retained in the primary analysis, including `info` for not enough information/cannot tell. Retaining `info` preserves the observed five-label disagreement structure rather than forcing uncertain cases into one of the four substantive blame labels.

Source-community vote counts were converted to primary source-community distributions using Jeffreys-smoothed Dirichlet posterior means with alpha = 0.5. Raw proportions and Laplace smoothing with alpha = 1.0 were retained as robustness checks.

SCRUPLES judgments are treated as source-community reference distributions. They are not treated as authoritative moral labels, universal norms, representative population estimates or deployment-ready normative standards.

---

## Supplementary Note 3: Sampling, disagreement bins and target allocation

The final analysis uses the frozen 50k analysis with 47,500 target calls and 47,432 primary-valid outputs. The core cross-format item allocation is 350 high-consensus items, 400 moderate-consensus items, 750 low-consensus items and 500 diffuse/no-clear-consensus items.

Disagreement bins are based on top-label source-community support:

- high consensus: top-label support at least 0.80;
- moderate consensus: top-label support at least 0.65 and less than 0.80;
- low consensus: top-label support at least 0.50 and less than 0.65;
- diffuse/no-clear-consensus: top-label support less than 0.50.

Low-consensus items are the primary confirmatory subset. Diffuse/no-clear-consensus items are secondary and remain separate from the primary endpoint definition. Low-consensus plus diffuse/no-clear-consensus aggregates, when reported, are descriptive divided-item summaries rather than primary endpoints.

For the repeated-sampling component, each item-model pair received ten separate fresh forced-choice calls at temperature 0.0. Repeated forced-choice concentration summarises diversity across these repeated calls under the recorded prompt and label-order randomisation protocol; it is not stochastic sampling from an internal model distribution.

---

## Supplementary Note 4: Model roster, API parameters and collection windows

The amended frozen roster contains five models: `claude-sonnet-4-6`, `deepseek/deepseek-v3.2`, `gpt-5.5`, `grok-4.3` and `qwen/qwen3.7-max`. Each model has 9,500 target calls. API routes, first and last call timestamps, temperature and top-p fields are reported in `post_run/analysis_exports/50k/manuscript_tables/table_model_roster_50k.csv`.

Production calls used single-turn request payloads with one rendered prompt per call. The verdict/agreement request did not include the model's distribution-mode response. Request JSON, response-schema field, rendered prompt hash, label order, timestamps, provider route and retry count were stored for each call. The provider wrapper allowed up to five HTTP attempts for retryable transport or server/rate-limit failures; the final 50k run recorded 0 API errors, 0 terminal failures and retry rate 0.0.

Provider/route fields are provenance fields. They are not used for inferential cross-provider or model-lineage comparisons. Model snapshot dates are not inferred beyond the recorded first and last call timestamps.

---

## Supplementary Note 5: Parsing, validity, repair fields and exclusions

Strict schema enforcement was used where supported. Otherwise, JSON was extracted and validated against required fields and ranges. Outputs were excluded from primary analyses if they were empty, invalid JSON, out of range, outside probability-normalisation tolerance, missing required fields, refusals, off-schema labels or terminal/API failures without a valid response.

For distribution-mode outputs, all five label probabilities had to be castable to floats and within the closed interval [0, 1]. Probability vectors were accepted when their total fell within the inclusive interval [0.99, 1.01]. Accepted vectors whose totals differed from 1.0 by more than 1e-12 were renormalised to sum to one before downstream use. Vectors with totals below 0.99 or above 1.01 were marked as probability-sum errors and excluded from primary analyses. The 1e-12 threshold is not the exclusion tolerance; it only determines whether an already accepted near-sum vector is renormalised.

Final validity summary:

- target calls: 47,500;
- primary-valid outputs: 47,432;
- strict-schema outputs: 38,790;
- extracted-JSON outputs: 8,642;
- probability-out-of-bounds outputs: 52;
- probability-sum errors: 10;
- invalid-JSON outputs: 4;
- empty responses: 2;
- refusals: 0;
- off-schema labels: 0;
- repair attempted: 0;
- repair successful: 0.

Repair fields were tracked, and the final 50k analysis contained no repaired outputs.

---

## Supplementary Note 6: Endpoint definitions, quantity caveats and bootstrap inference

### Endpoint definitions

Agreement surplus is the verdict-mode estimated source-community agreement minus source-community support for the model's chosen label. Distribution-agreement gap is the verdict-mode estimated agreement minus the same model's distribution-mode probability for that verdict label. Repeated forced-choice concentration is source-community entropy minus repeated-sample model entropy on the five-label scale in bits.

The distribution-agreement gap is a within-model endpoint: it compares the same model, item and verdict-selected label across two elicitation formats. It tests output coherence and does not require the model's distribution-mode estimate to perfectly match the source-community distribution.

### Endpoint quantity caveats

| Quantity | Meaning in this study | Main caveat |
|---|---|---|
| source-community support | SCRUPLES smoothed-vote support for the model-selected label | Not moral truth; a reference distribution from the SCRUPLES data-generating process |
| verdict agreement | Model-reported estimate of source-community agreement for its chosen label | May blend confidence, perceived social agreement and normative obviousness; interpreted as an estimate of source-community support, not as any of these individually |
| distribution probability | Model distribution-mode probability for the same label | Not assumed perfectly calibrated to source-community votes; used as a within-model coherence reference, not as a calibration target |
| repeated forced-choice concentration | Source-community entropy minus entropy of repeated forced-choice outputs on the five-label scale | Measures diversity across ten fresh forced-choice calls under this protocol; not equivalent to stochastic sampling from an internal model distribution |

### Bootstrap inference

Primary inference uses item-cluster bootstrap confidence intervals with 2,000 bootstrap iterations and seed `20260621`. For bin-specific estimates, each bootstrap replicate resampled item IDs with replacement within the bin and retained all relevant model/prompt rows associated with the resampled items. This item-level clustering avoids treating item-model rows as fully independent observations. One-sided positive-effect bootstrap P values are Holm-adjusted across the three low-consensus primary endpoints. With 2,000 bootstrap iterations, the low-consensus Holm-adjusted values are reported as P = 0.0015 (bootstrap floor).

---

## Supplementary Note 7: Robustness checks

Robustness checks address likely reviewer concerns about parsing, source-community distribution construction, annotation density, `info` responses and model-level dependence. Robustness outputs include strict-valid-only analyses, raw/Jeffreys/Laplace source-community distribution checks, high-annotation-only checks, `info`-majority exclusion, high-`info` exclusion, leave-one-model-out summaries and model-level endpoint summaries. These checks support the direction of the main findings while preserving the primary status of the low-consensus endpoint definitions.

One dependence-aware robustness analysis was run on frozen low-consensus model-ready endpoint rows: model fixed effects plus item-cluster bootstrap uncertainty (4,000 iterations; seed `20260701`). The resulting estimates preserved sign and similar magnitude for all three endpoints: agreement surplus 0.370919 (95% CI, 0.360798-0.381290), distribution-agreement gap 0.232772 (95% CI, 0.224615-0.241494), and repeated forced-choice concentration 1.264638 bits (95% CI, 1.220329-1.307882). This is reported as robustness only and does not replace preregistered primary inference.

The corresponding derived output file is `post_run/analysis_exports/50k/model_fixed_effects_item_cluster_bootstrap_50k.csv`.

---

## Supplementary Note 8: Paraphrase audit and contamination limitation

The paraphrase audit uses paraphrased versions of a stratified item subset and is reported as aggregate surface-form evidence. Because original-vs-paraphrase matched coverage is limited, paraphrase results should not be framed as a definitive paired paraphrase test.

The paraphrase audit contained 2,500 target calls and 2,495 valid outputs. Within the limited matched original-vs-paraphrase overlap, coverage was 29 low-consensus rows and 15 diffuse rows; chosen-label stability was 0.655 in low-consensus rows and 0.467 in diffuse rows.

Contamination was not directly measured. The paraphrase audit addresses surface-form sensitivity rather than training-set membership.

---

## Supplementary Note 9: Distribution-quality diagnostics and baselines

Distribution-quality diagnostics include Jensen-Shannon divergence, total variation distance, entropy and Brier summaries by source-community disagreement bin and model. Baseline summaries include uniform, global-base-rate and source-majority-oracle comparisons.

These diagnostics assess whether distribution-mode outputs were non-degenerate and item-sensitive. They are support analyses, not a separate distribution-prediction benchmark and not a claim of perfect distribution calibration.

---

## Supplementary Note 10: Normative-certainty secondary analysis

Normative certainty is a secondary descriptive construct. It is not equivalent to estimated source-community agreement and is not a fourth primary endpoint. The corresponding source data are provided in `post_run/analysis_exports/50k/manuscript_tables/table_normative_certainty_50k.csv`.

---

## Supplementary Note 11: Analysis provenance

The inferential source for the Article is the frozen 50k analysis. Earlier cumulative records document collection monitoring and release provenance rather than independent replications. They do not substitute for the final analysis exports. The final analysis uses only the amended frozen five-model roster; run manifests and the Supplementary Information document the roster amendment and completion provenance.

---

## Supplementary Tables and source-data files

Supplementary Tables 1–8 are provided as accompanying source-data files. File paths are relative to the released repository/archive root. The listed files are derived analysis/source-data files and do not indicate unrestricted redistribution of raw SCRUPLES anecdotes, rendered prompts, raw provider responses or full run stores. All files listed here are releasable under CC-BY as derived outputs of the analysis. A file-level inventory is provided in `submission/source_data/INVENTORY.md`, and a column-level data dictionary is provided in `submission/source_data/DATA_DICTIONARY.md`.

| Supplementary Table | What it supports | Source data |
|---|---|---|
| Supplementary Table 1 | Full model roster, API parameters, model-level endpoints and leave-one-model-out summaries supporting model provenance and cross-model consistency checks. | `post_run/analysis_exports/50k/manuscript_tables/table_model_roster_50k.csv`; `post_run/analysis_exports/50k/model_level_endpoint_table_50k.csv`; `post_run/analysis_exports/50k/leave_one_model_out_50k.csv` |
| Supplementary Table 2 | Source-community distribution smoothing robustness showing whether endpoint directions depend on raw proportions, Jeffreys smoothing or Laplace smoothing. | `post_run/analysis_exports/50k/manuscript_tables/table_robustness_smoothing_50k.csv` |
| Supplementary Table 3 | Annotation-count and `info` robustness checks supporting the treatment of annotation density and the retained `info` label. | `post_run/analysis_exports/50k/manuscript_tables/table_robustness_annotation_info_50k.csv` |
| Supplementary Table 4 | Paraphrase-audit aggregate effects, confidence intervals, chosen-label stability and matched-coverage caveat. | `post_run/analysis_exports/50k/manuscript_tables/table_paraphrase_effects_50k.csv`; `post_run/analysis_exports/50k/manuscript_tables/table_paraphrase_ci_50k.csv` |
| Supplementary Table 5 | Distribution-quality diagnostics and baselines supporting non-degeneracy and item sensitivity of distribution-mode outputs. | `post_run/analysis_exports/50k/manuscript_tables/table_distribution_quality_50k.csv`; `post_run/analysis_exports/50k/manuscript_tables/table_baseline_distribution_quality_50k.csv` |
| Supplementary Table 6 | Normative-certainty summaries for the secondary descriptive construct. | `post_run/analysis_exports/50k/manuscript_tables/table_normative_certainty_50k.csv` |
| Supplementary Table 7 | Validity by model/mode, invalid-output categories, minimum validity rates, refusals, off-schema labels, API errors, terminal failures and repair fields. | `post_run/analysis_exports/50k/manuscript_tables/table_validity_by_model_mode_50k.csv`; `post_run/analysis_exports/50k/manuscript_tables/table_invalid_output_summary_50k.csv` |
| Supplementary Table 8 | Model-ready endpoint rows and dependence-aware robustness summary (model fixed effects plus item-cluster bootstrap) used as a sensitivity check, not as primary inference. | `post_run/analysis_exports/50k/model_ready/mixed_effects_endpoint_rows_50k.csv`; `post_run/analysis_exports/50k/model_ready/mixed_effects_endpoint_rows_strict_valid_50k.csv`; `post_run/analysis_exports/50k/model_fixed_effects_item_cluster_bootstrap_50k.csv` |

---

## Extended Data figures and source data

| Extended Data item | What it supports | Source data |
|---|---|---|
| Extended Data Fig. 1 | Distribution-quality diagnostics showing that distribution-mode outputs varied by item/bin and were not merely uniform or fixed base-rate responses. | `post_run/analysis_exports/50k/rendered_figures/figure_distribution_quality_distances_50k.svg`; `post_run/analysis_exports/50k/figure_ready/figure_distribution_quality_by_bin_model_50k.csv` |
| Extended Data Fig. 2 | Aggregate paraphrase-audit effects for agreement surplus and distribution-agreement gap, interpreted with the limited matched-coverage caveat. | `post_run/analysis_exports/50k/rendered_figures/figure_paraphrase_audit_effects_50k.svg`; `post_run/analysis_exports/50k/figure_ready/figure_paraphrase_effects_by_bin_model_50k.csv` |
| Extended Data Fig. 3 | Primary-valid output rates by model and prompt mode, supporting the validity and exclusion summary. | `post_run/analysis_exports/50k/rendered_figures/figure_validity_rate_by_model_50k.svg`; `post_run/analysis_exports/50k/figure_ready/figure_validity_by_model_mode_50k.csv` |
| Extended Data Table 1 | Validity by model/mode and invalid-output summary, including repair fields and exclusion categories. | `post_run/analysis_exports/50k/manuscript_tables/table_validity_by_model_mode_50k.csv`; `post_run/analysis_exports/50k/manuscript_tables/table_invalid_output_summary_50k.csv` |

---

## Public and restricted materials

Public derived/reviewable materials include manuscript-table CSVs, figure-ready CSVs, rendered figures, run manifests, release-safe prompt templates and schemas, analysis code, endpoint tables, bootstrap confidence intervals, adjusted tests, validity/exclusion summaries, robustness summaries, paraphrase summaries, distribution-quality diagnostics, baseline diagnostics and normative-certainty summaries. All items in this Supplementary Information file are derived outputs intended for open distribution under CC-BY.

Restricted or carefully shared materials include unredacted source anecdotes, rendered prompts containing anecdote text, raw model/provider responses, full call ledgers with text or API metadata, and full run stores if they contain restricted or mixed material. Restriction reasons include SCRUPLES dataset licence terms (Allen Institute for AI), model-provider terms of service, potential privacy or sensitivity considerations in the source community content, and institutional review constraints. These materials are shared only under applicable dataset terms, provider terms and non-redistribution conditions. Restricted verification materials can be provided to editors or reviewers upon reasonable request under appropriate non-redistribution conditions and applicable third-party terms. The data availability statement in the Article identifies what is public and what is restricted, together with the access route for restricted materials.
