# Bug Fix Log

Use this log for fixes after `run_manifest_v1.md` is frozen or during engineering shakedowns.

| Date | Run context | Files changed | Problem | Fix | Scientific-facing? | Manifest update needed? |
|---|---|---|---|---|---|---|
| 2026-06-16 | pre-freeze | parser/protocol/docs | Added engineering shakedown milestones and deterministic extracted-JSON status before real provider collection. | Added `1`, `10`, `50`; added `valid_extracted_json`; documented process. | Yes | Included before v1 freeze |
| 2026-06-16 | `1` engineering shakedown | `src/prompts/prompt_templates.py`, `tests/test_core_pipeline.py`, `run_manifest_v1.md` | First real `gpt-5.5` distribution call returned a bare label-probability object instead of the frozen schema wrapper, causing `missing_required_field`. | Added explicit required top-level field names and JSON shape examples to prompt templates; added prompt contract regression test. | Yes | Updated prompt template hash before further shakedowns |
