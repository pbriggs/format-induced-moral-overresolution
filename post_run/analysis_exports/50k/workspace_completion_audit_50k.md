# Workspace Completion Audit: 50k NMI Manuscript

Date: 2026-06-25

Scope: audit-only pass for the `format-induced-moral-overresolution` workspace. This memo inspects manuscript, Supplementary Information, figure assets, source data, references, LaTeX readiness and packaging readiness. No files were moved, renamed, deleted or regenerated during this audit; the only file changed is this memo.

## 1. Concise verdict

**Nearly ready for LaTeX.**

The scientific manuscript package is largely complete enough to begin LaTeX conversion planning: the current main manuscript and SI are present, the final rendered figure package contains all expected main and Extended Data figures in SVG, PNG and PDF formats, source-data mappings are documented, and the tracked tree is clean.

The package is not yet fully submission-packaged because:

- no BibTeX file exists;
- no LaTeX workspace, template class, `main.tex`, `.bbl` or build script exists;
- the current manuscript references are embedded as numbered Markdown references;
- the proposed `paper/` directory is currently ignored by `.gitignore`, so `submission/` is cleaner unless the ignore rule is intentionally changed.

Live NMI pages checked during this audit:

- `https://www.nature.com/natmachintell/content`
- `https://www.nature.com/natmachintell/submission-guidelines/initial-formatting`

## 2. Current canonical manuscript and SI files

Current main manuscript:

- `article/nmi_moral_overresolution_draft_50k_v5.md`
- Size: 48,191 bytes
- Modified: 2026-06-25 11:57:10
- Abstract word count: 149 words

Current Supplementary Information:

- `article/nmi_supplementary_information_50k_v2.md`
- Size: 22,880 bytes
- Modified: 2026-06-24 17:43:47

Expected duplicate/candidate checks:

- `nmi_moral_overresolution_draft_50k_latest.md`: not found.
- root-level `nmi_supplementary_information_50k_v2.md`: not found.
- `drafts/nmi_moral_overresolution_draft_50k_4.md`: exists, older draft/local-only.
- `drafts/nmi_supplementary_information_50k.md`: exists, older draft/local-only.

Recommendation:

- Treat the two files in `article/` as current canonical source text for conversion.
- Later, create clearer canonical filenames in a clean package area, for example `submission/manuscript.md` and `submission/supplementary_information.md`, without changing the current article files until explicitly requested.

## 3. Current repo and workspace state

Git status:

- Branch: `main...origin/main`
- Before this memo update, the tracked tree was clean.
- After this memo update, the only tracked modification is `post_run/analysis_exports/50k/workspace_completion_audit_50k.md`.
- `git status --short --branch --ignored` also reports ignored/local-only directories.
- Warning observed: `could not open directory '.tmp_pytest/': Permission denied`.

Ignored/local-only material:

- `drafts/`: ignored; 50 files, about 1.4 MB.
- `runs/`: ignored; 2,967 files, about 4.78 GB.
- `data/scruples/`: ignored; three SCRUPLES JSONL files, about 74.96 MB.
- `__pycache__/` and `.tmp_pytest/`: runtime/cache only.
- `paper/`: ignored by `.gitignore`.

Local style-reference images:

- `drafts/style_reference/nmi_figures/42256_2022_536_Fig2_HTML.webp`
- `drafts/style_reference/nmi_figures/42256_2024_963_Fig3_HTML.webp`
- `drafts/style_reference/nmi_figures/42256_2024_976_Fig1_HTML.webp`
- `drafts/style_reference/nmi_figures/README.md`

These should remain local-only and should not be committed unless the author explicitly changes the policy.

## 4. Current figure package status

Final rendered figure directory:

- `post_run/analysis_exports/50k/rendered_figures/`

Rendering script:

- `src/analysis/render_final_figures.py`

Figure source inventory:

- `post_run/analysis_exports/50k/figure_source_inventory_50k.md`

Final export checklist:

- `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`

All expected rendered figures exist in SVG, PNG and PDF:

| Role | Rendered assets | Source CSV | Script |
|---|---|---|---|
| Fig. 1 study design | `figure_study_design_50k.{svg,png,pdf}` | not applicable | `src/analysis/render_final_figures.py` |
| Fig. 2 agreement surplus | `figure_agreement_surplus_by_bin_model_50k.{svg,png,pdf}` | `figure_ready/figure_agreement_surplus_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Fig. 3 distribution-agreement gap | `figure_distribution_gap_by_bin_model_50k.{svg,png,pdf}` | `figure_ready/figure_distribution_gap_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Fig. 4 sampling compression | `figure_sampling_compression_by_bin_model_50k.{svg,png,pdf}` | `figure_ready/figure_sampling_compression_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Extended Data Fig. 1 distribution quality | `figure_distribution_quality_distances_50k.{svg,png,pdf}` | `figure_ready/figure_distribution_quality_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Extended Data Fig. 2 paraphrase audit | `figure_paraphrase_audit_effects_50k.{svg,png,pdf}` | `figure_ready/figure_paraphrase_effects_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Extended Data Fig. 3 validity | `figure_validity_rate_by_model_50k.{svg,png,pdf}` | `figure_ready/figure_validity_by_model_mode_50k.csv` | `src/analysis/render_final_figures.py` |

Asset checks:

- All SVG, PNG and PDF files are non-empty.
- All PDFs have `%PDF-` headers.
- Search found no `<image>`, `base64` or `data:image` references in the rendered SVGs, so the SVGs appear vector/editable rather than raster-embedded.
- `quantitative_figure_numerical_validation_50k.txt` records PNG dimensions/DPI, SVG raster checks and PDF header checks.
- `figure_study_design_50k_layout_qa.txt` reports 0 text overlaps, 0 text-box border collisions and 0 sampled arrow-text collisions; it still notes that a manual visual check is required after render.

Polished endpoint-figure checks:

- Aggregate all-model bars are retained in Figs. 2-4.
- Aggregate CI/error bars are retained where available in Figs. 2-4.
- Model-level points are retained.
- Model colors and markers are centrally defined in `src/analysis/render_final_figures.py`.
- Fig. 4 uses `Sampling compression (bits)`.
- Fig. 3 and Extended Data Fig. 2 use `Distribution-agreement gap`, not `Distribution gap`.

One nuance:

- Older audit and production-decision notes, especially `figure_asset_audit_50k.md` and `figure_production_decision_lock_50k.md`, contain pre-polish statements that PDFs, Fig. 4 unit wording or the Extended Data Fig. 2 label still needed work. These appear superseded by the current rendered files, `final_figure_export_checklist_50k.md` and `quantitative_figure_numerical_validation_50k.txt`.

## 5. Source-data and numerical traceability status

Main Figs. 2-4:

- Fig. 2 source CSV: `post_run/analysis_exports/50k/figure_ready/figure_agreement_surplus_by_bin_model_50k.csv`
- Fig. 3 source CSV: `post_run/analysis_exports/50k/figure_ready/figure_distribution_gap_by_bin_model_50k.csv`
- Fig. 4 source CSV: `post_run/analysis_exports/50k/figure_ready/figure_sampling_compression_by_bin_model_50k.csv`
- CI table: `post_run/analysis_exports/50k/manuscript_tables/table_primary_results_with_ci_50k.csv`
- Contrast table: `post_run/analysis_exports/50k/manuscript_tables/table_primary_contrasts_with_ci_50k.csv`

Traceability findings:

- All all-model means in Figs. 2-4 match the corresponding figure-ready CSV rows.
- All all-model means also match `table_primary_results_with_ci_50k.csv`.
- CIs are read from `table_primary_results_with_ci_50k.csv`; no new CIs were computed for figure polish.
- Moderate-consensus rows have means but no CI bounds in the table, and the figure/checklist correctly state that no invented CIs were added.
- Figure-ready CSVs and manuscript tables have 2026-06-21 timestamps, while polished rendered figures and validation notes have 2026-06-24 timestamps, consistent with figure polish not changing source CSVs or manuscript tables.

Extended Data traceability:

- Extended Data Fig. 1 maps to `figure_distribution_quality_by_bin_model_50k.csv`, `table_distribution_quality_50k.csv` and `table_baseline_distribution_quality_50k.csv`.
- Extended Data Fig. 2 maps to `figure_paraphrase_effects_by_bin_model_50k.csv`, `table_paraphrase_effects_50k.csv` and `table_paraphrase_ci_50k.csv`.
- Extended Data Fig. 3 maps to `figure_validity_by_model_mode_50k.csv`, `table_validity_by_model_mode_50k.csv` and `table_invalid_output_summary_50k.csv`.

Status:

- Source-data and numerical traceability are strong enough for LaTeX conversion.
- Keep `figure_source_inventory_50k.md`, `final_figure_export_checklist_50k.md` and `quantitative_figure_numerical_validation_50k.txt` as the controlling audit records.

## 6. Caption and cross-reference status

Main manuscript captions/callouts are present for:

- Fig. 1
- Fig. 2
- Fig. 3
- Fig. 4
- Table 1
- Table 2
- Extended Data Fig. 1
- Extended Data Fig. 2
- Extended Data Fig. 3
- Extended Data Table 1

Alignment checks:

- Fig. 3 is described as the same model, same item and same selected/verdict label.
- Fig. 4 is described in bits.
- Low-consensus is described as primary.
- Diffuse/no-clear-consensus is described as secondary and separate.
- High-consensus is described as a positive reference condition, not a null or unaffected condition.
- Distribution diagnostics are described as support/diagnostics, not proof of perfect calibration.
- Paraphrase is described as aggregate surface-form evidence with limited matched coverage, not as contamination exclusion or strong paired robustness.
- Validity is described as supporting transparency/exclusions, not a primary endpoint.

Current NMI fit note:

- The abstract is 149 words, within the live NMI Article limit of up to 150 words.

## 7. Claim-discipline guardrails

Searches covered the manuscript, SI, captions, figure inventory and 50k notes for wording that could imply overclaims. Most hits are explicit caveats rather than problems.

Controlled/correct caveat examples:

- `article/nmi_moral_overresolution_draft_50k_v5.md`: SCRUPLES distributions are framed as source-community reference distributions, not moral truth, universal norms, representative population estimates or deployment-ready standards.
- `article/nmi_moral_overresolution_draft_50k_v5.md`: high-consensus items are described as a positive reference condition.
- `article/nmi_moral_overresolution_draft_50k_v5.md`: repeated forced-choice outputs are described as protocol outputs, not stochastic samples from an internal model distribution.
- `article/nmi_moral_overresolution_draft_50k_v5.md`: contamination was not directly measured.
- `article/nmi_supplementary_information_50k_v2.md`: paraphrase audit is aggregate surface-form evidence, not definitive paired paraphrase testing.
- `post_run/analysis_exports/50k/figure_source_inventory_50k.md`: guardrails for all seven figures are explicit.

No current manuscript/SI wording was found that appears to claim:

- SCRUPLES labels are moral truth;
- the source community is universal or representative;
- contamination was ruled out;
- paraphrase is strong paired robustness;
- provider-family, route-family or model-family effects;
- normative certainty is a primary endpoint;
- high-consensus is a null/unaffected condition;
- distribution mode perfectly recovered the source-community distribution;
- repeated temperature-0 calls estimate a latent model distribution.

Audit-note nuance:

- `post_run/analysis_exports/50k/figure_production_decision_lock_50k.md` and older draft/review files contain guardrail phrasing and "do not" lists. They are useful audit history, not submission prose.

## 8. Bibliography and references readiness

Findings:

- No `.bib` file found.
- No `.bbl` file found.
- No `main.tex`, `sn-jnl.cls`, `.bst`, `.csl` or LaTeX folder found.
- References are embedded in `article/nmi_moral_overresolution_draft_50k_v5.md` as numbered Markdown references `[1-8]`.
- No Pandoc citation keys such as `[@key]` were found in the current manuscript or SI.
- No obvious `TODO`, `TBD`, `PLACEHOLDER`, `CITE` or `citation needed` markers were found in the current manuscript or SI.

Needed before LaTeX conversion:

- Create `references.bib`.
- Convert the eight numbered Markdown references to BibTeX entries.
- Choose stable citation keys and replace numbered bracket citations with LaTeX/BibTeX-compatible citations, or preserve current numbering carefully during conversion if using manual `thebibliography`.
- Verify reference metadata during the bibliography pass.

## 9. LaTeX readiness status

Findings:

- No LaTeX workspace exists.
- No `main.tex` exists.
- No Nature/Springer class file such as `sn-jnl.cls` exists.
- No compiled manuscript PDF exists.
- No Pandoc conversion script exists.
- No bibliography build outputs exist.

Live NMI initial-formatting page says initial submission does not need special formatting if suitable for editorial assessment and peer review, and accepts PDF, Word or TeX/LaTeX formats; TeX/LaTeX submissions should include compiled PDFs.

Recommendation:

- Begin LaTeX setup after creating the clean package root and bibliography file.
- Create a clean package workspace with manuscript, SI, figures, source data and bibliography rather than converting in place.
- Word and PDF candidates may be useful for initial submission, but a LaTeX candidate is reasonable now because the figure and source-data package is stable.

## 10. Recommended folder/package structure

The proposed structure is conceptually sound, but the root name should be adjusted.

Recommendation: use `submission/`, not `paper/`, for the next clean package.

Reasons:

- `.gitignore` currently ignores `paper/`.
- `article/` already holds the current canonical Markdown drafts and should remain a source-text area.
- `submission/` clearly separates a curated journal package from historical drafts, raw data, large runs and audit notes.

Recommended next structure:

```text
submission/
  manuscript.md
  supplementary_information.md
  references.bib
  figures/
    src/
      fig1_study_design.py
      fig2_agreement_surplus.py
      fig3_distribution_agreement_gap.py
      fig4_sampling_compression.py
    editable/
      fig1_study_design.svg
      fig2_agreement_surplus.svg
      fig3_distribution_agreement_gap.svg
      fig4_sampling_compression.svg
      edfig1_distribution_quality.svg
      edfig2_paraphrase_audit.svg
      edfig3_validity.svg
    final/
      fig1_study_design.pdf
      fig1_study_design.svg
      fig2_agreement_surplus.pdf
      fig2_agreement_surplus.svg
      fig3_distribution_agreement_gap.pdf
      fig3_distribution_agreement_gap.svg
      fig4_sampling_compression.pdf
      fig4_sampling_compression.svg
      edfig1_distribution_quality.pdf
      edfig1_distribution_quality.svg
      edfig2_paraphrase_audit.pdf
      edfig2_paraphrase_audit.svg
      edfig3_validity.pdf
      edfig3_validity.svg
  latex/
    main.tex
    references.bib
    bibliography.bbl
  source_data/
    figure_source_inventory_50k.md
    relevant_figure_ready_csvs/
    relevant_manuscript_tables/
```

Notes:

- Include both SVG and PDF for Extended Data final figures, not only PDF.
- Keep PNGs available for previews, but PDFs/SVGs should be the editable/final submission assets.
- Do not copy local style-reference images into `submission/`.
- If the author strongly prefers `paper/`, first change `.gitignore` intentionally or use a force-add policy and document it.

## 11. Done

Items that appear complete and should be frozen:

- Current main manuscript in `article/nmi_moral_overresolution_draft_50k_v5.md`.
- Current SI in `article/nmi_supplementary_information_50k_v2.md`.
- Final rendered figure package in `post_run/analysis_exports/50k/rendered_figures/`.
- Figure source inventory in `post_run/analysis_exports/50k/figure_source_inventory_50k.md`.
- Final figure export checklist in `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`.
- Quantitative figure numerical validation in `post_run/analysis_exports/50k/quantitative_figure_numerical_validation_50k.txt`.
- Figure-ready CSVs in `post_run/analysis_exports/50k/figure_ready/`.
- Manuscript tables in `post_run/analysis_exports/50k/manuscript_tables/`.
- 50k analysis manifest and derived analysis exports.
- Figure rendering source in `src/analysis/render_final_figures.py`.

## 12. Needs small fix before LaTeX

- Decide whether to create canonical package filenames under `submission/`.
- Create `references.bib`; this is the main missing pre-conversion artifact.
- Confirm that older pre-polish audit notes will not be treated as controlling over the final checklist.
- Optionally do one final manual visual review of all rendered PDFs/SVGs, especially Fig. 1, because the QA file still says manual visual check is required.

## 13. Needs LaTeX setup

- Create `submission/latex/` or another clean LaTeX workspace.
- Create `main.tex`.
- Add the selected Nature/Springer template/class files if needed.
- Create `references.bib`.
- Convert numbered Markdown references to citation keys or a controlled manual bibliography.
- Add figure inclusion paths for the final PDFs/SVGs.
- Build and inspect a compiled PDF.

## 14. Needs submission package later

- Cover letter, currently only as ignored/local draft: `drafts/nmi_cover_letter_50k.md`.
- Submission checklist, currently ignored/local: `drafts/nmi_submission_checklist_custom.md`.
- Journal upload manifest.
- Final source-data package mapping.
- Final data/code availability text matched to the uploaded archive/release.
- Any required author forms, reporting summaries or editorial declarations.
- Word/PDF version if the author chooses an initial-submission format outside LaTeX.

## 15. Do not touch

Unless explicitly instructed later, do not modify:

- `data/scruples/`
- `runs/`
- `drafts/style_reference/`
- `drafts/` historical review/planning files
- raw provider responses, full run stores or restricted materials
- figure-ready CSVs
- manuscript-table CSVs
- final rendered figure assets
- current canonical manuscript/SI text
- source analysis code

## 16. Files that should be committed

Tracked package files that should remain committed:

- `article/nmi_moral_overresolution_draft_50k_v5.md`
- `article/nmi_supplementary_information_50k_v2.md`
- `src/analysis/render_final_figures.py`
- `src/analysis/final_50k_exports.py`
- `post_run/analysis_exports/50k/figure_ready/*.csv`
- `post_run/analysis_exports/50k/manuscript_tables/*.csv`
- `post_run/analysis_exports/50k/rendered_figures/*.{svg,png,pdf}`
- `post_run/analysis_exports/50k/figure_source_inventory_50k.md`
- `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`
- `post_run/analysis_exports/50k/quantitative_figure_numerical_validation_50k.txt`
- `post_run/analysis_exports/50k/quantitative_figure_polish_implementation_50k.md`
- `post_run/analysis_exports/50k/analysis_export_manifest_50k.json`
- `post_run/analysis_exports/50k/workspace_completion_audit_50k.md`

Future files to commit after explicit creation:

- `submission/manuscript.md`
- `submission/supplementary_information.md`
- `submission/references.bib`
- `submission/latex/main.tex`
- selected LaTeX template/class files if redistribution is permitted
- curated submission figures and source-data copies

## 17. Files that should stay untracked/ignored

- `drafts/style_reference/nmi_figures/*.webp`
- other files under `drafts/` unless explicitly promoted
- `runs/`
- `data/scruples/`
- `.tmp_pytest/`
- `__pycache__/`
- `.env` and `.env.*` except `.env.example`
- raw provider responses, full call ledgers, full run stores and restricted/mixed materials

## 18. Files not to modify

Do not modify these in the next packaging step unless the task explicitly asks for it:

- `article/nmi_moral_overresolution_draft_50k_v5.md`
- `article/nmi_supplementary_information_50k_v2.md`
- `post_run/analysis_exports/50k/figure_ready/*.csv`
- `post_run/analysis_exports/50k/manuscript_tables/*.csv`
- `post_run/analysis_exports/50k/rendered_figures/*`
- `src/analysis/render_final_figures.py`
- `src/analysis/final_50k_exports.py`
- `data/scruples/*`
- `runs/*`
- `drafts/style_reference/*`

## 19. Prioritized next steps

1. Create `references.bib` from the eight embedded Markdown references and choose stable citation keys.
2. Create `submission/` as the clean package root, not `paper/`, unless `.gitignore` is intentionally changed.
3. Copy current canonical manuscript/SI, final figures, figure inventory and relevant source-data tables into `submission/`.
4. Convert the manuscript and SI to LaTeX in `submission/latex/`.
5. Build and inspect a compiled PDF.
6. Prepare cover letter and final submission checklist after the LaTeX/PDF build works.

## 20. Clear recommendation for the next Codex task

Next Codex task:

> Create `submission/` as a clean package root, copy the canonical manuscript/SI and final figure/source-data assets into it, and create an initial `references.bib` from the eight numbered references. Then start LaTeX conversion in `submission/latex/`.

Rationale:

- The figure package is ready enough to freeze.
- The source-data mapping is ready enough to copy.
- The biggest blockers to LaTeX conversion are bibliographic structure and clean package layout, not analysis, figure regeneration or abstract length.
