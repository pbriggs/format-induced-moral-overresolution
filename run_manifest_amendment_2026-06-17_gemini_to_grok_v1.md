# Run Manifest Amendment: Gemini Availability Replacement With Direct xAI Grok 4.3

Date: 2026-06-17

This amendment supplements, but does not overwrite, `run_manifest_pre3k_freeze_v2.md`. The original pre-3k manifest remains the historical record for the frozen 3k start. This amendment documents a provider-availability-driven model substitution before further study-facing collection.

## 1. Reason For Amendment

The original slot 2 model was:

- Provider / route: Google first-party Gemini API
- Model ID: `gemini-3.5-flash`

During `production_milestones_cumulative_v1`, repeated Gemini first-party API `503` unavailable/high-demand errors prevented completion of the Gemini slot while other providers completed normally. The local production progress check before amendment showed:

- completed calls: `2486/3000`
- remaining calls: `514`
- provider-executable remaining calls: `14`
- prework-blocked paraphrase-audit calls: `500`
- API errors: `12`
- terminal failures: `0`

The unresolved provider-executable calls were Gemini-slot calls. This amendment treats the issue as provider availability, not a post hoc performance-based model exclusion.

## 2. Replacement Model

Future Gemini-slot collection after this amendment uses:

| Slot | Provider / route | Model ID | Rationale |
|---:|---|---|---|
| 2 | xAI first-party Responses API | `grok-4.3` | Distinct frontier proprietary model family; direct first-party route; replacement selected for availability and schema reliability after isolated shakedown. |

Direct xAI API configuration:

- `XAI_API_KEY`
- `XAI_MODEL=grok-4.3`
- optional `XAI_BASE_URL=https://api.x.ai/v1`
- endpoint: `https://api.x.ai/v1/responses`

The xAI route is separate from the OpenRouter-compatible `LLAMA_*` route. OpenRouter-hosted xAI calls are not used for the amended production route.

## 3. Amended Model Roster For Future Collection

The amended five-model roster for study-facing collection after this amendment is:

```text
STUDY_MODEL_IDS=gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2
```

| Slot | Provider / route | Amended model ID |
|---:|---|---|
| 1 | OpenAI first-party Responses API | `gpt-5.5` |
| 2 | xAI first-party Responses API | `grok-4.3` |
| 3 | Anthropic first-party Messages API | `claude-sonnet-4-6` |
| 4 | OpenRouter-compatible `LLAMA_*` route | `qwen/qwen3.7-max` |
| 5 | OpenRouter-compatible `LLAMA_*` route | `deepseek/deepseek-v3.2` |

Previously collected valid Gemini outputs remain labeled as `gemini-3.5-flash` and must not be relabeled as Grok. Any analysis that combines or excludes the partial Gemini 3k slot must report that decision explicitly.

## 4. Replacement Shakedown Evidence

OpenRouter `x-ai/grok-4.1-fast` was attempted as an isolated candidate and failed because OpenRouter returned `404` for all 50 attempts, with a provider message that Grok 4.1 Fast was deprecated and recommended Grok 4.3.

OpenRouter `x-ai/grok-4.3` was then tested in isolated engineering shakedown runs:

- `engineering_shakedown_grok_4_3_50_v1`
- `engineering_shakedown_grok_4_3_50_v2`
- `engineering_shakedown_grok_4_3_50_v3`
- `engineering_shakedown_grok_4_3_50_v4`
- `engineering_shakedown_grok_4_3_50_v5`

Aggregate result:

- raw calls: `50`
- API errors: `0`
- valid strict-schema outputs: `50`
- distribution-mode outputs: `25`
- descriptive-verdict-mode outputs: `25`

After direct xAI support was added, a one-call direct xAI key/routing smoke test passed:

- run ID: `engineering_smoke_xai_grok_4_3_direct_key_v1`
- model ID: `grok-4.3`
- provider route: direct xAI Responses API
- result: `1/1` completed, `valid_strict_schema`, `0` failed, `0` invalid

## 5. Code And Routing Changes

The amendment requires a code release that includes:

- direct xAI provider inference for model IDs beginning with `grok-`
- direct xAI provider config using `XAI_*` environment variables
- xAI Responses API adapter
- explicit-provider-map fix for unknown provider slugs
- regression tests for the direct xAI payload and explicit provider mapping

These changes affect model routing/configuration and are scientific-facing. They are logged in `docs/BUG_FIX_LOG.md`.

## 6. Required Archival Actions Before Further Study-Facing Collection

Before running further study-facing collection with `grok-4.3`:

1. Commit the amendment and routing-code changes to GitHub.
2. Create a GitHub release for this amendment.
3. Archive the release on Zenodo and record the DOI.
4. Upload this amendment file to the OSF project.
5. Add the GitHub release URL and Zenodo DOI to the OSF project materials or wiki/description.

Recommended release tag:

```text
gemini-to-grok-amendment-v1
```

## 7. Recommended Next Production Run ID

Use a new run ID for amended future collection rather than silently continuing the original 3k run as if the model roster had not changed:

```text
production_milestones_cumulative_grok_amendment_v1
```

If the partial original 3k is retained as an exploratory artifact, report it as the pre-amendment Gemini-run attempt and keep its ledgers separate from amended Grok collection.
