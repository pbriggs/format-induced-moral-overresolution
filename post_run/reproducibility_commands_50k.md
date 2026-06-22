# Reproducibility Commands: 50k Paper Artifacts

Run these from the repository root:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:PYTHONPATH='src'
$env:PYTHONDONTWRITEBYTECODE='1'

python -m analysis.final_50k_exports --bootstrap-iterations 2000
python -m analysis.render_final_figures
```

Expected primary output folder:

- `post_run/analysis_exports/50k/`

Expected subfolders:

- `post_run/analysis_exports/50k/manuscript_tables/`
- `post_run/analysis_exports/50k/figure_ready/`
- `post_run/analysis_exports/50k/rendered_figures/`
- `post_run/analysis_exports/50k/model_ready/`

Expected generated summary:

- `post_run/analysis_exports/50k/manuscript_results_summary_50k.md`

Expected manifest:

- `post_run/analysis_exports/50k/analysis_export_manifest_50k.json`

## Validation Commands

```powershell
$env:PYTHONPATH='src'
pytest tests\test_core_pipeline.py -q -p no:cacheprovider
```

Syntax-only check without writing Python bytecode:

```powershell
@'
from pathlib import Path
for path in ['src/analysis/final_50k_exports.py', 'src/analysis/render_final_figures.py']:
    source = Path(path).read_text(encoding='utf-8')
    compile(source, path, 'exec')
    print(path, 'syntax ok')
'@ | python -
```

## Git Notes

The `drafts/` directory is ignored by `.gitignore`; `post_run/` is intended for public analysis artifacts.

Recommended commit:

```powershell
git add src\analysis\final_50k_exports.py src\analysis\render_final_figures.py run_manifest_paper_analysis_50k_v1.md post_run\
```

Do not commit files under `drafts/` unless intentionally releasing them.

Generated CSVs and figures in `post_run/` are intended to be committed for the paper-analysis release and may also be mirrored on OSF.
