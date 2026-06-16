# Run Readiness Checklist

Use this checklist after the public staging folder is initialized as a standalone repository and before any real provider calls.

## Public Repository Hygiene

- [x] Choose and add a repository license.
- [x] Fill `CITATION.cff` author fields.
- [x] Fill `CITATION.cff` public GitHub repository URL.
- [x] Fill `CITATION.cff` OSF URL.
- [ ] Confirm no raw SCRUPLES data, `runs/`, SQLite databases, API keys, cache files, or generated JSONL artifacts are tracked.
- [ ] Run the public test suite from the standalone checkout.

## Data And Local Environment

- [ ] Place SCRUPLES Anecdotes split files under `data/scruples/anecdotes/` for local planning and data-dependent tests.
- [ ] Confirm the SCRUPLES version and redistribution constraints.
- [ ] Configure provider API keys in local environment variables or an untracked `.env`.
- [ ] Set `STUDY_MODEL_IDS` to exactly five model IDs before engineering shakedowns; freeze all five before `3k`.

## Pre-Provider Manifest Freeze

- [ ] Freeze OpenRouter model IDs and version/snapshot strings in `run_manifest_v1.md` after shakedown.
- [x] Fill prompt template and schema SHA-256 hashes in `run_manifest_v1.md`.
- [ ] Run a no-network mock execution smoke test with `RUN_ID=mock_smoke_v1`.
- [ ] Plan the `3k` milestone and fill planned-call hashes/counts after planning.

## Engineering Shakedowns

- [ ] Run `.\execute_milestone_run.bat 1` with `RUN_ID=engineering_shakedown_v1`.
- [ ] Run `.\execute_milestone_run.bat 10` with `RUN_ID=engineering_shakedown_v1`.
- [ ] Run `.\execute_milestone_run.bat 50` with `RUN_ID=engineering_shakedown_v1`.
- [ ] Log notable defects or fixes in `docs/BUG_FIX_LOG.md`.
- [ ] Choose the two OpenRouter-compatible models based on validity, refusal/malformed rate, scale behavior, latency, and error rate.
- [ ] Replace candidate OpenRouter IDs in `run_manifest_v1.md` with the final frozen pair.

## Before Study-Facing Collection

- [ ] Freeze updated `run_manifest_v1.md`.
- [ ] Create a GitHub release, for example `v0.1-pre-3k`.
- [ ] Archive the release with Zenodo or another DOI-issuing archive.
- [ ] Add the DOI/release link to OSF.
- [ ] Confirm `3k` remains exploratory and engineering-facing decisions are documented before collection begins.
