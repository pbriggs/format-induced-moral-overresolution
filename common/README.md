# Reusable multi-provider LLM API layer

This folder is the portable handoff from the API collection work in this
repository. It records what the study implementation did and provides a
self-contained, standard-library-only Python package that can be copied into
another project.

No credentials or response data are copied here. `env.example` contains only
variable names, public API base URLs, and the model identifiers frozen for the
study.

## Quick start

Copy `common/llm_api/` into the new repository (or copy the entire `common/`
folder), set the needed environment variables, and import it:

```python
from llm_api import InferenceRequest, build_adapters, load_provider_configs

models = ["gpt-5.5", "grok-4.3", "claude-sonnet-4-6",
          "qwen/qwen3.7-max", "deepseek/deepseek-v3.2"]
configs, routes = load_provider_configs(models)
clients = build_adapters(configs)

request = InferenceRequest(
    model_id=models[0],
    prompt='Return JSON only: {"answer": "..."}',
    max_tokens=256,
)
response = clients[routes[request.model_id]].run_single_turn(request)
print(response.raw_text)
```

If the entire `common` directory remains in a repository root, the imports used
by `common/example.py` also work. Run its offline tests with:

```powershell
python -m unittest discover -s common/tests -v
```

The code requires Python 3.11 or newer and has no runtime dependencies.

## What we built in the original project

The execution path was:

```text
environment variables
  -> provider/model routing
  -> provider-specific request payload
  -> JSON HTTP POST
  -> bounded retry/backoff
  -> provider-specific text extraction
  -> normalized response envelope
  -> JSON extraction and study-schema validation
  -> raw-call, attempt, and parsed-output persistence
  -> failure classification and provider circuit breaker
  -> progress and milestone reports
```

The implementation deliberately kept raw acquisition separate from parsing.
Every successful provider response was normalized to a text string while the
request payload, provider response payload, headers, resolved model version,
finish reason, status, and latency remained available for auditing. Parsing
then classified output validity without overwriting the raw response.

### Final model and route inventory

The final frozen run used:

| Model ID | Provider | Route shape | Adapter |
|---|---|---|---|
| `gpt-5.5` | OpenAI | `POST /v1/responses` | Responses API |
| `grok-4.3` | xAI | `POST /v1/responses` | Responses API |
| `claude-sonnet-4-6` | Anthropic | `POST /v1/messages` | Messages API |
| `qwen/qwen3.7-max` | OpenRouter | `POST /api/v1/chat/completions` | OpenAI-compatible chat |
| `deepseek/deepseek-v3.2` | OpenRouter | `POST /api/v1/chat/completions` | OpenAI-compatible chat |

Google `generateContent` support is also retained because it was implemented
and tested earlier in the project. The final run replaced its Gemini slot with
Grok. Model identifiers and provider API behavior can change, so confirm model
availability before a new production run.

## Source inventory

These original files contain the relevant work:

| Original file | Responsibility | Portability |
|---|---|---|
| `src/production/config.py` | Env lookup, Windows user-env fallback, credential requirements, model routing | Mostly reusable; study required exactly five models |
| `src/production/providers.py` | HTTP transport, retries, payloads, response extraction, normalized envelope, provider adapters | Reusable core |
| `src/production/failure_policy.py` | Error taxonomy, retry decisions, circuit breaker | Reusable core |
| `src/parsing/validate_json.py` | Strict JSON parse, one-object extraction, study-schema validation | Extraction reusable; labels/modes study-specific |
| `src/parsing/validity_status.py` | Validity taxonomy | Mostly study-specific |
| `src/prompts/schemas.py` | JSON schemas for each experimental prompt mode | Study-specific |
| `src/production/execute_milestone.py` | Planning, routing, calls, DB writes, parsing, resume logic, progress | Orchestration pattern reusable; records study-specific |
| `src/storage/db.py` | Raw calls, attempts, parsed values, model registry, manifests | Audit pattern reusable; schema study-specific |
| `src/production/reporting.py` | Call ledger, validity/retry summaries, milestone gates | Study-specific reporting |
| `src/production/shards.py` | Resumable JSONL work shards and state | Reusable for large batch jobs |
| `.env.example` | Credential/base URL/model variable contract | Reusable template |
| `tests/test_core_pipeline.py` | Regression tests for payloads, retries, parsing, errors, execution | Mixed reusable/study-specific coverage |

## Portable folder inventory

| New file | Use |
|---|---|
| `llm_api/config.py` | Credentials, base URLs, retry settings, and model routing |
| `llm_api/providers.py` | Five provider adapters, mock adapter, HTTP retry, normalized responses |
| `llm_api/failure_policy.py` | Error classification and circuit breaker |
| `llm_api/json_output.py` | Generic JSON extraction and small declarative field validator |
| `llm_api/__init__.py` | Stable public imports |
| `env.example` | Safe environment-variable template |
| `example.py` | End-to-end call, error classification, and JSON parsing |
| `tests/test_llm_api.py` | Offline regression tests; no keys or network calls |

## Authentication and configuration

Credentials are read from process environment variables. On Windows, if a key
is absent from the current process, the loader also checks the current user's
persistent `Environment` registry key. This handles terminals opened before a
user variable was added.

| Provider | Required key | Optional base URL | Optional default model |
|---|---|---|---|
| OpenAI | `OPENAI_API_KEY` | `OPENAI_BASE_URL` | `OPENAI_MODEL` |
| xAI | `XAI_API_KEY` | `XAI_BASE_URL` | `XAI_MODEL` |
| Anthropic | `ANTHROPIC_API_KEY` | `ANTHROPIC_BASE_URL` | `ANTHROPIC_MODEL` |
| OpenRouter | `OPENROUTER_API_KEY` | `OPENROUTER_BASE_URL` | `OPENROUTER_MODEL` |
| Google | `GOOGLE_API_KEY` | `GOOGLE_GENAI_BASE_URL` | `GOOGLE_MODEL` |

Only providers needed for the requested model list are loaded, so unused keys
are not required. `MODEL_PROVIDER_MAP` accepts comma-separated
`model=provider` overrides. The portable copy accepts the original `llama`
provider name and `LLAMA_*` variables for compatibility.

The library does not load `.env` files. That avoids silently choosing a stale
secret file; use the shell, deployment secret manager, or a dotenv library in
the host application. Never commit populated environment files, log
authorization headers, or serialize `ProviderConfig` objects.

## Request and response contract

`InferenceRequest` is the provider-neutral input:

- `prompt`: user content.
- `model_id`: exact provider model identifier.
- `temperature`: defaults to `0.0`.
- `max_tokens`: requested output budget; Responses API and Google payloads
  retain the study's minimum of 1,024 tokens.
- `system_prompt`: optional and mapped to each provider's native shape.

`ApiResponseEnvelope` is the normalized output:

- provider, requested model, provider-resolved model, and sanitized endpoint;
- HTTP status, total elapsed milliseconds, and actual attempt count;
- extracted model text in `raw_text`;
- exact request and response JSON objects;
- response headers, response ID, finish reason, and usage metadata.

For Google, the API key is a query parameter, but the envelope stores the
endpoint with that query removed. The request payload never contains API keys.

Provider formatting behavior:

- OpenAI and xAI extract top-level `output_text`, falling back to nested
  `output[].content[]` parts of type `output_text`.
- Anthropic concatenates all content blocks of type `text`.
- Google concatenates candidate text parts and joins candidate finish reasons.
- OpenRouter reads the first choice's assistant message content.

The envelope keeps both normalized text and the original response JSON so a new
project can parse convenient text without losing audit evidence.

## Retry and error behavior

The transport retries HTTP `408`, `409`, `425`, `429`, `500`, `502`, `503`,
and `504`, plus timeouts, socket/OS errors, HTTP protocol errors, and incomplete
chunked reads. Defaults are five total attempts, a 60-second timeout per
attempt, exponential backoff starting at 0.5 seconds, and up to 0.25 seconds of
jitter.

`Retry-After` takes precedence over backoff and accepts either seconds or an
HTTP date. Non-retryable HTTP statuses fail immediately. A 2xx response that is
not a JSON object is also surfaced as `ProviderRequestError` with its body
preserved for diagnosis.

`ProviderRequestError` exposes:

- `status_code`;
- response headers and error response body;
- parsed retry delay;
- transport error detail;
- actual attempt count.

The separate classifier maps failures to authorization, bad request, rate
limit, server error, timeout, safety filter, parse/schema, or unknown. It
contains an important production regression fix: OpenRouter HTTP 403 responses
whose body says an account/key limit was exceeded are treated as retryable rate
limits, not invalid credentials.

The circuit breaker operates across recent calls, not within one call. Its
defaults abort a provider queue after 20 retryable failures, 10 server errors,
or 10 rate limits. Feed it failures from a bounded time window and scope the
list by provider.

## JSON reading and validation

`parse_json_output` first attempts strict `json.loads`. If that fails, it will
accept exactly one balanced JSON object surrounded by prose. The scanner
respects quoted braces and escapes. It rejects multiple objects because
silently choosing one would be ambiguous.

The portable validator supports:

- required top-level fields;
- allowed string/enum values;
- inclusive numeric ranges.

It returns a status, parsed object, diagnostic errors, and whether extraction
was needed. Domain-specific nested schemas should be validated in the new
project after this generic step, using JSON Schema, Pydantic, or dedicated
functions. The original moral-label validators were intentionally not embedded
in the generic module; copy `src/parsing/validate_json.py`,
`src/protocol/label_schema.py`, and `src/protocol/prompt_modes.py` only if the
new project uses that same response contract.

## Persistence and resumability pattern

The reusable package does not impose a database, but the original design is
worth carrying over:

1. Assign a stable call ID before sending.
2. Store the complete request record separately from credentials.
3. Append every attempt to an immutable attempt ledger.
4. Store one final raw-call record with status, raw text, headers, error body,
   resolved model, timestamps, and retry count.
5. Parse into a separate table or object; never replace the raw response.
6. Resume by skipping successful or terminal call IDs and retrying only
   recoverable failures.
7. Apply a provider-scoped circuit breaker before taking the next queued call.
8. Export a human-readable ledger and aggregate retry/validity report.

The original SQLite tables implementing this were `api_calls_raw`,
`api_call_attempts`, `parsed_outputs`, `model_registry`, `planned_api_calls`,
and `run_manifest`. For a smaller project, a JSONL attempt ledger plus one
SQLite calls table is sufficient.

Suggested minimum raw-call fields are:

```text
call_id, provider, requested_model, resolved_model, endpoint,
request_json, raw_text, response_json, response_headers_json,
response_id, finish_reason, usage_json, status_code, attempts,
started_at, completed_at, error_kind, error_body, transport_error
```

## Differences from the study copy

The portable files preserve the behavior that matters while fixing coupling
and observability issues:

- They accept any number of models; the study config required exactly five.
- `openrouter` and `OPENROUTER_*` are the clear public names, while `llama` and
  `LLAMA_*` remain compatibility aliases.
- Retry settings are passed into adapters instead of existing only in a higher
  execution config.
- Successful envelopes report the actual attempt count and total elapsed time.
- Failed exceptions report actual attempts. In the study executor, internal
  transport retries were summarized as one attempt row and successful calls
  recorded retry count zero, so per-attempt audit data was less precise than
  the transport itself.
- The portable parser is domain-neutral.
- Optional system prompts and normalized usage/response IDs are exposed.

One subtle limit remains: the low-level transport performs its retries
internally, so it returns aggregate attempt count rather than an event for each
attempt. If a new project requires a row for every retry, add an `on_attempt`
callback to `post_json_with_retry` or place the retry loop in the orchestrator.

## Production adoption checklist

Before running the new project:

1. Copy the package and offline tests.
2. Put keys in the deployment secret store and verify only needed keys load.
3. Confirm current model IDs and base URLs with each provider.
4. Decide whether the study's forced JSON MIME type and minimum 1,024-token
   budget match the new task.
5. Define the new response schema and test malformed, refusal, and fenced/prose
   responses.
6. Persist raw responses before parsing.
7. Choose retry and circuit-breaker limits appropriate to rate limits and cost.
8. Add a mock smoke test, then make one inexpensive live call per provider.
9. Confirm logs never contain keys or Google query strings.
10. Record resolved model IDs, timestamps, and prompt/version hashes for
    reproducibility.

## Files intentionally not copied

Prompt templates, moral-label schemas, milestone planners, analysis code,
dataset loaders, and manuscript reporting were not duplicated because they
encode this study rather than general API mechanics. The source inventory above
points to them if the next project deliberately shares those contracts.
