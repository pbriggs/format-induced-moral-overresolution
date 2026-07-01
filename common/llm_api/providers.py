from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from http import client as http_client
import json
import random
import time
from typing import Any, Protocol
from urllib import error, request

from .config import ProviderConfig, RetryConfig


RETRY_STATUSES = {408, 409, 425, 429, 500, 502, 503, 504}


class ProviderRequestError(RuntimeError):
    """Normalized HTTP, transport, or provider-response error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_headers: dict[str, str] | None = None,
        error_response_body: str | None = None,
        retry_after_seconds: float | None = None,
        transport_error_message: str | None = None,
        attempts: int = 1,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_headers = response_headers or {}
        self.error_response_body = error_response_body
        self.retry_after_seconds = retry_after_seconds
        self.transport_error_message = transport_error_message
        self.attempts = attempts


@dataclass(frozen=True)
class InferenceRequest:
    prompt: str
    model_id: str
    temperature: float = 0.0
    max_tokens: int = 1024
    system_prompt: str | None = None


@dataclass(frozen=True)
class ApiResponseEnvelope:
    provider: str
    request_model_id: str
    resolved_model_id: str
    endpoint: str
    status_code: int
    raw_text: str
    latency_ms: int
    attempts: int
    request_payload: dict[str, Any]
    response_payload: dict[str, Any]
    response_headers: dict[str, str] = field(default_factory=dict)
    response_id: str | None = None
    finish_reason: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)


class ProviderAdapter(Protocol):
    provider_name: str
    endpoint: str

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        ...


def _retry_after(headers: dict[str, str]) -> float | None:
    raw = next((value for key, value in headers.items() if key.lower() == "retry-after"), None)
    if not raw:
        return None
    try:
        seconds = float(raw)
        return max(seconds, 0.0)
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(raw)
            if retry_at.tzinfo is None:
                retry_at = retry_at.replace(tzinfo=timezone.utc)
            return max((retry_at - datetime.now(timezone.utc)).total_seconds(), 0.0)
        except (TypeError, ValueError, OverflowError):
            return None


def _sleep_seconds(headers: dict[str, str], attempt: int, policy: RetryConfig) -> float:
    retry_after = _retry_after(headers)
    if retry_after is not None:
        return retry_after
    return policy.base_backoff_seconds * (2 ** (attempt - 1)) + random.uniform(0.0, policy.jitter_seconds)


def post_json_with_retry(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    retry: RetryConfig | None = None,
) -> tuple[dict[str, Any], int, int, dict[str, str], int]:
    """POST JSON and return body, status, total latency, headers, attempts."""
    policy = retry or RetryConfig()
    last_error: ProviderRequestError | None = None
    body_bytes = json.dumps(payload).encode("utf-8")
    request_headers = {"Content-Type": "application/json", **headers}
    overall_started = time.perf_counter()
    for attempt in range(1, policy.max_attempts + 1):
        req = request.Request(url, data=body_bytes, headers=request_headers, method="POST")
        try:
            with request.urlopen(req, timeout=policy.timeout_seconds) as resp:
                response_body = resp.read().decode("utf-8")
                response_headers = dict(resp.headers.items())
                try:
                    parsed = json.loads(response_body)
                except json.JSONDecodeError as exc:
                    raise ProviderRequestError(
                        f"Provider returned non-JSON response: {exc}",
                        status_code=int(resp.status),
                        response_headers=response_headers,
                        error_response_body=response_body,
                        attempts=attempt,
                    ) from exc
                if not isinstance(parsed, dict):
                    raise ProviderRequestError(
                        "Provider returned JSON whose top level is not an object",
                        status_code=int(resp.status),
                        response_headers=response_headers,
                        error_response_body=response_body,
                        attempts=attempt,
                    )
                latency_ms = int((time.perf_counter() - overall_started) * 1000)
                return parsed, int(resp.status), latency_ms, response_headers, attempt
        except error.HTTPError as exc:
            response_headers = dict(exc.headers.items()) if exc.headers is not None else {}
            error_body = exc.read().decode("utf-8", errors="replace")
            last_error = ProviderRequestError(
                f"HTTP {exc.code}: {_error_detail(error_body)}",
                status_code=int(exc.code),
                response_headers=response_headers,
                error_response_body=error_body,
                retry_after_seconds=_retry_after(response_headers),
                attempts=attempt,
            )
            if exc.code not in RETRY_STATUSES or attempt >= policy.max_attempts:
                raise last_error from exc
            time.sleep(_sleep_seconds(response_headers, attempt, policy))
        except (TimeoutError, OSError, http_client.HTTPException) as exc:
            last_error = ProviderRequestError(
                f"Transport error: {exc}",
                transport_error_message=str(exc),
                attempts=attempt,
            )
            if attempt >= policy.max_attempts:
                raise last_error from exc
            time.sleep(_sleep_seconds({}, attempt, policy))
    raise last_error or ProviderRequestError("Retry exhausted", attempts=policy.max_attempts)


def _error_detail(body: str, max_chars: int = 1200) -> str:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        clean = body.strip().replace("\n", " ").replace("\r", " ")
        return clean[:max_chars] if clean else "(empty response body)"
    if isinstance(payload, dict):
        provider_error = payload.get("error")
        if isinstance(provider_error, dict):
            parts = [
                str(provider_error.get(key))
                for key in ("type", "code", "message")
                if provider_error.get(key)
            ]
            if parts:
                return "; ".join(parts)
    return json.dumps(payload, sort_keys=True)[:max_chars]


class MockAdapter:
    provider_name = "mock"
    endpoint = "mock://local"

    def __init__(self, cfg: ProviderConfig | None = None) -> None:
        self.cfg = cfg

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        text = json.dumps({"answer": "mock", "model": req.model_id})
        return ApiResponseEnvelope(
            "mock",
            req.model_id,
            f"{req.model_id}-mock-snapshot",
            self.endpoint,
            200,
            text,
            1,
            1,
            {"prompt": req.prompt, "model": req.model_id},
            {"id": "mock-response", "text": text},
            response_id="mock-response",
        )


class OpenAIAdapter:
    provider_name = "openai"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/responses"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        payload = openai_response_payload(req)
        body, status, latency, headers, attempts = post_json_with_retry(
            self.endpoint,
            {"Authorization": f"Bearer {self.cfg.api_key}"},
            payload,
            self.cfg.retry,
        )
        text = body.get("output_text") or _extract_responses_text(body)
        return _envelope(self.provider_name, req, self.endpoint, body, payload, status, latency, headers, attempts, str(text))


class XAIAdapter:
    provider_name = "xai"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/responses"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        payload = responses_api_payload(req)
        body, status, latency, headers, attempts = post_json_with_retry(
            self.endpoint,
            {"Authorization": f"Bearer {self.cfg.api_key}"},
            payload,
            self.cfg.retry,
        )
        text = body.get("output_text") or _extract_responses_text(body)
        return _envelope(self.provider_name, req, self.endpoint, body, payload, status, latency, headers, attempts, str(text))


class AnthropicAdapter:
    provider_name = "anthropic"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/messages"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        payload: dict[str, Any] = {
            "model": req.model_id,
            "messages": [{"role": "user", "content": req.prompt}],
            "temperature": req.temperature,
            "max_tokens": req.max_tokens,
        }
        if req.system_prompt:
            payload["system"] = req.system_prompt
        body, status, latency, headers, attempts = post_json_with_retry(
            self.endpoint,
            {"x-api-key": self.cfg.api_key, "anthropic-version": "2023-06-01"},
            payload,
            self.cfg.retry,
        )
        text = "".join(
            str(part.get("text", ""))
            for part in body.get("content", [])
            if isinstance(part, dict) and part.get("type") == "text"
        )
        return _envelope(self.provider_name, req, self.endpoint, body, payload, status, latency, headers, attempts, text)


class GoogleAdapter:
    provider_name = "google"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = cfg.base_url.rstrip("/")

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        endpoint = f"{self.endpoint}/models/{req.model_id}:generateContent?key={self.cfg.api_key}"
        payload: dict[str, Any] = {
            "contents": [{"parts": [{"text": req.prompt}]}],
            "generationConfig": google_generation_config(req),
        }
        if req.system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": req.system_prompt}]}
        body, status, latency, headers, attempts = post_json_with_retry(
            endpoint, {}, payload, self.cfg.retry
        )
        text_parts: list[str] = []
        finish: list[str] = []
        for candidate in body.get("candidates", []):
            if not isinstance(candidate, dict):
                continue
            if candidate.get("finishReason"):
                finish.append(str(candidate["finishReason"]))
            for part in candidate.get("content", {}).get("parts", []):
                if isinstance(part, dict):
                    text_parts.append(str(part.get("text", "")))
        clean_endpoint = endpoint.split("?key=", 1)[0]
        envelope = _envelope(
            self.provider_name,
            req,
            clean_endpoint,
            body,
            payload,
            status,
            latency,
            headers,
            attempts,
            "".join(text_parts),
        )
        return ApiResponseEnvelope(
            **{**envelope.__dict__, "finish_reason": ";".join(finish) if finish else envelope.finish_reason}
        )


class OpenRouterAdapter:
    provider_name = "openrouter"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/chat/completions"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        messages = []
        if req.system_prompt:
            messages.append({"role": "system", "content": req.system_prompt})
        messages.append({"role": "user", "content": req.prompt})
        payload = {
            "model": req.model_id,
            "messages": messages,
            "temperature": req.temperature,
            "max_tokens": req.max_tokens,
        }
        body, status, latency, headers, attempts = post_json_with_retry(
            self.endpoint,
            {"Authorization": f"Bearer {self.cfg.api_key}"},
            payload,
            self.cfg.retry,
        )
        choices = body.get("choices", [])
        text = ""
        if choices and isinstance(choices[0], dict):
            content = choices[0].get("message", {}).get("content", "")
            text = content if isinstance(content, str) else str(content)
        return _envelope(self.provider_name, req, self.endpoint, body, payload, status, latency, headers, attempts, text)


def responses_api_payload(req: InferenceRequest) -> dict[str, Any]:
    prompt_input: Any = req.prompt
    if req.system_prompt:
        prompt_input = [
            {"role": "system", "content": req.system_prompt},
            {"role": "user", "content": req.prompt},
        ]
    return {"model": req.model_id, "input": prompt_input, "max_output_tokens": max(req.max_tokens, 1024)}


def openai_response_payload(req: InferenceRequest) -> dict[str, Any]:
    payload = responses_api_payload(req)
    if req.model_id.lower().startswith(("gpt-5", "o1", "o3", "o4")):
        payload["reasoning"] = {"effort": "none"}
    return payload


def google_generation_config(req: InferenceRequest) -> dict[str, Any]:
    config: dict[str, Any] = {
        "temperature": req.temperature,
        "maxOutputTokens": max(req.max_tokens, 1024),
        "responseMimeType": "application/json",
    }
    if req.model_id.lower().startswith("gemini-3"):
        config["thinkingConfig"] = {"thinkingLevel": "low"}
    return config


def build_adapters(configs: dict[str, ProviderConfig]) -> dict[str, ProviderAdapter]:
    adapter_types = {
        "mock": MockAdapter,
        "openai": OpenAIAdapter,
        "anthropic": AnthropicAdapter,
        "google": GoogleAdapter,
        "openrouter": OpenRouterAdapter,
        "llama": OpenRouterAdapter,
        "xai": XAIAdapter,
    }
    adapters: dict[str, ProviderAdapter] = {}
    for name, cfg in configs.items():
        adapter_type = adapter_types.get(name)
        if adapter_type is None:
            raise ValueError(f"No adapter for provider {name!r}")
        adapters[name] = adapter_type(cfg)
    return adapters


def _extract_responses_text(body: dict[str, Any]) -> str:
    parts: list[str] = []
    for item in body.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                parts.append(str(content.get("text", "")))
    return "".join(parts)


def _envelope(
    provider: str,
    req: InferenceRequest,
    endpoint: str,
    body: dict[str, Any],
    payload: dict[str, Any],
    status: int,
    latency: int,
    headers: dict[str, str],
    attempts: int,
    text: str,
) -> ApiResponseEnvelope:
    choices = body.get("choices", [])
    choice_finish = choices[0].get("finish_reason") if choices and isinstance(choices[0], dict) else None
    finish = body.get("stop_reason") or choice_finish
    usage = body.get("usage") or body.get("usageMetadata") or {}
    return ApiResponseEnvelope(
        provider=provider,
        request_model_id=req.model_id,
        resolved_model_id=str(body.get("model") or body.get("modelVersion") or req.model_id),
        endpoint=endpoint,
        status_code=status,
        raw_text=text,
        latency_ms=latency,
        attempts=attempts,
        request_payload=payload,
        response_payload=body,
        response_headers=headers,
        response_id=str(body["id"]) if body.get("id") is not None else None,
        finish_reason=str(finish) if finish is not None else None,
        usage=usage if isinstance(usage, dict) else {},
    )
