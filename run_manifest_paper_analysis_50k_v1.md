# Run Manifest Paper Analysis 50k v1

Date: 2026-06-21

This file records the post-run paper-analysis artifact set created after the completed 50k execution milestone for `format-induced-moral-overresolution`.

It supplements, but does not replace, `run_manifest_post50k_completion_v1.md`.

## 0. Archive Identifiers

- OSF project: `https://osf.io/rwhax/`
- OSF storage location used for milestone uploads: `https://osf.io/rwhax/files/osfstorage`
- GitHub repository: `https://github.com/pbriggs/format-induced-moral-overresolution`
- 50k execution/completion release tag: `post-50k-completion-v1`
- 50k execution/completion release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-50k-completion-v1`
- 50k execution/completion Zenodo DOI: `https://doi.org/10.5281/zenodo.20786461`
- Paper-analysis release tag: `paper-analysis-50k-v1`
- Paper-analysis release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/paper-analysis-50k-v1`
- Paper-analysis Zenodo DOI: `https://doi.org/10.5281/zenodo.20789625`
- Author: Paul Briggs
- License: CC0 1.0 Universal, unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## 1. Why A New Paper-Analysis Release Is Recommended

`run_manifest_post50k_completion_v1.md` and DOI `https://doi.org/10.5281/zenodo.20786461` document the completed 50k run and the post-run milestone reports.

After that release point, additional paper-analysis artifacts were created:

- final 50k endpoint exports;
- bootstrap confidence intervals and contested-minus-high contrasts;
- manuscript-table CSVs;
- figure-ready CSVs;
- rendered PNG/SVG figures;
- model-ready endpoint rows for optional secondary models;
- paper assembly, archive inventory, data-availability, and remaining-decision documents;
- reproducible export/render scripts.

Because those analysis scripts and paper artifacts were created after the post-50k completion release, the cleanest citation/provenance path for manuscript submission is:

1. cite the post-50k completion DOI for the completed run state;
2. cite a new paper-analysis DOI for the final analysis/export/figure package.

This avoids making `post-50k-completion-v1` appear to contain code or artifacts that were created afterward.

## 2. New Or Updated Scripts

- `src/analysis/final_50k_exports.py`
- `src/analysis/render_final_figures.py`

Regeneration command:

```powershell
$env:PYTHONPATH='src'
$env:PYTHONDONTWRITEBYTECODE='1'
python -m analysis.final_50k_exports --bootstrap-iterations 2000
python -m analysis.render_final_figures
```

## 3. Main Generated Analysis Artifacts

Generated root:

- `post_run/analysis_exports/50k/`

Key files:

- `analysis_export_manifest_50k.json`
- `manuscript_results_summary_50k.md`
- `primary_endpoint_table_50k.csv`
- `bootstrap_endpoint_ci_50k.csv`
- `bootstrap_contrast_ci_50k.csv`
- `adjusted_tests_50k.csv`
- `validity_by_model_mode_50k.csv`
- `invalid_output_summary_50k.csv`
- `validity_sensitivity_50k.csv`
- `smoothing_sensitivity_50k.csv`
- `annotation_info_sensitivity_50k.csv`
- `paraphrase_effects_50k.csv`
- `paraphrase_bootstrap_ci_50k.csv`
- `distribution_diagnostics_summary_50k.csv`
- `distribution_entropy_correlations_50k.csv`
- `baseline_distribution_quality_50k.csv`
- `normative_certainty_by_bin_model_50k.csv`

Generated folders:

- `post_run/analysis_exports/50k/manuscript_tables/`
- `post_run/analysis_exports/50k/figure_ready/`
- `post_run/analysis_exports/50k/rendered_figures/`
- `post_run/analysis_exports/50k/model_ready/`

## 4. Public Post-Run Documents

- `post_run/data_availability_statement_50k.md`
- `post_run/reproducibility_commands_50k.md`

Internal working notes were moved to ignored `drafts/` and are not part of the public paper-analysis release.

## 5. Current Final Analysis Snapshot

Primary low-consensus endpoint estimates:

- agreement surplus: `0.37093131989024575`, 95% CI `[0.36120569049405754, 0.3811135291192549]`
- distribution-agreement gap: `0.23268736616702354`, 95% CI `[0.22438670996752436, 0.2413409453000531]`
- sampling compression: `1.2646376937804604`, 95% CI `[1.2184254408342536, 1.3090535619562242]`

Primary contested-minus-high contrast estimates:

- low-consensus agreement-surplus contrast: `0.2015225518284205`, 95% CI `[0.17483459213576952, 0.22856811237068103]`
- low-consensus distribution-gap contrast: `0.04984495929023272`, 95% CI `[0.033773579764769995, 0.06532868086109839]`
- low-consensus sampling-compression contrast: `0.7009295684986816`, 95% CI `[0.618287445926516, 0.783543256942796]`

These estimates are derived from the frozen 50k target IDs and do not require additional provider execution.

## 6. GitHub Release

Tag:

```text
paper-analysis-50k-v1
```

Title:

```text
Paper analysis artifacts for 50k completion v1
```

Suggested release notes:

```text
Adds the final offline 50k paper-analysis artifact set for the completed production_milestones_cumulative_v1 run.

This release supplements the post-50k completion release and DOI:
- post-50k completion DOI: https://doi.org/10.5281/zenodo.20786461

Included analysis updates:
- target-scoped final 50k endpoint exports
- item-cluster bootstrap CIs for primary endpoints
- contested-minus-high bootstrap contrasts
- validity/exclusion and strict-valid-only sensitivity exports
- source-distribution smoothing and annotation/info robustness exports
- paraphrase audit summaries and bootstrap CIs
- distribution-quality and baseline diagnostics
- manuscript-table CSVs and figure-ready CSVs
- rendered PNG/SVG figures
- model-ready endpoint rows for optional secondary mixed-effects models
- paper assembly, data availability, archive inventory, and reproducibility documents

No new provider calls or human-subjects data collection are included in this release.
```

## 7. Recommended OSF Action

Upload or add the paper-analysis artifacts to the existing OSF project storage:

- `https://osf.io/rwhax/files/osfstorage`

The earlier milestone uploads remain valid. For the paper-analysis release, upload the generated `post_run/` analysis/export/figure folders, public post-run documents, and this manifest.
