# Archive Upload Inventory: 50k Completion

Date prepared: 2026-06-21

Project: format-induced moral overresolution

Run ID: `production_milestones_cumulative_v1`

Milestone: 50k completion

OSF project: `https://osf.io/rwhax/`

OSF storage location used for milestone uploads: `https://osf.io/rwhax/files/osfstorage`

GitHub repository: `https://github.com/pbriggs/format-induced-moral-overresolution`

50k execution/completion release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-50k-completion-v1`

50k execution/completion Zenodo DOI: `https://doi.org/10.5281/zenodo.20786461`

Recommended paper-analysis release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/paper-analysis-50k-v1`

Paper-analysis Zenodo DOI: `[fill after paper-analysis-50k-v1 is archived]`

## Recommended OSF Uploads

Upload these files or folders to OSF for the final 50k completion record.

### Run Manifests And Release Records

- `run_manifest_post50k_completion_v1.md`
- `run_manifest_pre50k_freeze_v1.md`
- `run_manifest_amendment_2026-06-17_gemini_to_grok_v1.md`
- 50k execution/completion GitHub release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-50k-completion-v1`
- 50k execution/completion Zenodo DOI URL: `https://doi.org/10.5281/zenodo.20786461`
- recommended paper-analysis manifest: `run_manifest_paper_analysis_50k_v1.md`
- recommended paper-analysis GitHub release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/paper-analysis-50k-v1`
- paper-analysis Zenodo DOI URL: `[fill after release archival]`

### Paper-Analysis Planning Documents

- `paper/punch-list-resolution.md`
- `paper/manuscript_assembly_plan_50k.md`
- `paper/final_remaining_decisions_50k.md`
- `paper/archive_upload_inventory_50k.md`
- `paper/data_availability_statement_50k.md`
- `paper/reproducibility_commands_50k.md`
- `paper/nmi_additional_analyses_decision_50k.md`
- `run_manifest_paper_analysis_50k_v1.md`

### Final Run Reports

From `runs/production_milestones_cumulative_v1/`:

- `execution_summary_50k.json`
- `milestone_report_50k.json`
- `milestone_report_50k.md`
- `run_summary_50k.json`
- `target_api_call_ids_50k.jsonl`
- `selected_items_50k.jsonl`
- `pending_api_calls_50k.jsonl`

### Final Analysis Exports

From `paper/analysis_exports/50k/`:

- `analysis_export_manifest_50k.json`
- `manuscript_results_summary_50k.md`
- `primary_endpoint_table_50k.csv`
- `bootstrap_endpoint_ci_50k.csv`
- `adjusted_tests_50k.csv`
- `model_level_endpoint_table_50k.csv`
- `leave_one_model_out_50k.csv`
- `validity_by_model_mode_50k.csv`
- `invalid_output_summary_50k.csv`
- `validity_flags_50k.csv`
- `validity_sensitivity_50k.csv`
- `smoothing_sensitivity_50k.csv`
- `annotation_info_sensitivity_50k.csv`
- `paraphrase_effects_50k.csv`
- `paraphrase_bootstrap_ci_50k.csv`
- `distribution_diagnostics_summary_50k.csv`
- `distribution_entropy_correlations_50k.csv`
- `baseline_distribution_quality_50k.csv`
- `normative_certainty_by_bin_model_50k.csv`

### Manuscript Tables, Figure Data, And Rendered Figures

Upload the full folders:

- `paper/analysis_exports/50k/manuscript_tables/`
- `paper/analysis_exports/50k/figure_ready/`
- `paper/analysis_exports/50k/rendered_figures/`

### Optional Model-Ready Files

Upload if you want downstream reviewers/collaborators to be able to fit secondary models without reconstructing endpoint rows:

- `paper/analysis_exports/50k/model_ready/mixed_effects_endpoint_rows_50k.csv`
- `paper/analysis_exports/50k/model_ready/mixed_effects_endpoint_rows_strict_valid_50k.csv`

## Restricted Or Carefully Shared Files

These files may include raw prompt text, raw model-output text, or source anecdotes and should not be publicly redistributed without checking SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements:

- `runs/production_milestones_cumulative_v1/study.sqlite`
- `runs/production_milestones_cumulative_v1/call_ledger_50k.csv`
- `runs/production_milestones_cumulative_v1/call_ledger_50k.jsonl`
- any raw SCRUPLES source anecdote files;
- any raw provider response logs not already reduced into aggregate analysis exports.

If these are needed for review, place them in a restricted-access OSF component or provide them by controlled request, subject to the applicable terms.

## Suggested OSF Description

Final 50k completion artifacts for the format-induced moral overresolution study. Includes post-run milestone reports, target call IDs, selected item IDs, derived analysis exports, manuscript-table CSVs, figure-ready CSVs, rendered figures, and reproducibility manifests. Raw prompt/model-output ledgers and source anecdotes are treated as restricted/carefully shared materials because redistribution remains subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## Completion Checklist

- [x] Create/upload post-50k completion run archive files.
- [x] Record post-50k completion DOI: `https://doi.org/10.5281/zenodo.20786461`.
- [x] Upload 50k milestone files to OSF project storage: `https://osf.io/rwhax/files/osfstorage`.
- [ ] Commit/push paper-analysis scripts and docs.
- [ ] Create recommended paper-analysis GitHub release: `paper-analysis-50k-v1`.
- [ ] Confirm Zenodo archived the paper-analysis release.
- [ ] Fill paper-analysis Zenodo DOI above.
- [ ] Upload recommended paper-analysis artifacts to OSF.
- [ ] Upload restricted artifacts only if appropriate and with the correct access control.
- [x] Record OSF location: `https://osf.io/rwhax/files/osfstorage`.
- [ ] Record exact OSF upload date/time if needed; OSF file metadata should preserve individual upload timestamps.
