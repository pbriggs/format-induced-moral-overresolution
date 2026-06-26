# Build Report

Generated from canonical manuscript source `article/nmi_moral_overresolution_draft_50k_v5.md`.

## Command Used

Run from `submission/latex/`:

```bat
cmd /c sync_build_open.bat
```

`sync_build_open.bat` now prepends the local MiKTeX binary directory when available, regenerates `main.tex`, runs two `pdflatex` passes for `main.tex`, runs two `xelatex` passes for `supplementary_information.tex`, and opens the generated PDFs.

## Build Status

- `latex/main.pdf`: built successfully, 24 pages, includes the seven verified figure PDFs.
- `latex/supplementary_information.pdf`: built successfully, 12 pages.
- Fatal errors: none.
- Missing figure files: none.
- Undefined references/citations found in logs: none.
- MiKTeX update warnings: present, nuisance only; they did not block compilation.
- Supplementary Information font setup was simplified: explicit `fontspec` and `microtype` loads were removed.

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

- Table 1a, Table 1b and Table 2 are present in `latex/main.tex`.
- These tables are rendered in landscape `longtable` blocks.
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

- Main-text overfull boxes around lines 45-76, mostly long endpoint phrases.
- Extended Data Table 1 caption overfull box around lines 404-405.
- `supplementary_information.log` contains underfull boxes around lines 95-96 involving inline schema field names.

No content or numerical result was changed to address these layout warnings.

## Restricted-Material Boundary

This package intentionally excludes raw SCRUPLES anecdotes, rendered prompts containing anecdote text, raw provider/model responses, full call ledgers, full run stores, `analysis_rows_50k.csv`, `distribution_diagnostics_50k.csv`, `paraphrase_original_vs_rewrite_50k.csv`, and model-ready row stores. Included files are derived summaries, figure-ready CSVs, manuscript-table CSVs, final figures and editable figure assets.
