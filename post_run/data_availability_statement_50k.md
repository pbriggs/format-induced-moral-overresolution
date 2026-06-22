# Data And Code Availability Statement

Code, run manifests, and derived analysis artifacts for this study are available through:

- OSF: `https://osf.io/rwhax/`
- GitHub: `https://github.com/pbriggs/format-induced-moral-overresolution`
- Zenodo, 50k execution/completion archive: `https://doi.org/10.5281/zenodo.20786461`
- Zenodo, paper-analysis archive: `https://doi.org/10.5281/zenodo.20789625`

The repository license is CC0 1.0 Universal unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

The public analysis package should include target-scoped derived outputs rather than unrestricted raw ledgers. Public-facing derived outputs include endpoint tables, bootstrap confidence intervals, validity summaries, robustness analyses, paraphrase-audit summaries, distribution-quality diagnostics, manuscript-table CSVs, figure-ready CSVs, and rendered figures.

Raw source anecdotes, raw prompts, raw provider responses, full call ledgers, and the SQLite database may contain material whose redistribution requires additional review. These should be treated as restricted or carefully shared materials unless the applicable dataset and provider terms permit public redistribution.

The final 50k analysis can be regenerated locally from the completed run database with:

```powershell
$env:PYTHONPATH='src'
$env:PYTHONDONTWRITEBYTECODE='1'
python -m analysis.final_50k_exports --bootstrap-iterations 2000
python -m analysis.render_final_figures
```

The main generated summary is:

- `post_run/analysis_exports/50k/manuscript_results_summary_50k.md`

The main export manifest is:

- `post_run/analysis_exports/50k/analysis_export_manifest_50k.json`

The post-50k completion archive records the completed 50k execution state. The paper-analysis archive records the final offline analysis/export/figure package created after that release point.
