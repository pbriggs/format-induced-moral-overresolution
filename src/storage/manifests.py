from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
import json
import subprocess
from typing import Any

from utils.hashing import stable_hash


@dataclass(frozen=True)
class RunManifest:
    run_id: str
    created_at: str
    git_commit: str | None
    dataset_versions: dict[str, Any] = field(default_factory=dict)
    source_distribution_versions: dict[str, Any] = field(default_factory=dict)
    config_hashes: dict[str, str] = field(default_factory=dict)
    prompt_template_hashes: dict[str, str] = field(default_factory=dict)
    model_versions: dict[str, Any] = field(default_factory=dict)
    api_parameters: dict[str, Any] = field(default_factory=dict)
    random_seeds: dict[str, int] = field(default_factory=dict)
    call_milestone: dict[str, Any] = field(default_factory=dict)
    planned_call_budget: int | None = None
    planned_call_count: int | None = None
    sequential_monitoring_plan: str = ""
    exclusion_rules_version: str = "v1"
    metric_registry_version: str = "v1"
    analysis_code_version: str = "v1"
    operator_notes: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=2)

    @property
    def manifest_hash(self) -> str:
        return stable_hash(asdict(self))


def current_git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def create_manifest(run_id: str, **kwargs: Any) -> RunManifest:
    return RunManifest(
        run_id=run_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        git_commit=current_git_commit(),
        **kwargs,
    )
