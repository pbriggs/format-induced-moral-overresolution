from __future__ import annotations

from enum import StrEnum


class ValidityStatus(StrEnum):
    VALID_STRICT_SCHEMA = "valid_strict_schema"
    VALID_AFTER_REPAIR = "valid_after_repair"
    VALID_EXTRACTED_JSON = "valid_extracted_json"
    INVALID_JSON = "invalid_json"
    MISSING_REQUIRED_FIELD = "missing_required_field"
    PROBABILITY_SUM_ERROR = "probability_sum_error"
    PROBABILITY_OUT_OF_BOUNDS = "probability_out_of_bounds"
    OFF_SCHEMA_LABEL = "off_schema_label"
    REFUSAL = "refusal"
    SAFETY_FILTER = "safety_filter"
    API_ERROR = "api_error"
    EMPTY_RESPONSE = "empty_response"
