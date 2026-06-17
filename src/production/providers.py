from __future__ import annotations

from dataclasses import dataclass, field
import json
import random
import time
from typing import Any, Protocol
from urllib import error, request

from production.config import ProviderConfig


RETRY_STATUSES = {408, 409, 425, 429, 500, 502, 503, 504}


class ProviderRequestError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_headers: dict[str, str] | None = None,
        error_response_body: str | None = None,
        retry_after_seconds: float | None = None,
        transport_error_message: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_headers = response_headers or {}
        self.error_response_body = error_response_body
        self.retry_after_seconds = retry_after_seconds
        self.transport_error_message = transport_error_message


@dataclass(frozen=True)
class InferenceRequest:
    prompt: str
    model_id: str
    prompt_mode: str
    temperature: float = 0.0
    max_tokens: int = 512
    response_schema: str | None = None


@dataclass(frozen=True)
class ApiResponseEnvelope:
    provider: str
    request_model_id: str
    resolved_model_id: str
    endpoint: str
    status_code: int
    raw_text: str
    latency_ms: int
    request_payload: dict[str, Any]
    response_payload: dict[str, Any]
    response_headers: dict[str, str] = field(default_factory=dict)
    finish_reason: str | None = None
    finish_metadata: dict[str, Any] = field(default_factory=dict)


class ProviderAdapter(Protocol):
    provider_name: str
    endpoint: str

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        ...


def _retry_after(headers: dict[str, str]) -> float | None:
    raw = headers.get("retry-after") or headers.get("Retry-After")
    if not raw:
        return None
    try:
        parsed = float(raw)
    except ValueError:
        return None
    return parsed if parsed > 0 else None


def _sleep_seconds(headers: dict[str, str], attempt: int, base_backoff_seconds: float) -> float:
    retry_after = _retry_after(headers)
    if retry_after is not None:
        return retry_after
    return base_backoff_seconds * (2 ** (attempt - 1)) + random.uniform(0.0, 0.25)


def post_json_with_retry(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    max_attempts: int = 5,
    base_backoff_seconds: float = 0.5,
    timeout_seconds: float = 60.0,
) -> tuple[dict[str, Any], int, int, dict[str, str]]:
    last_error: ProviderRequestError | None = None
    body_bytes = json.dumps(payload).encode("utf-8")
    request_headers = {"Content-Type": "application/json", **headers}
    for attempt in range(1, max_attempts + 1):
        started = time.perf_counter()
        req = request.Request(url, data=body_bytes, headers=request_headers, method="POST")
        try:
            with request.urlopen(req, timeout=timeout_seconds) as resp:
                latency_ms = int((time.perf_counter() - started) * 1000)
                response_body = resp.read().decode("utf-8")
                response_headers = dict(resp.headers.items())
                return json.loads(response_body), int(resp.status), latency_ms, response_headers
        except error.HTTPError as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            response_headers = dict(exc.headers.items()) if exc.headers is not None else {}
            error_body = exc.read().decode("utf-8", errors="replace")
            retry_after = _retry_after(response_headers)
            last_error = ProviderRequestError(
                f"HTTP {exc.code}: {_error_detail(error_body)}",
                status_code=int(exc.code),
                response_headers=response_headers,
                error_response_body=error_body,
                retry_after_seconds=retry_after,
            )
            if exc.code not in RETRY_STATUSES or attempt >= max_attempts:
                raise last_error from exc
            time.sleep(_sleep_seconds(response_headers, attempt, base_backoff_seconds))
        except (TimeoutError, OSError) as exc:
            last_error = ProviderRequestError(
                f"Transport error: {exc}",
                transport_error_message=str(exc),
            )
            if attempt >= max_attempts:
                raise last_error from exc
            time.sleep(base_backoff_seconds * (2 ** (attempt - 1)) + random.uniform(0.0, 0.25))
        except json.JSONDecodeError as exc:
            raise ProviderRequestError(f"Provider returned non-JSON response: {exc}", status_code=200) from exc
    raise last_error or ProviderRequestError("Retry exhausted")


def _error_detail(body: str, max_chars: int = 1200) -> str:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        clean = body.strip().replace("\n", " ").replace("\r", " ")
        return clean[:max_chars] if clean else "(empty response body)"
    if isinstance(payload, dict):
        err = payload.get("error")
        if isinstance(err, dict):
            parts = [str(err.get(key)) for key in ("type", "code", "message") if err.get(key)]
            if parts:
                return "; ".join(parts)
    return json.dumps(payload, sort_keys=True)[:max_chars]


class MockAdapter:
    provider_name = "mock"
    endpoint = "mock://local"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        if "distribution" in req.prompt_mode:
            text = json.dumps(
                {
                    "label_probabilities": {
                        "author": 0.4,
                        "other": 0.25,
                        "everybody": 0.2,
                        "nobody": 0.1,
                        "info": 0.05,
                    },
                    "most_likely_label": "author",
                }
            )
        elif "normative" in req.prompt_mode:
            text = json.dumps({"chosen_label": "author", "moral_certainty": 0.78})
        elif "sampling" in req.prompt_mode:
            text = json.dumps({"chosen_label": "author"})
        else:
            text = json.dumps({"chosen_label": "author", "estimated_source_community_agreement": 0.72})
        return ApiResponseEnvelope(
            provider=self.provider_name,
            request_model_id=req.model_id,
            resolved_model_id=f"{req.model_id}-mock-snapshot",
            endpoint=self.endpoint,
            status_code=200,
            raw_text=text,
            latency_ms=1,
            request_payload={"prompt": req.prompt, "model": req.model_id, "temperature": req.temperature},
            response_payload={"mock": True, "text": text},
        )


class OpenAIAdapter:
    provider_name = "openai"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/responses"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        payload = openai_response_payload(req)
        body, status, latency, headers = post_json_with_retry(
            self.endpoint,
            {"Authorization": f"Bearer {self.cfg.api_key}"},
            payload,
        )
        text = body.get("output_text") or _extract_openai_text(body)
        return ApiResponseEnvelope("openai", req.model_id, str(body.get("model", req.model_id)), self.endpoint, status, text, latency, payload, body, headers)


class XAIAdapter:
    provider_name = "xai"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/responses"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        payload = xai_response_payload(req)
        body, status, latency, headers = post_json_with_retry(
            self.endpoint,
            {"Authorization": f"Bearer {self.cfg.api_key}"},
            payload,
        )
        text = body.get("output_text") or _extract_openai_text(body)
        return ApiResponseEnvelope("xai", req.model_id, str(body.get("model", req.model_id)), self.endpoint, status, text, latency, payload, body, headers)


def openai_response_payload(req: InferenceRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": req.model_id,
        "input": req.prompt,
        "max_output_tokens": max(req.max_tokens, 1024),
    }
    lower = req.model_id.lower()
    if lower.startswith(("gpt-5", "o1", "o3", "o4")):
        payload["reasoning"] = {"effort": "none"}
    return payload


def xai_response_payload(req: InferenceRequest) -> dict[str, Any]:
    return {
        "model": req.model_id,
        "input": req.prompt,
        "max_output_tokens": max(req.max_tokens, 1024),
    }


class AnthropicAdapter:
    provider_name = "anthropic"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/messages"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        payload = {"model": req.model_id, "messages": [{"role": "user", "content": req.prompt}], "temperature": req.temperature, "max_tokens": req.max_tokens}
        body, status, latency, headers = post_json_with_retry(
            self.endpoint,
            {"x-api-key": self.cfg.api_key, "anthropic-version": "2023-06-01"},
            payload,
        )
        text = "".join(part.get("text", "") for part in body.get("content", []) if isinstance(part, dict) and part.get("type") == "text")
        return ApiResponseEnvelope("anthropic", req.model_id, str(body.get("model", req.model_id)), self.endpoint, status, text, latency, payload, body, headers, finish_reason=body.get("stop_reason"))


class GoogleAdapter:
    provider_name = "google"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = cfg.base_url.rstrip("/")

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        endpoint = f"{self.endpoint}/models/{req.model_id}:generateContent?key={self.cfg.api_key}"
        payload = {
            "contents": [{"parts": [{"text": req.prompt}]}],
            "generationConfig": google_generation_config(req),
        }
        body, status, latency, headers = post_json_with_retry(endpoint, {}, payload)
        text = ""
        finish: list[str] = []
        for candidate in body.get("candidates", []):
            finish_reason = candidate.get("finishReason")
            if finish_reason:
                finish.append(str(finish_reason))
            for part in candidate.get("content", {}).get("parts", []):
                text += part.get("text", "")
        clean_endpoint = endpoint.split("?key=", 1)[0]
        return ApiResponseEnvelope("google", req.model_id, str(body.get("modelVersion", req.model_id)), clean_endpoint, status, text, latency, payload, body, headers, finish_reason=";".join(finish) if finish else None)


def google_generation_config(req: InferenceRequest) -> dict[str, Any]:
    config: dict[str, Any] = {
        "temperature": req.temperature,
        "maxOutputTokens": max(req.max_tokens, 1024),
        "responseMimeType": "application/json",
    }
    if req.model_id.lower().startswith("gemini-3"):
        config["thinkingConfig"] = {"thinkingLevel": "low"}
    return config


class LlamaAdapter:
    provider_name = "llama"

    def __init__(self, cfg: ProviderConfig) -> None:
        self.cfg = cfg
        self.endpoint = f"{cfg.base_url.rstrip('/')}/chat/completions"

    def run_single_turn(self, req: InferenceRequest) -> ApiResponseEnvelope:
        payload = {"model": req.model_id, "messages": [{"role": "user", "content": req.prompt}], "temperature": req.temperature, "max_tokens": req.max_tokens}
        body, status, latency, headers = post_json_with_retry(
            self.endpoint,
            {"Authorization": f"Bearer {self.cfg.api_key}"},
            payload,
        )
        text = ""
        choices = body.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "")
            text = content if isinstance(content, str) else str(content)
        return ApiResponseEnvelope("llama", req.model_id, str(body.get("model", req.model_id)), self.endpoint, status, text, latency, payload, body, headers)


def build_adapters(configs: dict[str, ProviderConfig]) -> dict[str, ProviderAdapter]:
    adapters: dict[str, ProviderAdapter] = {}
    for provider, cfg in configs.items():
        if provider == "mock":
            adapters[provider] = MockAdapter()
        elif provider == "openai":
            adapters[provider] = OpenAIAdapter(cfg)
        elif provider == "anthropic":
            adapters[provider] = AnthropicAdapter(cfg)
        elif provider == "google":
            adapters[provider] = GoogleAdapter(cfg)
        elif provider == "llama":
            adapters[provider] = LlamaAdapter(cfg)
        elif provider == "xai":
            adapters[provider] = XAIAdapter(cfg)
    return adapters


def _extract_openai_text(body: dict[str, Any]) -> str:
    parts: list[str] = []
    for item in body.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                parts.append(str(content.get("text", "")))
    return "".join(parts)
