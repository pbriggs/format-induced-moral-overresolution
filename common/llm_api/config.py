from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


class ConfigurationError(RuntimeError):
    """Raised when provider configuration is absent or inconsistent."""


@dataclass(frozen=True)
class RetryConfig:
    max_attempts: int = 5
    base_backoff_seconds: float = 0.5
    timeout_seconds: float = 60.0
    jitter_seconds: float = 0.25

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if min(self.base_backoff_seconds, self.timeout_seconds, self.jitter_seconds) < 0:
            raise ValueError("retry timing values cannot be negative")


@dataclass(frozen=True)
class ProviderConfig:
    provider_name: str
    api_key: str
    base_url: str
    default_model_id: str | None = None
    retry: RetryConfig = RetryConfig()


def _read_windows_user_env(name: str) -> Optional[str]:
    """Read a persistent per-user Windows variable if this process missed it."""
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
    except (FileNotFoundError, OSError):
        return None
    return str(value) if value is not None else None


def getenv(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is not None and value.strip():
        return value.strip()
    user_value = _read_windows_user_env(name)
    if user_value is not None and user_value.strip():
        os.environ[name] = user_value.strip()
        return user_value.strip()
    return default


def require_env(name: str) -> str:
    value = getenv(name)
    if not value:
        raise ConfigurationError(f"Missing required environment variable: {name}")
    return value


def _require_one_env(primary: str, fallback: str) -> str:
    value = getenv(primary) or getenv(fallback)
    if not value:
        raise ConfigurationError(
            f"Missing required environment variable: {primary} (or compatibility alias {fallback})"
        )
    return value


def infer_provider_for_model(model_id: str) -> str:
    lower = model_id.lower()
    if lower.startswith(("gpt-", "o1", "o3", "o4")):
        return "openai"
    if lower.startswith("claude-"):
        return "anthropic"
    if lower.startswith("gemini-"):
        return "google"
    if lower.startswith("grok-"):
        return "xai"
    if any(name in lower for name in ("llama", "meta-llama", "qwen", "mistral", "deepseek")):
        return "openrouter"
    if lower.startswith("mock-"):
        return "mock"
    raise ConfigurationError(
        f"Cannot infer provider for model {model_id!r}; supply an explicit model-to-provider mapping."
    )


def parse_provider_map(raw: str | None) -> dict[str, str]:
    """Parse ``model=provider,model=provider`` into a normalized mapping."""
    if not raw:
        return {}
    mapping: dict[str, str] = {}
    for chunk in raw.split(","):
        if not chunk.strip():
            continue
        if "=" not in chunk:
            raise ConfigurationError(
                "MODEL_PROVIDER_MAP must use model=provider comma-separated pairs"
            )
        model, provider = chunk.split("=", 1)
        model, provider = model.strip(), provider.strip().lower()
        if not model or not provider:
            raise ConfigurationError(f"Invalid provider mapping entry: {chunk!r}")
        mapping[model] = provider
    return mapping


def load_provider_configs(
    model_ids: tuple[str, ...] | list[str],
    provider_map: dict[str, str] | None = None,
    retry: RetryConfig | None = None,
) -> tuple[dict[str, ProviderConfig], dict[str, str]]:
    """Load only the credentials needed by ``model_ids``.

    Returns ``(provider_configs, model_to_provider)``. No secret is logged or
    included in exception messages.
    """
    retry = retry or RetryConfig()
    explicit = provider_map if provider_map is not None else parse_provider_map(getenv("MODEL_PROVIDER_MAP"))
    model_to_provider = {
        model: explicit[model] if model in explicit else infer_provider_for_model(model)
        for model in model_ids
    }
    needed = set(model_to_provider.values())
    factories = {
        "openai": lambda: ProviderConfig(
            "openai",
            require_env("OPENAI_API_KEY"),
            getenv("OPENAI_BASE_URL", "https://api.openai.com/v1") or "",
            getenv("OPENAI_MODEL"),
            retry,
        ),
        "anthropic": lambda: ProviderConfig(
            "anthropic",
            require_env("ANTHROPIC_API_KEY"),
            getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1") or "",
            getenv("ANTHROPIC_MODEL"),
            retry,
        ),
        "google": lambda: ProviderConfig(
            "google",
            require_env("GOOGLE_API_KEY"),
            getenv("GOOGLE_GENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
            or "",
            getenv("GOOGLE_MODEL"),
            retry,
        ),
        "openrouter": lambda: ProviderConfig(
            "openrouter",
            _require_one_env("OPENROUTER_API_KEY", "LLAMA_API_KEY"),
            getenv("OPENROUTER_BASE_URL")
            or getenv("LLAMA_BASE_URL")
            or "https://openrouter.ai/api/v1",
            getenv("OPENROUTER_MODEL") or getenv("LLAMA_MODEL"),
            retry,
        ),
        # Compatibility with the original project's LLAMA_* variable names.
        "llama": lambda: ProviderConfig(
            "openrouter",
            require_env("LLAMA_API_KEY"),
            getenv("LLAMA_BASE_URL", "https://openrouter.ai/api/v1") or "",
            getenv("LLAMA_MODEL"),
            retry,
        ),
        "xai": lambda: ProviderConfig(
            "xai",
            require_env("XAI_API_KEY"),
            getenv("XAI_BASE_URL", "https://api.x.ai/v1") or "",
            getenv("XAI_MODEL"),
            retry,
        ),
        "mock": lambda: ProviderConfig("mock", "mock", "mock://local", "mock-model", retry),
    }
    unsupported = sorted(needed - factories.keys())
    if unsupported:
        raise ConfigurationError(f"Unsupported provider(s): {', '.join(unsupported)}")
    return ({name: factories[name]() for name in sorted(needed)}, model_to_provider)
