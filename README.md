# Format-Induced Moral Over-Resolution

This repository contains protocol, data-processing, milestone-planning, API collection, parsing, and metric code for a preregistered audit of whether large language models preserve source-community moral disagreement across output formats.

The primary source-community dataset is SCRUPLES Anecdotes. Raw dataset text and raw model outputs should be shared only if permitted by dataset license, provider terms, privacy considerations, and ethics review. The public repository should default to code, prompts, schemas, manifests, derived metrics, aggregate reports, and exclusion logs.

## Quick Start

```powershell
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -e .[dev]
$env:PYTHONPATH='src'
pytest
```

## Engineering Shakedowns

Before `3k`, run progressively larger engineering shakedowns. These are excluded from study analyses:

```powershell
.\execute_milestone_run.bat 1
.\execute_milestone_run.bat 10
.\execute_milestone_run.bat 50
```

Use a separate `RUN_ID`, such as `engineering_shakedown_v1`, for these runs when possible.

## Plan A Milestone

```powershell
Set-Location "<repo-root>"
.\start_milestone_run.bat 3k
```

## Execute A Milestone

Set `STUDY_MODEL_IDS` to exactly five frozen model IDs before real provider execution. The execution runner reuses old production environment variable names:

- `OPENAI_API_KEY`, `OPENAI_MODEL`, optional `OPENAI_BASE_URL`
- `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, optional `ANTHROPIC_BASE_URL`
- `GOOGLE_API_KEY`, `GOOGLE_MODEL`, optional `GOOGLE_GENAI_BASE_URL`
- `LLAMA_API_KEY`, `LLAMA_MODEL`, optional `LLAMA_BASE_URL` for the OpenRouter-compatible route. These historical env names may point to stronger Qwen, DeepSeek, Mistral, or comparable OpenRouter-hosted models; Llama-family models are not required.
- optional `STUDY_MODEL_PROVIDER_MAP` for explicit `model=provider` routing

```powershell
Set-Location "<repo-root>"
.\execute_milestone_run.bat 3k
```

For a no-network smoke run:

```powershell
$env:STUDY_MODEL_IDS='mock-a,mock-b,mock-c,mock-d,mock-e'
$env:MOCK_PROVIDER='1'
.\execute_milestone_run.bat 3k
```

## Public Release Notes

Before making the repository public, review [docs/PUBLIC_RELEASE_CHECKLIST.md](docs/PUBLIC_RELEASE_CHECKLIST.md) and [docs/STUDY_PROCESS.md](docs/STUDY_PROCESS.md). In particular, confirm that generated run artifacts, SQLite ledgers, raw SCRUPLES text, provider responses, API keys, local temp folders, and vendored large files are not included unless intentionally released under the relevant terms.

## License And Redistribution

Original code, documentation, prompts, schemas, and protocol materials in this repository are released under CC0 1.0 Universal unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## Data Note

Raw SCRUPLES files are intentionally not included in the public repository. Tests that require raw split files are skipped until the user places the files under `data/scruples/anecdotes/` according to [docs/DATA_SETUP.md](docs/DATA_SETUP.md).
