"""Small, dependency-free clients for the LLM providers used in this project."""

from .config import (
    ConfigurationError,
    ProviderConfig,
    RetryConfig,
    getenv,
    infer_provider_for_model,
    load_provider_configs,
    parse_provider_map,
    require_env,
)
from .failure_policy import (
    ApiFailureKind,
    CircuitBreakerDecision,
    FailureDecision,
    circuit_breaker_decision,
    classify_api_failure,
    should_retry_call,
)
from .json_output import JsonOutput, JsonOutputStatus, parse_json_output, validate_object
from .providers import (
    ApiResponseEnvelope,
    InferenceRequest,
    ProviderAdapter,
    ProviderRequestError,
    build_adapters,
    post_json_with_retry,
)

__all__ = [
    "ApiFailureKind",
    "ApiResponseEnvelope",
    "CircuitBreakerDecision",
    "ConfigurationError",
    "FailureDecision",
    "InferenceRequest",
    "JsonOutput",
    "JsonOutputStatus",
    "ProviderAdapter",
    "ProviderConfig",
    "ProviderRequestError",
    "RetryConfig",
    "build_adapters",
    "circuit_breaker_decision",
    "classify_api_failure",
    "getenv",
    "infer_provider_for_model",
    "load_provider_configs",
    "parse_json_output",
    "parse_provider_map",
    "post_json_with_retry",
    "require_env",
    "should_retry_call",
    "validate_object",
]
