"""Minimal single-turn JSON call.

Run from the repository root:
    python -m common.example
"""

from __future__ import annotations

import json

from common.llm_api import (
    InferenceRequest,
    ProviderRequestError,
    build_adapters,
    classify_api_failure,
    load_provider_configs,
    parse_json_output,
)


def main() -> None:
    model_id = "gpt-5.5"
    configs, model_to_provider = load_provider_configs([model_id])
    adapters = build_adapters(configs)
    provider = model_to_provider[model_id]

    try:
        response = adapters[provider].run_single_turn(
            InferenceRequest(
                model_id=model_id,
                prompt='Return JSON only: {"answer": "your short answer"}\nQuestion: What is 2 + 2?',
                max_tokens=128,
            )
        )
    except ProviderRequestError as exc:
        failure = classify_api_failure(
            http_status_code=exc.status_code,
            error_type="transport_error" if exc.transport_error_message else None,
            error_response_body=exc.error_response_body,
            retry_after_seconds=exc.retry_after_seconds,
        )
        raise SystemExit(
            f"{failure.kind.value}: {failure.reason}; attempts={exc.attempts}; detail={exc}"
        ) from exc

    parsed = parse_json_output(response.raw_text, required_fields=("answer",))
    if not parsed.valid:
        raise SystemExit(f"Invalid model output: {parsed.status.value}: {parsed.errors}")

    print(
        json.dumps(
            {
                "provider": response.provider,
                "requested_model": response.request_model_id,
                "resolved_model": response.resolved_model_id,
                "attempts": response.attempts,
                "latency_ms": response.latency_ms,
                "usage": response.usage,
                "parsed": parsed.value,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
