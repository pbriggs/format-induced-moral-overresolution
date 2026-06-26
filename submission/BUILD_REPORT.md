# Build Report

Generated from canonical manuscript source `article/nmi_moral_overresolution_draft_50k_v5.md`.

Build/audit timestamp: 2026-06-25 23:26:43 -07:00.

## Command Used

Run from `submission/latex/`:

```bat
cmd /c sync_build_open.bat
```

`sync_build_open.bat` now prepends the local MiKTeX binary directory when available, regenerates `main.tex`, runs two `pdflatex` passes for `main.tex`, runs two `xelatex` passes for `supplementary_information.tex`, and opens the generated PDFs.

## Build Status

- `latex/main.pdf`: built successfully, 24 pages, includes the seven verified figure PDFs.
- `latex/supplementary_information.pdf`: built successfully, 12 pages.
- `submission/manuscript.md`: refreshed from the canonical manuscript source and verified hash-identical.
- Abstract length corrected for NMI readiness; current abstract is 150 words by the local package audit count.
- Table 1 display-count ambiguity resolved: model roster and target allocation now appear under one Table 1 caption with internal panels `a, Model roster and collection windows` and `b, Target allocation by study component`.
- Fatal errors: none.
- Missing figure files: none.
- Undefined references/citations found in logs: none.
- MiKTeX update warnings: present, nuisance only; they did not block compilation.
- Supplementary Information font setup was simplified: explicit `fontspec` and `microtype` loads were removed.
- `submission/` is not ignored by `.gitignore`.

## Figure Inclusion Status

`latex/main.tex` includes real `\includegraphics` blocks for:

- Fig. 1: `../figures/final/figure_study_design_50k.pdf`
- Fig. 2: `../figures/final/figure_agreement_surplus_by_bin_model_50k.pdf`
- Fig. 3: `../figures/final/figure_distribution_gap_by_bin_model_50k.pdf`
- Fig. 4: `../figures/final/figure_sampling_compression_by_bin_model_50k.pdf`
- Extended Data Fig. 1: `../figures/final/figure_distribution_quality_distances_50k.pdf`
- Extended Data Fig. 2: `../figures/final/figure_paraphrase_audit_effects_50k.pdf`
- Extended Data Fig. 3: `../figures/final/figure_validity_rate_by_model_50k.pdf`

Editable SVGs for the same seven figures are included under `figures/editable/`.

## Table Status

- Table 1 and Table 2 are present in `latex/main.tex`.
- Table 1 is one main display item with two internal panels:
  - `a, Model roster and collection windows`
  - `b, Target allocation by study component`
- The Table 1 panels and Table 2 are rendered in landscape `longtable` blocks.
- Table values were not changed.
- Table captions and table references remain intact.

## Source Data Status

Release-facing derived source data were copied under `source_data/`:

- `figure_ready/`: figure-ready CSVs for all quantitative figures.
- `manuscript_tables/`: manuscript and supplementary table CSVs.
- `endpoint_summaries/`: endpoint, CI, leave-one-model-out, diagnostic and result summary files.
- `robustness/`: smoothing, annotation/info and baseline robustness summaries.
- `validity/`: validity and invalid-output summaries.

## Missing Assets

No required Fig. 1-4 or Extended Data Fig. 1-3 PDF/SVG assets were missing. No required derived source-data class requested for this package was missing.

## Warnings Requiring Author Attention

The PDF builds, but the logs contain layout warnings that should be visually reviewed:

- `main.log` line 45-46, page 2: 6.13116 pt overfull in the agreement-surplus paragraph, caused by the long phrase `source-community` in a dense results paragraph.
- `main.log` line 69-70, page 3: 9.63971 pt overfull in the cross-model pattern paragraph, caused by long endpoint phrases such as `Low-consensus distribution-agreement`.
- `main.log` line 71-72, page 4: 1.62645 pt and 19.05746 pt overfull boxes in the output-validity paragraph, caused by compact validity/status wording such as `strict-schema` and `extracted-JSON`.
- `main.log` line 75-76, page 4: 5.55223 pt overfull in the robustness paragraph, caused by long compound phrases such as `reference-distribution` and `item-composition`.
- `main.log` line 404-405, page 23: 12.4355 pt overfull in the Extended Data Table 1 caption, caused by a long caption/title line.
- `supplementary_information.log` line 95-96, page 3: underfull boxes involving inline schema field names such as `label_probabilities`, `most_likely_label` and `chosen_label`.

No content or numerical result was changed to address these layout warnings. The warnings are from dense text/code-token wrapping rather than missing files, unresolved references or figure path failures.

## Figure Readability Status

- Fig. 1-4 are included in `latex/main.pdf` using vector PDF assets from `figures/final/`.
- The LaTeX log confirms the expected final PDFs are included for Fig. 1-4 and Extended Data Fig. 1-3.
- Matching editable SVG assets are present for all seven figures under `figures/editable/`.
- No missing, raster-only or clipped figure file was detected from the build logs or asset inventory. Final visual legibility should still be checked in the PDF viewer before upload.

## Generated-File Hygiene

The repository currently tracks LaTeX build artifacts under `submission/latex/`, including `.aux`, `.log`, `.out`, `.fls`, `.fdb_latexmk` and `.xdv` files. Recommended policy:

- Commit: `main.tex`, `supplementary_information.tex`, `sync_markdown_to_tex.py`, `sync_build_open.bat`, final PDFs if the package intentionally versions review builds.
- Do not commit / ignore: `.aux`, `.log`, `.out`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, `.xdv` and temporary LaTeX files.
- Suggested `.gitignore` rule, if generated artifacts are removed from tracking in a separate cleanup commit:

```gitignore
submission/latex/*.aux
submission/latex/*.log
submission/latex/*.out
submission/latex/*.fls
submission/latex/*.fdb_latexmk
submission/latex/*.synctex.gz
submission/latex/*.xdv
submission/latex/*.tmp
```

No generated files were deleted during this audit.

## References And Bibliography

- Manual numbered references [1]-[8] appear in `article/nmi_moral_overresolution_draft_50k_v5.md` and generated `latex/main.tex`.
- DOI/URL strings in the numbered references were carried through unchanged apart from LaTeX escaping/formatting.
- No `references.bib` file was found in the package; the current build uses manual references embedded in the manuscript file.

## Restricted-Material Boundary

This package intentionally excludes raw SCRUPLES anecdotes, rendered prompts containing anecdote text, raw provider/model responses, full call ledgers, full run stores, `analysis_rows_50k.csv`, `distribution_diagnostics_50k.csv`, `paraphrase_original_vs_rewrite_50k.csv`, and model-ready row stores. Included files are derived summaries, figure-ready CSVs, manuscript-table CSVs, final figures and editable figure assets.

Filename audit found no restricted-material files under `submission/`. Content matches for restricted-material terms are boundary notes in the manuscript/SI/documentation, not restricted payloads.

## Next Human Checks

- Visually inspect `latex/main.pdf` around lines reported in overfull box warnings, especially the endpoint text near lines 45-76 and Extended Data Table 1 caption.
- Confirm wide tables are readable in the PDF viewer at normal zoom and are acceptable for upload as a review/check build.
- Confirm figure labels and panel text are visually legible and meet journal expectations before final upload.
- Confirm portal-entered metadata, competing interests, data/code availability and ethics statements match the manuscript.
