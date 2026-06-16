from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from protocol.call_milestones import call_milestone_payload
from protocol.endpoint_registry import PRIMARY_ENDPOINTS, SECONDARY_ENDPOINTS
from protocol.label_schema import CANONICAL_SCHEMA
from protocol.robustness_plan import ROBUSTNESS_CHECKS


def preregistration_payload() -> dict:
    return {
        "label_schema": {
            "version": CANONICAL_SCHEMA.version,
            "labels": list(CANONICAL_SCHEMA.labels),
            "definitions": CANONICAL_SCHEMA.definitions,
        },
        "primary_endpoints": [asdict(endpoint) for endpoint in PRIMARY_ENDPOINTS],
        "secondary_endpoints": list(SECONDARY_ENDPOINTS),
        "robustness_checks": list(ROBUSTNESS_CHECKS),
        "call_milestones": call_milestone_payload(),
        "primary_validity_statuses": ["valid_strict_schema", "valid_after_repair"],
    }


def write_preregistration_json(path: str | Path) -> None:
    Path(path).write_text(json.dumps(preregistration_payload(), sort_keys=True, indent=2), encoding="utf-8")
