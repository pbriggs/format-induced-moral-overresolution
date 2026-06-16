from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class ModelRegistryEntry:
    model_id: str
    provider: str
    api_route: str
    model_family: str
    model_display_name: str
    provider_model_id: str
    provider_model_version_if_available: str | None
    open_weight_flag: bool
    structured_output_mode: str
    batch_supported_flag: bool
    sampling_control_available: bool
    logprobs_available: bool
    run_freeze_verified_at: str | None
    provider_metadata_json: dict[str, Any]
    pricing_metadata_json: dict[str, Any]

    def to_record(self) -> dict[str, Any]:
        record = asdict(self)
        for field in (
            "open_weight_flag",
            "batch_supported_flag",
            "sampling_control_available",
            "logprobs_available",
        ):
            record[field] = int(record[field])
        return record

