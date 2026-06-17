# Study Process

This document describes the operating procedure for engineering shakedowns, bug fixes, freezes, OSF/GitHub/Zenodo releases, and milestone decisions.

## Canonical Roles

- OSF is the canonical study page and preregistered protocol record.
- GitHub is the working code repository.
- Zenodo archives immutable GitHub releases and provides software/materials DOIs.

Recommended release sequence:

1. Freeze `run_manifest_v1.md`.
2. Create a GitHub release, for example `v0.1-pre-3k`.
3. Archive that GitHub release on Zenodo.
4. Add the Zenodo DOI/link back to the OSF project.
5. Cite OSF registration as the preregistered protocol, GitHub as active code, and Zenodo DOI as the immutable software/materials release.

## Run Ladder

Engineering shakedowns are excluded from study analyses:

| Milestone | Role | Expected calls |
|---|---|---:|
| `1` | one-call provider hookup test | 1 |
| `10` | all five model slots across two core modes for one item | 10 |
| `50` | small schema, latency, and outlier screen | 50 |

Study-facing staged milestones:

| Milestone | Role |
|---|---|
| `3k` | exploratory engineering pilot |
| `6k` | exploratory pilot / first directional signal check |
| `13k` | pre-confirmatory diagnostic |
| `25k`, `35k`, `50k` | confirmatory-capable milestones after freeze |

Use a separate `RUN_ID` for engineering shakedowns when possible, for example `engineering_shakedown_v1`, so they are visibly separate from `production_milestones_cumulative_v1`.

## Bug Fix And Locking Rules

The scientific protocol is locked more tightly than implementation plumbing.

Before `3k`:

- Bug fixes are normal.
- Update `run_manifest_v1.md` if a fix changes prompts, schemas, parsing, retry/circuit-breaker behavior, exclusions, model routing, seeds, model IDs, or planned calls.

During `1` / `10` / `50`:

- Bug fixes are expected.
- Outputs are engineering-only and excluded from pilot/confirmatory analyses.
- Record notable defects and fixes in `docs/BUG_FIX_LOG.md`.

After `3k`:

- Fix implementation defects without changing researcher discretion.
- Log every fix that could affect collection, parsing, exclusion, or analysis.
- If a scientific-facing behavior changes, freeze a new manifest version before further study-facing collection.

Before confirmatory `25k+`:

- Freeze the final model roster, prompt templates, JSON extraction rule, parser, exclusion rules, retry policy, item-selection seed, target call list, and milestone decision rules.
- Make a GitHub release and Zenodo archive before confirmatory collection.

## Expected Response And Parsing Rule

The preferred provider response is a single JSON object and no surrounding text.

If a provider returns extra text plus exactly one balanced JSON object, the parser extracts that one object, validates it against the prompt-mode schema, preserves the raw response, and marks the output `valid_extracted_json`.

If zero JSON objects or multiple JSON objects are present, the output is `invalid_json`. Conflicting prose is not silently accepted.

No extra API repair call is used unless a future manifest explicitly freezes the repair prompt, retry budget, and storage fields.

## OpenRouter / Open-Weight Model Rule

The study requires at least one open-weight or open-weight-derived comparison, preferably two stronger OpenRouter-hosted models from the same family for the within-family capability contrast.

The route is configured through the historical `LLAMA_*` environment variables for compatibility, but the models do not need to be Llama-family models. Preferred candidates should be selected by the `1` / `10` / `50` shakedown results:

- schema validity;
- low refusal/malformed rate;
- stable use of 0-1 scales;
- no degenerate label or probability behavior;
- acceptable latency and error rate.

If Llama-family models behave as outliers, they should not be forced into the roster. Stronger Qwen, DeepSeek, Mistral, or comparable OpenRouter models are acceptable if frozen before study-facing collection.

## Provider Availability Amendments

If a provider becomes unavailable during exploratory collection, do not silently substitute a new model inside the frozen roster. Preserve the collected calls under their original model ID, document the provider failure evidence, run an isolated replacement shakedown, and freeze a protocol amendment before further study-facing collection with the replacement.

The 2026-06-17 Gemini availability amendment replaces future Gemini-slot collection with direct xAI `grok-4.3` via the first-party xAI Responses API. The route uses:

- `XAI_API_KEY`
- `XAI_MODEL=grok-4.3`
- optional `XAI_BASE_URL=https://api.x.ai/v1`

The direct xAI route is separate from the OpenRouter-compatible `LLAMA_*` route.

## Paraphrase-Audit Prework

The 3k milestone includes 500 paraphrase-audit calls. These are intentionally blocked until paraphrased item texts are materialized and stored in `paraphrase_pairs`.

Use `materialize_paraphrases.bat 3k` after the immediately provider-executable 3k calls finish. The script generates one paraphrase for each selected paraphrase-audit item, rewrites the blocked paraphrased prompts to use that paraphrase, clears the prework flag, and refreshes `pending_api_calls_3k.jsonl`.

The default helper model is `grok-4.3`; override with `PARAPHRASE_HELPER_MODEL_ID` if needed. After materialization, rerun `execute_remaining_milestone_run.bat 3k` to execute the final paraphrase-audit calls.

## Milestone Outputs To Upload Or Link

Each milestone writes:

- `run_summary_<milestone>.json`
- `pending_api_calls_<milestone>.jsonl`
- `target_api_call_ids_<milestone>.jsonl`
- `selected_items_<milestone>.jsonl`
- `call_ledger_<milestone>.csv`
- `call_ledger_<milestone>.jsonl`
- `milestone_report_<milestone>.md`
- `milestone_report_<milestone>.json`

The milestone report contains the ten OSF reporting sections:

1. calls attempted and completed;
2. retry rate;
3. JSON validity by model and mode;
4. malformed/refusal/off-schema rate;
5. distribution entropy by disagreement bin;
6. agreement surplus by bin/model;
7. distribution-agreement gap by bin/model;
8. sampling compression if available;
9. paraphrase/label-order check result if available;
10. decision: continue, revise, stop, or redesign.
