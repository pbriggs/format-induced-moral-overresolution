# Handoff Status

Use this document as the starting point for a new conversation or a new workspace rooted at `format-induced-moral-overresolution`.

## Current State

- Public repository staging folder has been created from the private working repo.
- Intended public repo name: `format-induced-moral-overresolution`.
- Raw SCRUPLES data, historical `old/` material, `runs/`, SQLite databases, cache/temp files, and generated JSONL artifacts are excluded.
- Core code lives in `src/`.
- Regression tests live in `tests/`.
- Study operating procedure is in `docs/STUDY_PROCESS.md`.
- Public release checklist is in `docs/PUBLIC_RELEASE_CHECKLIST.md`.
- Data setup instructions are in `docs/DATA_SETUP.md`.
- Bug-fix logging template is in `docs/BUG_FIX_LOG.md`.

## Implemented Protocol / Code Features

- Engineering shakedown milestones: `1`, `10`, `50`.
- Study-facing milestones: `3k`, `6k`, `13k`, `25k`, `35k`, `50k`.
- Resume-safe planned-call ledger.
- Provider execution layer with old environment-variable names.
- OpenRouter-compatible route still uses historical `LLAMA_*` env vars, but Llama-family models are not required.
- Stronger Qwen/DeepSeek/Mistral/comparable OpenRouter models are allowed and should be selected based on shakedown results.
- Raw API responses and failed-call details are retained.
- Attempt logs are separate from final parsed outputs.
- Circuit breaker stops repeated retryable/5xx/rate-limit failures.
- Deterministic extracted-JSON parsing: strict JSON first, then exactly one balanced JSON object if surrounded by extra text.
- Uploadable milestone artifacts:
  - `call_ledger_<milestone>.csv`
  - `call_ledger_<milestone>.jsonl`
  - `milestone_report_<milestone>.md`
  - `milestone_report_<milestone>.json`

## Validation Status

In the private source repo with local SCRUPLES data:

```powershell
$env:PYTHONPATH='src'
pytest tests/test_core_pipeline.py -q -p no:cacheprovider
```

Expected current result: all tests pass.

In the clean public repo without SCRUPLES data, data-dependent tests should skip. Core tests should pass.

## Next Steps In New Workspace

1. Copy `public_repo/format-induced-moral-overresolution` to a standalone folder outside the private repo.
2. Open the standalone folder as the new workspace.
3. Initialize Git:

```powershell
git init
git add .
git commit -m "Initial public study repository"
```

4. Create a new public GitHub repository named `format-induced-moral-overresolution`.
5. Push this clean repo.
6. Fill `CITATION.cff` author/repository/OSF fields.
7. Fill `run_manifest_v1.md` exact model IDs and hashes before real provider execution.
8. Run engineering shakedowns in order:

```powershell
.\execute_milestone_run.bat 1
.\execute_milestone_run.bat 10
.\execute_milestone_run.bat 50
```

9. Choose the two OpenRouter models based on schema validity, refusal/malformed rate, scale behavior, latency, and error rate.
10. Freeze and release:
    - GitHub release, e.g. `v0.1-pre-3k`;
    - archive on Zenodo;
    - add DOI/link to OSF.

## Bug-Fix Policy Reminder

- Before `3k`: bug fixes are normal, but update `run_manifest_v1.md` if they affect prompts, schemas, parsing, retry/circuit-breaker behavior, exclusions, model routing, seeds, model IDs, or planned calls.
- During `1` / `10` / `50`: bug fixes are expected and outputs are engineering-only.
- After `3k`: log every collection/parsing/exclusion/analysis-relevant fix in `docs/BUG_FIX_LOG.md`.
- Before confirmatory `25k+`: freeze a new manifest and archive a release if scientific-facing behavior changed.
