# Model Selection Notes

Updated: 2026-06-17

## Original Pre-3k First-Party Model Slots

The first three model slots were treated as locked for pre-3k setup:

| Slot | Provider / route | Model ID | Source |
|---:|---|---|---|
| 1 | OpenAI first-party Responses API | `gpt-5.5` | OpenAI model docs list GPT-5.5 with model ID `gpt-5.5`. |
| 2 | Google first-party Gemini API | `gemini-3.5-flash` | Google Gemini API docs list Gemini 3.5 Flash as stable and give `gemini-3.5-flash` as the stable model example. |
| 3 | Anthropic first-party Messages API | `claude-sonnet-4-6` | Anthropic model docs list Claude Sonnet 4.6 with Claude API ID `claude-sonnet-4-6`. |

## Post-3k Amendment: Gemini Replacement Candidate

During the 3k exploratory pilot, repeated first-party Gemini `503` availability failures prevented completion of the Gemini slot while the other providers completed normally. The replacement candidate is:

| Original slot | Replacement provider / route | Replacement model ID | Rationale |
|---:|---|---|---|
| 2 | xAI first-party Responses API | `grok-4.3` | Frontier proprietary family distinct from OpenAI, Anthropic, Qwen, and DeepSeek. Direct xAI route avoids OpenRouter indirection. Isolated shakedown passed 50/50 strict-schema calls with 0 API errors, plus a direct-key smoke test passed 1/1. |

The original Gemini calls already collected under `production_milestones_cumulative_v1` must remain labeled as Gemini. Do not silently relabel, overwrite, or mix them with Grok. Use a protocol amendment and a new run manifest before collecting further study-facing data with `grok-4.3`.

## OpenRouter Candidate Pair For Shakedowns

The OpenRouter-compatible slots should be selected based on `1`, `10`, and `50` shakedown behavior. The selected post-shakedown pair is:

| Slot | Provider / route | Candidate model ID | Rationale |
|---:|---|---|---|
| 4 | OpenRouter-compatible `LLAMA_*` route | `qwen/qwen3.7-max` | Stronger Qwen-family candidate, text-to-text, supports `response_format`, `structured_outputs`, `seed`, and `temperature` on OpenRouter. |
| 5 | OpenRouter-compatible `LLAMA_*` route | `deepseek/deepseek-v3.2` | Strong non-Qwen open/open-weight-derived comparison for family diversity; selected after engineering shakedowns favored one Qwen plus one non-Qwen model. |

Do not treat the OpenRouter pair as scientifically frozen until the engineering shakedowns show acceptable:

- JSON/schema validity;
- refusal and malformed-output rates;
- stable use of 0-1 scales;
- non-degenerate label/probability behavior;
- latency and retry/error rates.

If the Qwen pair behaves poorly, test DeepSeek, Mistral, or comparable OpenRouter-hosted alternatives before `3k`.
