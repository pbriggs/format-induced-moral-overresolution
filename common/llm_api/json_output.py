from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
import json
from typing import Any


class JsonOutputStatus(StrEnum):
    VALID_JSON = "valid_json"
    VALID_EXTRACTED_JSON = "valid_extracted_json"
    EMPTY_RESPONSE = "empty_response"
    INVALID_JSON = "invalid_json"
    SCHEMA_ERROR = "schema_error"


@dataclass(frozen=True)
class JsonOutput:
    status: JsonOutputStatus
    value: dict[str, Any] | None
    errors: tuple[str, ...] = field(default_factory=tuple)
    extracted_json: bool = False

    @property
    def valid(self) -> bool:
        return self.status in {JsonOutputStatus.VALID_JSON, JsonOutputStatus.VALID_EXTRACTED_JSON}


def parse_json_output(
    raw_text: str,
    *,
    required_fields: tuple[str, ...] = (),
    allowed_values: dict[str, set[str] | tuple[str, ...] | list[str]] | None = None,
    numeric_ranges: dict[str, tuple[float, float]] | None = None,
) -> JsonOutput:
    """Parse an object, tolerating exactly one balanced object around prose.

    The optional checks cover the common API-output contract without coupling
    this module to the moral-label schema in the source project.
    """
    if raw_text is None or not raw_text.strip():
        return JsonOutput(JsonOutputStatus.EMPTY_RESPONSE, None, ("empty response",))
    extracted = False
    try:
        value = json.loads(raw_text)
    except json.JSONDecodeError as original_error:
        candidate = extract_single_json_object(raw_text)
        if candidate is None:
            return JsonOutput(JsonOutputStatus.INVALID_JSON, None, (str(original_error),))
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError as extracted_error:
            return JsonOutput(
                JsonOutputStatus.INVALID_JSON,
                None,
                (str(original_error), str(extracted_error)),
                True,
            )
        extracted = True
    if not isinstance(value, dict):
        return JsonOutput(JsonOutputStatus.INVALID_JSON, None, ("top-level value is not an object",), extracted)
    errors = validate_object(
        value,
        required_fields=required_fields,
        allowed_values=allowed_values,
        numeric_ranges=numeric_ranges,
    )
    if errors:
        return JsonOutput(JsonOutputStatus.SCHEMA_ERROR, value, errors, extracted)
    status = JsonOutputStatus.VALID_EXTRACTED_JSON if extracted else JsonOutputStatus.VALID_JSON
    note = ("extracted one balanced JSON object from surrounding text",) if extracted else ()
    return JsonOutput(status, value, note, extracted)


def validate_object(
    value: dict[str, Any],
    *,
    required_fields: tuple[str, ...] = (),
    allowed_values: dict[str, set[str] | tuple[str, ...] | list[str]] | None = None,
    numeric_ranges: dict[str, tuple[float, float]] | None = None,
) -> tuple[str, ...]:
    errors: list[str] = []
    for name in required_fields:
        if name not in value:
            errors.append(f"missing required field: {name}")
    for name, allowed in (allowed_values or {}).items():
        if name in value and value[name] not in allowed:
            errors.append(f"field {name!r} has disallowed value: {value[name]!r}")
    for name, (minimum, maximum) in (numeric_ranges or {}).items():
        if name not in value:
            continue
        try:
            number = float(value[name])
        except (TypeError, ValueError):
            errors.append(f"field {name!r} is not numeric")
            continue
        if not minimum <= number <= maximum:
            errors.append(f"field {name!r} is outside [{minimum}, {maximum}]")
    return tuple(errors)


def extract_single_json_object(raw_text: str) -> str | None:
    objects: list[str] = []
    start: int | None = None
    depth = 0
    in_string = False
    escape = False
    for index, char in enumerate(raw_text):
        if start is None:
            if char == "{":
                start, depth, in_string, escape = index, 1, False, False
            continue
        if escape:
            escape = False
            continue
        if char == "\\" and in_string:
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                objects.append(raw_text[start : index + 1])
                start = None
    return objects[0] if len(objects) == 1 else None
