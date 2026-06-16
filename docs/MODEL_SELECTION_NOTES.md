# Model Selection Notes

Updated: 2026-06-16

## Locked First-Party Model Slots

The first three model slots are treated as locked for pre-shakedown setup:

| Slot | Provider / route | Model ID | Source |
|---:|---|---|---|
| 1 | OpenAI first-party Responses API | `gpt-5.5` | OpenAI model docs list GPT-5.5 with model ID `gpt-5.5`. |
| 2 | Google first-party Gemini API | `gemini-3.5-flash` | Google Gemini API docs list Gemini 3.5 Flash as stable and give `gemini-3.5-flash` as the stable model example. |
| 3 | Anthropic first-party Messages API | `claude-sonnet-4-6` | Anthropic model docs list Claude Sonnet 4.6 with Claude API ID `claude-sonnet-4-6`. |

## OpenRouter Candidate Pair For Shakedowns

The OpenRouter-compatible slots should be selected based on `1`, `10`, and `50` shakedown behavior. The current recommended candidate pair is:

| Slot | Provider / route | Candidate model ID | Rationale |
|---:|---|---|---|
| 4 | OpenRouter-compatible `LLAMA_*` route | `qwen/qwen3.7-max` | Stronger Qwen-family candidate, text-to-text, supports `response_format`, `structured_outputs`, `seed`, and `temperature` on OpenRouter. |
| 5 | Same family as slot 4 | `qwen/qwen3.7-plus` | Same-family lower-cost/smaller contrast candidate, supports the same relevant OpenRouter parameters. |

Do not treat the OpenRouter pair as scientifically frozen until the engineering shakedowns show acceptable:

- JSON/schema validity;
- refusal and malformed-output rates;
- stable use of 0-1 scales;
- non-degenerate label/probability behavior;
- latency and retry/error rates.

If the Qwen pair behaves poorly, test DeepSeek, Mistral, or comparable OpenRouter-hosted alternatives before `3k`.
