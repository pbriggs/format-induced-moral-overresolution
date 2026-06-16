# Public Release Checklist

## Before Creating The Public Repository

- Choose and add a repository license.
- Fill contributor, OSF, GitHub, and citation fields in `CITATION.cff`.
- Confirm that `final_for_osf.md`, `osf_document.md`, and any uploaded registration text agree on pilot vs. confirmatory status.
- Confirm that `docs/STUDY_PROCESS.md` matches the OSF/GitHub/Zenodo release plan and bug-fix policy.
- Freeze the five exact model IDs in `STUDY_MODEL_IDS` slot order.
- Freeze prompt templates, JSON schemas, random seeds, milestone decision rules, retry policy, parsing rules, and exclusion rules.
- Run the no-network mock execution test and the full unit suite.

## Do Not Commit Unless Intentionally Released

- `runs/`
- `*.sqlite`, `*.db`, and sidecar database files
- `.env` and any file containing API keys
- raw SCRUPLES anecdote text, if redistribution is not confirmed
- raw model API responses, if provider terms or privacy review do not permit release
- local temp folders such as `.tmp_*` and `pytest-cache-files-*`
- vendored model weights or other large binary files
- old exploratory run artifacts under `old/`

## Recommended Public Repository Layout

```text
README.md
LICENSE
CITATION.cff
.env.example
docs/
  PUBLIC_RELEASE_CHECKLIST.md
  run_manifest_v1.md
  milestone_decision_rules.md
osf/
  osf_registration.md
  osf_document.md
src/
tests/
```

## Release Sequence

1. Clean the worktree and verify `.gitignore`.
2. Create a private GitHub repository first.
3. Push only reviewed source, protocol, tests, and public-safe docs.
4. Run tests from a fresh clone.
5. Make the repository public.
6. Create a GitHub release.
7. Archive the release with Zenodo or another DOI-issuing archive.
8. Add the DOI/release link as an OSF linked resource.

## Notes From The Old API Workflow Worth Keeping

- Use freeze/hash checks for files that must not drift after OSF submission.
- Validate shard bundles before merging or treating a stage as complete.
- Keep append-only attempt logs separate from final parsed outputs.
- Keep milestone reports separate from raw run artifacts.
- Treat public release as a curated artifact, not a dump of the working folder.
