from __future__ import annotations

from dataclasses import dataclass

from parsing.validity_status import ValidityStatus

PRIMARY_VALID_STATUSES = frozenset(
    {
        ValidityStatus.VALID_STRICT_SCHEMA,
        ValidityStatus.VALID_AFTER_REPAIR,
        ValidityStatus.VALID_EXTRACTED_JSON,
    }
)


@dataclass(frozen=True)
class ExclusionDecision:
    include_primary: bool
    rule: str | None = None
    reason: str | None = None


def primary_output_exclusion(validity_status: str | ValidityStatus) -> ExclusionDecision:
    status = ValidityStatus(validity_status)
    if status in PRIMARY_VALID_STATUSES:
        return ExclusionDecision(True)
    return ExclusionDecision(False, "invalid_or_unusable_output_v1", f"{status.value} excluded from primary analysis")


def source_item_exclusion(
    info_support: float,
    majority_label: str,
    exclude_info_majority: bool = False,
    high_info_threshold: float | None = None,
) -> ExclusionDecision:
    if exclude_info_majority and majority_label == "info":
        return ExclusionDecision(False, "info_majority_sensitivity_v1", "info is source-community majority label")
    if high_info_threshold is not None and info_support >= high_info_threshold:
        return ExclusionDecision(False, "high_info_sensitivity_v1", f"info support >= {high_info_threshold}")
    return ExclusionDecision(True)
