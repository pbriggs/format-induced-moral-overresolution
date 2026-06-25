# Stage 2 Figure Production Decision Lock: Fig. 1 and Final Export Plan

Date: 2026-06-25

Controlling input: `post_run/analysis_exports/50k/figure_asset_audit_50k.md`.

Scope: Fig. 1 schematic finalization and production-decision lock. This memo does not change source CSVs, manuscript prose, numerical results, manuscript tables or rendered figures.

## 1. Concise Verdict

Fig. 1 draft should be replaced as final publication artwork, but it is usable as the content basis for the final schematic.

The current draft correctly identifies the source-community target, disagreement bins, matched item x model design, prompt formats and primary endpoints. It is editable SVG and contains no raw SCRUPLES anecdote text. However, it is too dense for a first-figure schematic because it includes audit scale, component allocation and supporting components inside the main flow. H1b, the distribution-agreement gap, is present but not visually privileged enough as the cleanest same-model, same-item, same-label uncertainty-transfer endpoint.

Stage 3 should produce a cleaner three-panel Fig. 1 as a hand-polished SVG or Python/Matplotlib-generated SVG/PDF/PNG. The existing Mermaid file can remain a planning source, but it should not be treated as final publication artwork.

## 2. Fig. 1 Draft Audit

Files located:

- `drafts/display_items/fig1_study_design.svg`
- `drafts/display_items/fig1_study_design.mmd`

No related Fig. 1 PNG, PDF or figure notes were found in the searched repository paths.

Draft SVG properties:

- Size: 1200 x 760 viewBox.
- Vector/editable: yes; no embedded `<image>` tags.
- Text: 44 SVG text elements.
- Structure: source-community target, disagreement bins, matched audit design, prompt formats, primary endpoints and supporting components.

Assessment:

| Criterion | Finding |
|---|---|
| Is it too dense? | Yes for final publication artwork. The call counts and component allocation compete with the conceptual flow. |
| Does it explain uncertainty transfer clearly? | Partly. It shows prompt formats and endpoints, but the cross-format comparison could be more direct. |
| Does it separate source distribution, prompt formats and endpoints? | Yes, but the layout reads as an audit map more than a schematic. |
| Does it make H1b legible as the cleanest endpoint? | Not enough. Distribution-agreement gap appears as one endpoint box but is not visually emphasized as same model, same item, same label. |
| Does it keep paraphrase and normative certainty secondary? | Mostly, but supporting components occupy a full prompt-format-region box and call-count lines, which gives them more visual weight than needed. |
| Does it avoid raw SCRUPLES anecdote text? | Yes. |
| Does it avoid moral-truth framing? | Yes; it says source-community votes and disagreement bins. |
| Does it avoid universal/representative source-community implications? | Yes; it uses source-community language. |
| Does it avoid treating normative certainty as primary? | Mostly, but final Fig. 1 should move normative certainty to a small support strip or omit it from the main flow. |

Decision: use the current draft as a content checklist, not as final artwork.

## 3. Final Fig. 1 Design Specification

Final Fig. 1 should be schematic-like, not a dense audit map. Recommended title:

`Study design for testing cross-format uncertainty transfer`

Recommended structure:

| Panel | Purpose | Required content | Visual emphasis |
|---|---|---|---|
| a | Source-community distribution and binning | Five-label source-community vote distribution; disagreement-bin logic: high, moderate, low, diffuse/no-clear-consensus | Show that SCRUPLES provides reference distributions, not moral truth. Avoid raw anecdote text. |
| b | Prompt-format comparison | Same item x same model is evaluated in distribution mode, descriptive verdict/agreement mode and repeated forced-choice mode | Make the matched design clear. Use arrows from one shared item-model unit to the three formats. |
| c | Endpoint definitions | Agreement surplus, distribution-agreement gap and sampling compression | Put distribution-agreement gap in the center or visually highlight it as same model, same item, same verdict-selected label across formats. |
| Footer/side strip | Secondary components | Paraphrase audit = aggregate surface-form support; normative certainty = secondary descriptive analysis | Smaller, visually subordinate, not connected as primary endpoints. |

Panel c endpoint wording:

- Agreement surplus: `verdict agreement estimate - source support for chosen label`.
- Distribution-agreement gap: `verdict agreement estimate - same model's distribution-mode probability for the same item and label`.
- Sampling compression: `source-community entropy - repeated-output entropy (bits)`.

Design guardrails:

- Do not include raw SCRUPLES anecdote text.
- Do not imply SCRUPLES labels are moral truth.
- Do not imply the source community is universal or representative.
- Do not make provider-family, route-family or model-family claims.
- Do not make normative certainty a primary endpoint.
- Do not include detailed target-call allocation in the main schematic; those details belong in Table 1/Methods.

Implementation recommendation:

- Prefer a hand-polished SVG or Python/Matplotlib-rendered vector schematic in Stage 3.
- Keep Mermaid only as a planning sketch unless the final SVG is manually simplified and polished.
- Export final Fig. 1 as SVG, PNG and PDF.

## 4. CI/Error-Bar Decision for Figs. 2-4

Decision: Option A - add visible aggregate 95% CI error bars to Figs. 2-4 where CIs are already available for `all_models`.

Rationale:

- Figs. 2-4 are claim-bearing main figures.
- Table 2 and captions already report exact CIs, but visible uncertainty intervals strengthen the figure.
- The required CI values are already present in `post_run/analysis_exports/50k/manuscript_tables/table_primary_results_with_ci_50k.csv`.
- Joining those CIs to the rendered figures does not change numerical results.

Implementation lock:

- Add error bars only for `all_models` aggregate bars/points.
- Use `table_primary_results_with_ci_50k.csv` as the sole CI source.
- Do not compute new CIs.
- Do not add model-level CIs; no model-level CI source is currently defined.
- Moderate-consensus rows in `table_primary_results_with_ci_50k.csv` have no CI values. Do not invent them. Either omit the CI for the moderate bar or caption that CIs are shown only where available from the primary CI table.
- Low+diffuse CIs are available and may be shown if the low+diffuse aggregate remains plotted as descriptive context.

## 5. Production-Fix List for Each Figure

| Figure | Required production fixes | Do not do |
|---|---|---|
| Main Fig. 1 | Replace dense draft with cleaner three-panel schematic; export SVG, PNG and PDF; keep source-community/prompt-format/endpoint separation; visually privilege H1b | Do not include raw anecdote text, target-call allocation clutter or normative certainty as a primary endpoint |
| Main Fig. 2 | Add aggregate 95% CI error bars where available; reduce legend footprint if needed; keep "agreement surplus" endpoint label clear; export PDF | Do not add model-level CIs or provider/model-family grouping |
| Main Fig. 3 | Add aggregate 95% CI error bars where available; keep distribution-agreement gap as central uncertainty-transfer endpoint in label/caption; export PDF | Do not frame as distribution-calibration benchmark |
| Main Fig. 4 | Add aggregate 95% CI error bars where available; change y-axis to include bits, preferably `Sampling compression (bits)` or `Source-community entropy - repeated-output entropy (bits)`; export PDF | Do not imply repeated temperature-0 calls estimate a latent model distribution |
| Extended Data Fig. 1 | Export PDF; keep aggregate diagnostic framing | Do not imply perfect calibration or distribution recovery |
| Extended Data Fig. 2 | Change legend from `Distribution gap` to `Distribution-agreement gap`; export PDF | Do not imply strong paired paraphrase robustness or contamination exclusion |
| Extended Data Fig. 3 | Export PDF; keep validity/exclusion transparency framing | Do not make validity a primary scientific endpoint |
| All figures | Preserve SVG/vector editability; keep PNG as preview/export; use PDF for package completeness | Do not flatten SVG text/labels into raster images |

## 6. Main Fig. 2-4 Source-Data Mapping Table

This table should be added to the SI or a standalone figure-source inventory in Stage 3.

| Main figure | Role | Render/source CSV | CI/statistical table | Contrast table |
|---|---|---|---|---|
| Fig. 2 | Agreement surplus | `post_run/analysis_exports/50k/figure_ready/figure_agreement_surplus_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/manuscript_tables/table_primary_results_with_ci_50k.csv` | `post_run/analysis_exports/50k/manuscript_tables/table_primary_contrasts_with_ci_50k.csv` |
| Fig. 3 | Distribution-agreement gap | `post_run/analysis_exports/50k/figure_ready/figure_distribution_gap_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/manuscript_tables/table_primary_results_with_ci_50k.csv` | `post_run/analysis_exports/50k/manuscript_tables/table_primary_contrasts_with_ci_50k.csv` |
| Fig. 4 | Sampling compression | `post_run/analysis_exports/50k/figure_ready/figure_sampling_compression_by_bin_model_50k.csv` | `post_run/analysis_exports/50k/manuscript_tables/table_primary_results_with_ci_50k.csv` | `post_run/analysis_exports/50k/manuscript_tables/table_primary_contrasts_with_ci_50k.csv` |

Extended Data source-data map check:

- Existing SI maps Extended Data Fig. 1 to `figure_distribution_quality_distances_50k.svg` and `figure_distribution_quality_by_bin_model_50k.csv`; no mismatch.
- Existing SI maps Extended Data Fig. 2 to `figure_paraphrase_audit_effects_50k.svg` and `figure_paraphrase_effects_by_bin_model_50k.csv`; add `post_run/analysis_exports/50k/manuscript_tables/table_paraphrase_ci_50k.csv` if the Extended Data caption or source inventory reports paraphrase CIs.
- Existing SI maps Extended Data Fig. 3 to `figure_validity_rate_by_model_50k.svg` and `figure_validity_by_model_mode_50k.csv`; no mismatch. Extended Data Table 1 already maps to validity and invalid-output summaries.

## 7. Files That Should Be Generated in Stage 3

Recommended final asset outputs:

- `post_run/analysis_exports/50k/rendered_figures/figure_study_design_50k.svg`
- `post_run/analysis_exports/50k/rendered_figures/figure_study_design_50k.png`
- `post_run/analysis_exports/50k/rendered_figures/figure_study_design_50k.pdf`
- PDF siblings for all six quantitative figures currently in `post_run/analysis_exports/50k/rendered_figures/`

Recommended production/support artifacts:

- Updated or new Fig. 1 rendering source, for example `src/analysis/render_fig1_schematic.py` or a documented hand-polished SVG source.
- Updated `src/analysis/render_final_figures.py` if Stage 3 implements aggregate CI error bars, Fig. 4 unit fix, ED Fig. 2 legend text and PDF export.
- A figure-source inventory, for example `post_run/analysis_exports/50k/figure_source_inventory_50k.md`.
- A final export/package checklist, for example `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`.

## 8. Files Not To Change

Do not change these files in Stage 3 unless the user explicitly asks for a manuscript/source-data edit:

- `post_run/analysis_exports/50k/figure_ready/*.csv`
- `post_run/analysis_exports/50k/manuscript_tables/*.csv`
- `post_run/analysis_exports/50k/manuscript_results_summary_50k.md`
- `article/nmi_moral_overresolution_draft_50k_v5.md`
- `article/nmi_supplementary_information_50k_v2.md`, unless the specific Stage 3 task is to add the source-data mapping table
- raw SCRUPLES data files
- raw rendered prompts
- raw provider/model responses
- full run databases or call ledgers

Do not regenerate all analysis exports. Do not rerun provider calls. Do not alter model roster, endpoint definitions, bootstrap values or contrast values.

## 9. Stage 3 Readiness Checklist

- [x] Stage 1b QA memo reviewed.
- [x] Current Fig. 1 draft SVG and Mermaid source inspected.
- [x] Fig. 1 final-artwork decision locked: replace final artwork, retain draft as content basis.
- [x] Final Fig. 1 panel structure specified.
- [x] CI/error-bar decision locked: add aggregate all-model CIs where already available; no model-level CIs; no new CIs.
- [x] Fig. 4 unit fix locked.
- [x] ED Fig. 2 legend wording fix locked.
- [x] PDF export requirement locked for all figures.
- [x] Main Fig. 2-4 source-data mapping specified.
- [x] Extended Data source-data map checked.
- [ ] Stage 3 figure-rendering implementation approved.
- [ ] Final Fig. 1 artwork generated.
- [ ] Quantitative figures regenerated only for production fixes.
- [ ] SVG/PNG/PDF final package verified.
- [ ] Figure-source inventory and final export checklist created.

Stage 3 should implement the locked production fixes without changing the study, source CSVs, numerical results or manuscript prose.
