from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any

from parsing.validity_status import ValidityStatus
from protocol.label_schema import LABELS
from protocol.prompt_modes import PromptMode


@dataclass(frozen=True)
class ParsedOutput:
    status: ValidityStatus
    parsed_json: dict[str, Any] | None
    probability_sum: float | None = None
    normalized_probability_sum: bool = False
    errors: tuple[str, ...] = field(default_factory=tuple)
    extracted_json: bool = False


def parse_and_validate(
    raw_text: str,
    prompt_mode: PromptMode | str,
    probability_tolerance: tuple[float, float] = (0.99, 1.01),
) -> ParsedOutput:
    if raw_text is None or raw_text.strip() == "":
        return ParsedOutput(ValidityStatus.EMPTY_RESPONSE, None, errors=("empty response",))
    try:
        value = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        extracted = extract_single_json_object(raw_text)
        if extracted is None:
            return ParsedOutput(ValidityStatus.INVALID_JSON, None, errors=(str(exc),))
        try:
            value = json.loads(extracted)
        except json.JSONDecodeError as extracted_exc:
            return ParsedOutput(ValidityStatus.INVALID_JSON, None, errors=(str(exc), str(extracted_exc)))
        parsed = validate_object(value, prompt_mode, probability_tolerance)
        if parsed.status == ValidityStatus.VALID_STRICT_SCHEMA:
            return ParsedOutput(
                ValidityStatus.VALID_EXTRACTED_JSON,
                parsed.parsed_json,
                parsed.probability_sum,
                parsed.normalized_probability_sum,
                ("extracted one balanced JSON object from surrounding text",),
                extracted_json=True,
            )
        return ParsedOutput(
            parsed.status,
            parsed.parsed_json,
            parsed.probability_sum,
            parsed.normalized_probability_sum,
            parsed.errors,
            extracted_json=True,
        )
    if not isinstance(value, dict):
        return ParsedOutput(ValidityStatus.INVALID_JSON, None, errors=("top-level value is not an object",))
    return validate_object(value, prompt_mode, probability_tolerance)


def extract_single_json_object(raw_text: str) -> str | None:
    objects: list[str] = []
    start: int | None = None
    depth = 0
    in_string = False
    escape = False
    for index, char in enumerate(raw_text):
        if start is None:
            if char == "{":
                start = index
                depth = 1
                in_string = False
                escape = False
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
    if len(objects) != 1:
        return None
    return objects[0]


def validate_object(
    value: dict[str, Any],
    prompt_mode: PromptMode | str,
    probability_tolerance: tuple[float, float] = (0.99, 1.01),
) -> ParsedOutput:
    mode = PromptMode(prompt_mode)
    if mode in {PromptMode.DISTRIBUTION, PromptMode.PARAPHRASED_DISTRIBUTION}:
        return _validate_distribution(value, probability_tolerance)
    if mode in {PromptMode.DESCRIPTIVE_VERDICT, PromptMode.PARAPHRASED_DESCRIPTIVE_VERDICT}:
        return _validate_label_and_number(value, "estimated_source_community_agreement")
    if mode == PromptMode.NORMATIVE_VERDICT:
        return _validate_label_and_number(value, "moral_certainty")
    if mode == PromptMode.SAMPLING:
        return _validate_label_only(value)
    if mode == PromptMode.RECOGNITION_AUDIT:
        return _validate_recognition(value)
    if mode == PromptMode.PARAPHRASE_GENERATION:
        text = value.get("paraphrased_situation")
        if not isinstance(text, str) or len(text) < 20:
            return ParsedOutput(ValidityStatus.MISSING_REQUIRED_FIELD, value, errors=("invalid paraphrased_situation",))
        return ParsedOutput(ValidityStatus.VALID_STRICT_SCHEMA, value)
    raise ValueError(f"unsupported prompt mode {mode}")


def _validate_distribution(value: dict[str, Any], tolerance: tuple[float, float]) -> ParsedOutput:
    probs = value.get("label_probabilities")
    if not isinstance(probs, dict) or "most_likely_label" not in value:
        return ParsedOutput(ValidityStatus.MISSING_REQUIRED_FIELD, value)
    if value["most_likely_label"] not in LABELS or set(probs) != set(LABELS):
        return ParsedOutput(ValidityStatus.OFF_SCHEMA_LABEL, value)
    try:
        clean = {label: float(probs[label]) for label in LABELS}
    except (TypeError, ValueError):
        return ParsedOutput(ValidityStatus.PROBABILITY_OUT_OF_BOUNDS, value)
    if any(p < 0.0 or p > 1.0 for p in clean.values()):
        return ParsedOutput(ValidityStatus.PROBABILITY_OUT_OF_BOUNDS, value, probability_sum=sum(clean.values()))
    total = sum(clean.values())
    if tolerance[0] <= total <= tolerance[1]:
        normalized = abs(total - 1.0) > 1e-12
        if normalized:
            value = dict(value)
            value["label_probabilities"] = {label: clean[label] / total for label in LABELS}
        return ParsedOutput(ValidityStatus.VALID_STRICT_SCHEMA, value, total, normalized)
    return ParsedOutput(ValidityStatus.PROBABILITY_SUM_ERROR, value, probability_sum=total)


def _validate_label_and_number(value: dict[str, Any], field_name: str) -> ParsedOutput:
    if "chosen_label" not in value or field_name not in value:
        return ParsedOutput(ValidityStatus.MISSING_REQUIRED_FIELD, value)
    if value["chosen_label"] not in LABELS:
        return ParsedOutput(ValidityStatus.OFF_SCHEMA_LABEL, value)
    try:
        number = float(value[field_name])
    except (TypeError, ValueError):
        return ParsedOutput(ValidityStatus.PROBABILITY_OUT_OF_BOUNDS, value)
    if not 0.0 <= number <= 1.0:
        return ParsedOutput(ValidityStatus.PROBABILITY_OUT_OF_BOUNDS, value)
    return ParsedOutput(ValidityStatus.VALID_STRICT_SCHEMA, value)


def _validate_label_only(value: dict[str, Any]) -> ParsedOutput:
    if "chosen_label" not in value:
        return ParsedOutput(ValidityStatus.MISSING_REQUIRED_FIELD, value)
    if value["chosen_label"] not in LABELS:
        return ParsedOutput(ValidityStatus.OFF_SCHEMA_LABEL, value)
    return ParsedOutput(ValidityStatus.VALID_STRICT_SCHEMA, value)


def _validate_recognition(value: dict[str, Any]) -> ParsedOutput:
    allowed = {"recognized_specific_item", "recognized_general_style", "not_recognized", "unsure"}
    if "recognition_status" not in value or "confidence" not in value:
        return ParsedOutput(ValidityStatus.MISSING_REQUIRED_FIELD, value)
    if value["recognition_status"] not in allowed:
        return ParsedOutput(ValidityStatus.OFF_SCHEMA_LABEL, value)
    confidence = float(value["confidence"])
    if not 0.0 <= confidence <= 1.0:
        return ParsedOutput(ValidityStatus.PROBABILITY_OUT_OF_BOUNDS, value)
    return ParsedOutput(ValidityStatus.VALID_STRICT_SCHEMA, value)
