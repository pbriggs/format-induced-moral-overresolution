from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum


class ApiFailureKind(StrEnum):
    NONE = "none"
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    TIMEOUT = "timeout"
    AUTHORIZATION = "authorization"
    BAD_REQUEST = "bad_request"
    SAFETY_FILTER = "safety_filter"
    PARSE_OR_SCHEMA = "parse_or_schema"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FailureDecision:
    kind: ApiFailureKind
    retryable: bool
    terminal: bool
    retry_after_seconds: float | None = None
    reason: str = ""


@dataclass(frozen=True)
class CircuitBreakerDecision:
    abort: bool
    reason: str
    retryable_error_count: int
    server_error_count: int
    rate_limit_count: int


def classify_api_failure(
    http_status_code: int | None = None,
    error_type: str | None = None,
    error_response_body: str | None = None,
    retry_after_seconds: float | None = None,
) -> FailureDecision:
    normalized_error = (error_type or "").strip().lower()
    normalized_body = (error_response_body or "").strip().lower()
    if http_status_code is None and not normalized_error:
        return FailureDecision(ApiFailureKind.NONE, False, False)
    if http_status_code == 403 and any(
        token in normalized_body for token in ("key limit exceeded", "resource-exhausted", "rate limit")
    ):
        return FailureDecision(
            ApiFailureKind.RATE_LIMIT, True, False, retry_after_seconds, "provider account limit exceeded"
        )
    if http_status_code in {401, 403} or normalized_error in {
        "auth",
        "authentication",
        "authorization",
    }:
        return FailureDecision(ApiFailureKind.AUTHORIZATION, False, True, reason="authorization failure")
    if http_status_code in {400, 404, 405, 413, 422} or normalized_error in {
        "bad_request",
        "invalid_request",
    }:
        return FailureDecision(ApiFailureKind.BAD_REQUEST, False, True, reason="bad request")
    if http_status_code in {408, 409, 425, 429} or normalized_error in {
        "rate_limit",
        "rate_limited",
    }:
        kind = ApiFailureKind.RATE_LIMIT if http_status_code == 429 or "rate" in normalized_error else ApiFailureKind.TIMEOUT
        return FailureDecision(kind, True, False, retry_after_seconds, "transient client/provider condition")
    if http_status_code is not None and 500 <= http_status_code <= 599:
        return FailureDecision(ApiFailureKind.SERVER_ERROR, True, False, reason="provider server error")
    if normalized_error in {"timeout", "connection_error", "network_error", "transport_error"}:
        return FailureDecision(ApiFailureKind.TIMEOUT, True, False, reason="transport failure")
    if normalized_error in {"safety_filter", "content_filter", "policy_refusal"}:
        return FailureDecision(ApiFailureKind.SAFETY_FILTER, False, True, reason="provider safety filter")
    if normalized_error in {"parse_or_schema", "invalid_json", "schema_error"}:
        return FailureDecision(ApiFailureKind.PARSE_OR_SCHEMA, False, False, reason="unexpected response schema")
    return FailureDecision(ApiFailureKind.UNKNOWN, True, False, reason="unknown provider error")


def should_retry_call(retry_count: int, failure: FailureDecision, max_retries_per_call: int = 3) -> bool:
    return failure.retryable and not failure.terminal and retry_count < max_retries_per_call


def circuit_breaker_decision(
    recent_failures: Iterable[Mapping[str, object]],
    max_retryable_errors: int = 20,
    max_server_errors: int = 10,
    max_rate_limits: int = 10,
) -> CircuitBreakerDecision:
    retryable = server_errors = rate_limits = 0
    for row in recent_failures:
        decision = classify_api_failure(
            http_status_code=_optional_int(row.get("http_status_code")),
            error_type=_optional_str(row.get("api_error_type")),
            error_response_body=_optional_str(row.get("error_response_body")),
        )
        retryable += int(decision.retryable)
        server_errors += int(decision.kind == ApiFailureKind.SERVER_ERROR)
        rate_limits += int(decision.kind == ApiFailureKind.RATE_LIMIT)
    if server_errors >= max_server_errors:
        return CircuitBreakerDecision(True, "too many recent provider 5xx errors", retryable, server_errors, rate_limits)
    if rate_limits >= max_rate_limits:
        return CircuitBreakerDecision(True, "too many recent rate-limit errors", retryable, server_errors, rate_limits)
    if retryable >= max_retryable_errors:
        return CircuitBreakerDecision(True, "too many recent retryable provider errors", retryable, server_errors, rate_limits)
    return CircuitBreakerDecision(False, "within retry budget", retryable, server_errors, rate_limits)


def _optional_int(value: object) -> int | None:
    return None if value in {None, ""} else int(value)  # type: ignore[arg-type]


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)
