# Stage 1b Figure Asset Audit: 50k NMI Manuscript

Date: 2026-06-25

Scope: existing figure asset validation and figure-plan lock for the Nature Machine Intelligence manuscript figure-design phase. This memo does not change numerical results, source CSVs, manuscript prose or rendered figures.

Primary manuscript file used: `article/nmi_moral_overresolution_draft_50k_v5.md`. The requested `nmi_moral_overresolution_draft_50k_latest.md` was not found. Support files inspected include `article/nmi_supplementary_information_50k_v2.md`, `drafts/nmi_handoff_summary_50k_2.md`, `drafts/reviews/_revision_plan_4.md`, `post_run/analysis_exports/50k/manuscript_results_summary_50k.md`, `post_run/archive_upload_inventory_50k.md`, `post_run/reproducibility_commands_50k.md`, `post_run/analysis_exports/50k/analysis_export_manifest_50k.json`, and relevant CSVs in `post_run/analysis_exports/50k/manuscript_tables/`.

NMI-style reference points used: Nature Machine Intelligence submission guidance says the manuscript file may include Figures and Extended Data, Extended Data display items provide essential background but are not main display items, figures should remain editable rather than flattened, figure legends should be brief and avoid methodological detail, and statistics source data are encouraged for relevant figures. See:

- `https://www.nature.com/natmachintell/submission-guidelines/preparing-your-submission`
- `https://www.nature.com/natmachintell/submission-guidelines/aip-and-formatting`

## 1. Concise Verdict

The existing quantitative figures are mostly ready scientifically, but not yet final-production ready.

The plotted data agree with the source CSVs and with the manuscript/Table 2 numerical claims. The main remaining blockers are production/package issues rather than scientific redesign: no PDF exports, no final packaged Fig. 1 export, no main Fig. 2-4 source-data mapping table in the SI, and no CI/error-bar fields in the figure-ready CSVs for the claim-bearing main figures. Fig. 4 also needs the unit "bits" in the y-axis label for final artwork.

No numerical result needs to change. No source CSV needs to change. Existing quantitative figures should only be regenerated if Stage 2 asks for production updates such as PDF export, CI/error-bar inclusion, tighter legends, and unit/label polish.

## 2. Asset Inventory Table

| Expected figure | Expected display role | Figure-ready CSV | Rendered SVG | Rendered PNG | PDF | Figure-generation script | Status |
|---|---|---|---|---|---|---|---|
| Main Fig. 1 | Study design / uncertainty-transfer schematic | Not applicable | Draft exists: `drafts/display_items/fig1_study_design.svg`; no final copy in `post_run/analysis_exports/50k/rendered_figures/` | Missing | Missing | Draft Mermaid source exists: `drafts/display_items/fig1_study_design.mmd`; no final package/export script found | Missing final package; draft exists |
| Main Fig. 2 | Agreement surplus | `post_run/analysis_exports/50k/figure_ready/figure_agreement_surplus_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/rendered_figures/figure_agreement_surplus_by_bin_model_50k.svg` | `post_run/analysis_exports/50k/rendered_figures/figure_agreement_surplus_by_bin_model_50k.png` | Missing | `src/analysis/final_50k_exports.py`; `src/analysis/render_final_figures.py` | Needs minor QA/regeneration for final production |
| Main Fig. 3 | Distribution-agreement gap | `post_run/analysis_exports/50k/figure_ready/figure_distribution_gap_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/rendered_figures/figure_distribution_gap_by_bin_model_50k.svg` | `post_run/analysis_exports/50k/rendered_figures/figure_distribution_gap_by_bin_model_50k.png` | Missing | `src/analysis/final_50k_exports.py`; `src/analysis/render_final_figures.py` | Needs minor QA/regeneration for final production |
| Main Fig. 4 | Sampling compression | `post_run/analysis_exports/50k/figure_ready/figure_sampling_compression_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/rendered_figures/figure_sampling_compression_by_bin_model_50k.svg` | `post_run/analysis_exports/50k/rendered_figures/figure_sampling_compression_by_bin_model_50k.png` | Missing | `src/analysis/final_50k_exports.py`; `src/analysis/render_final_figures.py` | Needs minor QA/regeneration for final production |
| Extended Data Fig. 1 | Distribution-quality diagnostics | `post_run/analysis_exports/50k/figure_ready/figure_distribution_quality_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/rendered_figures/figure_distribution_quality_distances_50k.svg` | `post_run/analysis_exports/50k/rendered_figures/figure_distribution_quality_distances_50k.png` | Missing | `src/analysis/final_50k_exports.py`; `src/analysis/render_final_figures.py` | Mostly ready; needs PDF/export package |
| Extended Data Fig. 2 | Paraphrase-audit aggregate effects | `post_run/analysis_exports/50k/figure_ready/figure_paraphrase_effects_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/rendered_figures/figure_paraphrase_audit_effects_50k.svg` | `post_run/analysis_exports/50k/rendered_figures/figure_paraphrase_audit_effects_50k.png` | Missing | `src/analysis/final_50k_exports.py`; `src/analysis/render_final_figures.py` | Mostly ready; needs PDF/export package and label polish |
| Extended Data Fig. 3 | Validity by model/mode | `post_run/analysis_exports/50k/figure_ready/figure_validity_by_model_mode_50k.csv` | `post_run/analysis_exports/50k/rendered_figures/figure_validity_rate_by_model_50k.svg` | `post_run/analysis_exports/50k/rendered_figures/figure_validity_rate_by_model_50k.png` | Missing | `src/analysis/final_50k_exports.py`; `src/analysis/render_final_figures.py` | Mostly ready; needs PDF/export package |

## 3. Source-Data Validation Table

| CSV | Rows | Key columns | Bins | Models | Endpoint names / units | Aggregate/model/CI support | Validation finding |
|---|---:|---|---|---|---|---|---|
| `figure_agreement_surplus_by_bin_model_50k.csv` | 30 | `disagreement_bin`, `endpoint`, `mean`, `model_id`, `n` | high, moderate, low, diffuse, low_diffuse | all_models plus five evaluated models | `agreement_surplus`, unitless proportion difference | Aggregate and model means present; CIs absent | Supports current bars and model points; CIs require `table_primary_results_with_ci_50k.csv` |
| `figure_distribution_gap_by_bin_model_50k.csv` | 30 | `disagreement_bin`, `endpoint`, `mean`, `model_id`, `n` | high, moderate, low, diffuse, low_diffuse | all_models plus five evaluated models | `distribution_agreement_gap`, unitless probability difference | Aggregate and model means present; CIs absent | Supports current bars and model points; CIs require `table_primary_results_with_ci_50k.csv` |
| `figure_sampling_compression_by_bin_model_50k.csv` | 30 | `disagreement_bin`, `endpoint`, `mean`, `model_id`, `n` | high, moderate, low, diffuse, low_diffuse | all_models plus five evaluated models | `sampling_compression`, bits | Aggregate and model means present; CIs absent | Supports current bars and model points; CIs require `table_primary_results_with_ci_50k.csv`; y-axis should say bits |
| `figure_distribution_quality_by_bin_model_50k.csv` | 24 | `mean_brier_majority_label`, `mean_jsd`, `mean_model_distribution_entropy`, `mean_total_variation_distance`, `model_id`, `n` | high, moderate, low, diffuse | all_models plus five evaluated models | JSD, total variation, entropy, Brier diagnostics | Aggregate and model summaries present; no CIs | Supports aggregate diagnostic display; model-level data are available but not plotted |
| `figure_paraphrase_effects_by_bin_model_50k.csv` | 24 | paraphrase aggregate means, matched overlap, stability | high, moderate, low, diffuse | all_models plus five evaluated models | agreement surplus and distribution-agreement gap in paraphrased items | Aggregate and model summaries present; no CIs in this CSV | Supports aggregate display; CIs require `table_paraphrase_ci_50k.csv`; matched overlap caveat present |
| `figure_validity_by_model_mode_50k.csv` | 30 | validity status counts, `prompt_mode`, `valid_primary`, `valid_primary_rate` | None | five evaluated models | validity rate by model/prompt mode | Model/mode rows present; no aggregate all_models row | Supports validity transparency display; not a primary claim figure |

Figs. 2-4 aggregate values match the manuscript/results summary/Table 2 values:

| Endpoint | Bin | Figure CSV mean | Manuscript/Table 2 value | 95% CI source |
|---|---|---:|---:|---|
| Agreement surplus | low_consensus | 0.370931 | 0.370931 | 0.361206-0.381114 |
| Agreement surplus | diffuse | 0.435619 | 0.435619 | 0.427337-0.444341 |
| Agreement surplus | high_consensus | 0.169409 | 0.169409 | 0.145651-0.194624 |
| Distribution-agreement gap | low_consensus | 0.232687 | 0.232687 | 0.224387-0.241341 |
| Distribution-agreement gap | diffuse | 0.226556 | 0.226556 | 0.216740-0.237164 |
| Distribution-agreement gap | high_consensus | 0.182842 | 0.182842 | 0.169762-0.196217 |
| Sampling compression | low_consensus | 1.264638 | 1.264638 | 1.218425-1.309054 |
| Sampling compression | diffuse | 1.507379 | 1.507379 | 1.452200-1.562768 |
| Sampling compression | high_consensus | 0.563708 | 0.563708 | 0.495005-0.633547 |

Low-consensus-minus-high-consensus contrasts are present in `post_run/analysis_exports/50k/manuscript_tables/table_primary_contrasts_with_ci_50k.csv`, not directly in the plotted figure-ready CSVs. That is acceptable because the current figures are bin-level displays and Table 2 carries contrasts.

## 4. Rendered-Figure Validation Table

All six quantitative SVGs open as vector drawings with zero embedded `<image>` tags. Matplotlib converted text to paths and retained label comments; PNGs are preview/export copies, not canonical editable source.

| Figure | Render validation | Axis/units | Bins/primary endpoint | Model points and CIs | Claim/design QA | Status |
|---|---|---|---|---|---|---|
| Fig. 2 agreement surplus | SVG and PNG present; PNG 1803 x 1056 | Y-axis says "Mean agreement surplus"; correct | High, Moderate, Low, Diffuse, Low + diffuse visible; low-consensus identifiable | Model points present; CIs/error bars absent | No provider-family or route-family comparison implied, but legend is large | Needs minor QA/regeneration before final |
| Fig. 3 distribution-agreement gap | SVG and PNG present; PNG 1803 x 1056 | Y-axis says "Mean distribution-agreement gap"; correct | Bin labels clear; central endpoint identifiable | Model points present; CIs/error bars absent | Correctly frames within-model gap; legend large but legible | Needs minor QA/regeneration before final |
| Fig. 4 sampling compression | SVG and PNG present; PNG 1803 x 1056 | Y-axis says "Source entropy minus sample entropy"; unit "bits" missing | Bin labels clear; low/diffuse pattern visible | Model points present; CIs/error bars absent | Correct endpoint, but unit omission matters | Needs minor QA/regeneration before final |
| Extended Data Fig. 1 distribution quality | SVG and PNG present; PNG 1628 x 1011 | Y-axis says "Distance from source distribution"; JSD/TV legend clear | High, Moderate, Low, Diffuse visible | Aggregate lines present; model-level data not plotted | Supports non-degeneracy/item sensitivity, not calibration | Mostly ready |
| Extended Data Fig. 2 paraphrase audit | SVG and PNG present; PNG 1716 x 1011 | Y-axis says "Mean effect" | High, Moderate, Low, Diffuse visible | Aggregate bars present; CIs absent from display | Supports aggregate surface-form evidence only; legend should spell "Distribution-agreement gap" | Mostly ready with label polish |
| Extended Data Fig. 3 validity | SVG and PNG present; PNG 1848 x 968 | Y-axis says "Mean valid rate across prompt modes" | Not bin-based | Model-level bars only | Supports validity/exclusion transparency, not primary scientific claim | Mostly ready with export polish |

## 5. Claim-to-Figure Alignment Map

| Claim | Figure/table support | Alignment |
|---|---|---|
| Agreement surplus is verdict agreement estimate minus source-community support for the selected label | Fig. 2, Table 2, `figure_agreement_surplus_by_bin_model_50k.csv`, `table_primary_results_with_ci_50k.csv` | Aligned |
| Distribution-agreement gap is verdict agreement estimate minus same model's distribution-mode probability for same item and selected label | Fig. 3, Table 2, `figure_distribution_gap_by_bin_model_50k.csv` | Aligned and correctly central |
| Fig. 3 is the central uncertainty-transfer/coherence endpoint | Main draft Results and caption emphasize same model, item, label and elicitation-format contrast | Aligned |
| Sampling compression is source-community entropy minus repeated-output entropy | Fig. 4, Table 2, `figure_sampling_compression_by_bin_model_50k.csv` | Aligned; figure y-axis should include bits |
| Distribution-quality diagnostics show non-degeneracy and item sensitivity, not perfect calibration | Extended Data Fig. 1 and SI text | Aligned |
| Paraphrase audit supports aggregate surface-form evidence only | Extended Data Fig. 2, Results caveat, SI Note 8 | Aligned |
| Validity display supports high validity and exclusion transparency | Extended Data Fig. 3, Extended Data Table 1, validity tables | Aligned |
| Provider/route/model-family comparisons are not claimed | Main draft, Table 1 caption, SI, and figures use model IDs without family grouping | Aligned |

No mismatch was found between the numerical claims and the plotted quantitative values. The main presentation mismatch is narrower: captions report CIs while current plotted figures do not show CI/error bars; this is defensible if CIs are treated as caption/Table 2 values, but a final NMI-style claim figure would be stronger with visible intervals or an explicit production decision not to plot intervals.

## 6. NMI-Style Alignment Assessment

The figure plan is logically aligned with the structure common to NMI Articles:

- A schematic first figure is appropriate because the design needs explanation across source-community distributions, prompt formats and endpoints.
- Figs. 2-4 are claim-bearing quantitative results and deserve main-figure status.
- Robustness, diagnostic and validity displays are correctly placed in Extended Data.
- Quantitative source CSVs exist for all plotted quantitative figures.
- Captions are concise and explain endpoints without becoming Methods sections.
- The current artwork is clean enough for review, but final production should improve interval display, PDF availability, legend scale and unit labels.

The plan should not imitate a decorative visual style. The right NMI-style move here is a clear schematic plus compact quantitative result figures with source data and editable vector exports.

## 7. Overclaim and Underclaim Guardrails

The current draft largely avoids the requested overclaims. These are the remaining wording/label risks and suggested corrections:

| Risk | Current/likely source | Safer wording |
|---|---|---|
| SCRUPLES labels as moral truth | Already controlled in main draft and SI | "source-community reference distributions from the SCRUPLES data-generating process, not moral truth" |
| Source community as universal/representative | Already controlled in main draft and SI | "SCRUPLES source-community" or "source-community judges"; avoid generic "humans" in technical claims |
| Contamination ruled out | Already controlled | "Contamination was not directly measured; the paraphrase audit addresses surface-form sensitivity rather than training-set membership" |
| Strong paired paraphrase robustness | Already controlled, but ED Fig. 2 caption should stay cautious | "aggregate paraphrase-audit effects, interpreted with limited matched original-vs-paraphrase coverage" |
| Provider/route/model-family claims | Figures show model IDs; no family grouping | "provider/route fields record provenance only and are not analysed as group effects" |
| Normative certainty as primary endpoint | Fig. 1 caption mentions it as secondary | "normative-certainty results are secondary descriptive evidence, not a primary endpoint" |
| High-consensus as null/unaffected condition | Current draft treats as positive reference | Keep "high-consensus reference condition" and "also positive but smaller" |
| Distribution mode perfectly recovered source distribution | Current draft mostly avoids this | "non-degenerate, item-sensitive distributions; not a perfect-calibration claim" |
| Temperature-0 repeated calls as latent model distribution | Current draft and SI already avoid this | "diversity across repeated fresh calls under the recorded prompt and label-order randomization protocol" |
| Ambiguous ED Fig. 2 legend "Distribution gap" | Rendered legend | Use "Distribution-agreement gap" |
| Missing Fig. 4 unit on y-axis | Rendered y-axis | Use "Source entropy minus repeated-output entropy (bits)" or "Sampling compression (bits)" |

## 8. Gap/Fix List, Prioritized

### Must fix before Stage 2

1. Lock Fig. 1 status: either promote `drafts/display_items/fig1_study_design.svg` into the final figure package or explicitly mark Fig. 1 as not yet produced. Current state is draft SVG/Mermaid only.
2. Add or plan PDF exports for all final figures. No figure PDFs were found.
3. Add a main Fig. 2-4 source-data mapping table in the SI or a standalone figure-source inventory. The SI currently maps Extended Data figures but not main Figs. 2-4.
4. Decide whether Figs. 2-4 should show CI/error bars. If yes, join figure rendering to `table_primary_results_with_ci_50k.csv` or equivalent; if no, explicitly lock Table 2/caption as the interval display.
5. Fix Fig. 4 unit label to include bits in final artwork.

### Should fix before final submission

1. Generate final SVG/PNG/PDF package in a single canonical folder for all main and Extended Data figures.
2. Add a caption/source-data consistency table covering every figure, source CSV, CI source, and caption-reported value.
3. Add a final export/package checklist with expected file names, formats and source-data files.
4. Reduce main-figure legend footprint and verify readability at likely journal column width.
5. Expand ED Fig. 2 legend/caption wording from "Distribution gap" to "Distribution-agreement gap".
6. Consider whether Extended Data Fig. 1 should mention that model-level summaries exist in source data even though the display is aggregate.

### Optional polish

1. Standardize short model labels for readability if the manuscript or legend defines the full IDs elsewhere.
2. Consider reordering main Fig. 2-4 bins to visually emphasize low-consensus primary and diffuse secondary evidence while preserving the positive high-consensus reference condition. Do this only if Stage 2 explicitly allows design changes.
3. Consider adding panel letters only if figures become multi-panel.

## 9. Locked Stage 1 Recommendation

Final main figure set:

1. Main Fig. 1: study design / uncertainty-transfer schematic.
2. Main Fig. 2: agreement surplus.
3. Main Fig. 3: distribution-agreement gap, central coherence endpoint.
4. Main Fig. 4: sampling compression.

Final Extended Data figure set:

1. Extended Data Fig. 1: distribution-quality diagnostics.
2. Extended Data Fig. 2: paraphrase-audit aggregate effects.
3. Extended Data Fig. 3: validity by model/mode.

Table recommendation: Table 1 and Table 2 should remain main display items. Table 1 carries model roster/target allocation and provenance guardrails; Table 2 carries endpoint estimates, contrasts, confidence intervals and adjusted tests that the current figures do not visually encode.

Fig. 1 recommendation: Fig. 1 is the only missing main figure in the final package, but a draft vector schematic exists at `drafts/display_items/fig1_study_design.svg`.

Quantitative-regeneration recommendation: no scientific regeneration is needed. A final production regeneration is recommended for Figs. 2-4 if Stage 2 wants visible CIs/error bars, PDF output, smaller legends and unit fixes. Extended Data figures require export/package polish rather than scientific redesign.

## 10. Stage 2 Readiness Checklist

- [x] Expected quantitative SVG/PNG assets found.
- [x] Expected figure-ready CSVs found.
- [x] Figure-generation scripts found: `src/analysis/final_50k_exports.py` and `src/analysis/render_final_figures.py`.
- [x] Figs. 2-4 aggregate means validated against manuscript/results summary/Table 2.
- [x] Low-consensus-minus-high-consensus contrasts verified in manuscript tables.
- [x] Rendered quantitative SVGs verified as vector, not raster-embedded.
- [x] Main and Extended Data figure roles checked against manuscript claims.
- [x] Overclaim guardrails checked.
- [ ] Final packaged Fig. 1 present in main figure folder.
- [ ] Figure PDFs exported.
- [ ] CI/error-bar display decision locked for Figs. 2-4.
- [ ] Main Fig. 2-4 source-data mapping added to SI or figure-source inventory.
- [ ] Caption/source-data consistency table created.
- [ ] Final export/package checklist created.

Stage 2 can proceed after the unchecked package/source-data items are assigned. It should not revisit study design or numerical results.
