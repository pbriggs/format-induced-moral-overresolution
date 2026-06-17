from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


class ConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProviderConfig:
    provider_name: str
    api_key: str
    base_url: str
    default_model_id: str


@dataclass(frozen=True)
class ExecutionConfig:
    providers: dict[str, ProviderConfig]
    model_to_provider: dict[str, str]
    model_ids: tuple[str, ...]
    max_attempts_per_call: int = 5
    base_backoff_seconds: float = 0.5
    max_recent_retryable_errors: int = 20
    max_recent_server_errors: int = 10
    max_recent_rate_limits: int = 10
    recent_failure_window_minutes: float = 10.0


def _read_windows_user_env(name: str) -> Optional[str]:
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


def parse_model_ids(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(part.strip() for part in raw.split(",") if part.strip())


def infer_provider_for_model(model_id: str) -> str:
    lower = model_id.lower()
    if lower.startswith(("gpt-", "o1", "o3", "o4")):
        return "openai"
    if lower.startswith("claude-"):
        return "anthropic"
    if lower.startswith("gemini-"):
        return "google"
    if any(name in lower for name in ("llama", "meta-llama", "qwen", "mistral", "deepseek")):
        return "llama"
    if lower.startswith("mock-"):
        return "mock"
    raise ConfigurationError(
        f"Cannot infer provider for model {model_id!r}; set STUDY_MODEL_PROVIDER_MAP as model=provider pairs."
    )


def parse_provider_map(raw: str | None) -> dict[str, str]:
    if not raw:
        return {}
    mapping: dict[str, str] = {}
    for chunk in raw.split(","):
        if not chunk.strip():
            continue
        if "=" not in chunk:
            raise ConfigurationError("STUDY_MODEL_PROVIDER_MAP must use model=provider comma-separated pairs")
        model, provider = chunk.split("=", 1)
        mapping[model.strip()] = provider.strip().lower()
    return mapping


def load_execution_config(model_ids: tuple[str, ...], mock_provider: bool = False) -> ExecutionConfig:
    if len(model_ids) != 5:
        raise ConfigurationError(f"Expected exactly 5 model IDs, got {len(model_ids)}")
    if any(model.startswith("model_slot_") for model in model_ids):
        raise ConfigurationError("Placeholder model IDs are not allowed for provider execution")

    if mock_provider:
        return ExecutionConfig(
            providers={"mock": ProviderConfig("mock", "mock", "mock://local", "mock-model")},
            model_to_provider={model_id: "mock" for model_id in model_ids},
            model_ids=model_ids,
        )

    providers = {
        "openai": ProviderConfig(
            "openai",
            require_env("OPENAI_API_KEY"),
            getenv("OPENAI_BASE_URL", "https://api.openai.com/v1") or "https://api.openai.com/v1",
            require_env("OPENAI_MODEL"),
        ),
        "anthropic": ProviderConfig(
            "anthropic",
            require_env("ANTHROPIC_API_KEY"),
            getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1") or "https://api.anthropic.com/v1",
            require_env("ANTHROPIC_MODEL"),
        ),
        "google": ProviderConfig(
            "google",
            require_env("GOOGLE_API_KEY"),
            getenv("GOOGLE_GENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
            or "https://generativelanguage.googleapis.com/v1beta",
            require_env("GOOGLE_MODEL"),
        ),
        "llama": ProviderConfig(
            "llama",
            require_env("LLAMA_API_KEY"),
            getenv("LLAMA_BASE_URL", "https://openrouter.ai/api/v1") or "https://openrouter.ai/api/v1",
            require_env("LLAMA_MODEL"),
        ),
    }
    explicit_map = parse_provider_map(getenv("STUDY_MODEL_PROVIDER_MAP"))
    model_to_provider = {model: explicit_map.get(model, infer_provider_for_model(model)) for model in model_ids}
    missing = sorted({provider for provider in model_to_provider.values() if provider not in providers})
    if missing:
        raise ConfigurationError(f"No provider config for provider(s): {', '.join(missing)}")
    return ExecutionConfig(providers=providers, model_to_provider=model_to_provider, model_ids=model_ids)
