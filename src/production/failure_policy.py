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


TERMINAL_FAILURE_KINDS: frozenset[ApiFailureKind] = frozenset(
    {
        ApiFailureKind.AUTHORIZATION,
        ApiFailureKind.BAD_REQUEST,
        ApiFailureKind.SAFETY_FILTER,
    }
)

RETRYABLE_FAILURE_KINDS: frozenset[ApiFailureKind] = frozenset(
    {
        ApiFailureKind.RATE_LIMIT,
        ApiFailureKind.SERVER_ERROR,
        ApiFailureKind.TIMEOUT,
        ApiFailureKind.UNKNOWN,
    }
)


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
    retry_after_seconds: float | None = None,
) -> FailureDecision:
    normalized_error = (error_type or "").strip().lower()
    if http_status_code is None and not normalized_error:
        return FailureDecision(ApiFailureKind.NONE, retryable=False, terminal=False)
    if http_status_code in {401, 403} or normalized_error in {"auth", "authentication", "authorization"}:
        return FailureDecision(ApiFailureKind.AUTHORIZATION, retryable=False, terminal=True, reason="authorization failure")
    if http_status_code == 400 or normalized_error in {"bad_request", "invalid_request"}:
        return FailureDecision(ApiFailureKind.BAD_REQUEST, retryable=False, terminal=True, reason="bad request")
    if http_status_code == 429 or normalized_error in {"rate_limit", "rate_limited"}:
        return FailureDecision(
            ApiFailureKind.RATE_LIMIT,
            retryable=True,
            terminal=False,
            retry_after_seconds=retry_after_seconds,
            reason="rate limited",
        )
    if http_status_code is not None and 500 <= http_status_code <= 599:
        return FailureDecision(ApiFailureKind.SERVER_ERROR, retryable=True, terminal=False, reason="provider server error")
    if normalized_error in {"timeout", "connection_error", "network_error", "transport_error"}:
        return FailureDecision(ApiFailureKind.TIMEOUT, retryable=True, terminal=False, reason="transport failure")
    if normalized_error in {"safety_filter", "content_filter", "policy_refusal"}:
        return FailureDecision(ApiFailureKind.SAFETY_FILTER, retryable=False, terminal=True, reason="provider safety filter")
    if normalized_error in {"parse_or_schema", "invalid_json", "schema_error"}:
        return FailureDecision(ApiFailureKind.PARSE_OR_SCHEMA, retryable=False, terminal=False, reason="unexpected response schema")
    return FailureDecision(ApiFailureKind.UNKNOWN, retryable=True, terminal=False, reason="unknown provider error")


def should_retry_call(
    retry_count: int,
    failure: FailureDecision,
    max_retries_per_call: int = 3,
) -> bool:
    if failure.terminal or not failure.retryable:
        return False
    return retry_count < max_retries_per_call


def circuit_breaker_decision(
    recent_failures: Iterable[Mapping[str, object]],
    max_retryable_errors: int = 20,
    max_server_errors: int = 10,
    max_rate_limits: int = 10,
) -> CircuitBreakerDecision:
    retryable = 0
    server_errors = 0
    rate_limits = 0
    for row in recent_failures:
        decision = classify_api_failure(
            http_status_code=_optional_int(row.get("http_status_code")),
            error_type=_optional_str(row.get("api_error_type")),
        )
        if decision.retryable:
            retryable += 1
        if decision.kind == ApiFailureKind.SERVER_ERROR:
            server_errors += 1
        if decision.kind == ApiFailureKind.RATE_LIMIT:
            rate_limits += 1
    if server_errors >= max_server_errors:
        return CircuitBreakerDecision(True, "too many recent provider 5xx errors", retryable, server_errors, rate_limits)
    if rate_limits >= max_rate_limits:
        return CircuitBreakerDecision(True, "too many recent rate-limit errors", retryable, server_errors, rate_limits)
    if retryable >= max_retryable_errors:
        return CircuitBreakerDecision(True, "too many recent retryable provider errors", retryable, server_errors, rate_limits)
    return CircuitBreakerDecision(False, "within retry budget", retryable, server_errors, rate_limits)


def _optional_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
