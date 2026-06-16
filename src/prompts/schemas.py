from __future__ import annotations

from protocol.label_schema import LABELS
from protocol.prompt_modes import PromptMode


def label_enum_schema() -> dict:
    return {"type": "string", "enum": list(LABELS)}


def distribution_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["label_probabilities", "most_likely_label"],
        "properties": {
            "label_probabilities": {
                "type": "object",
                "additionalProperties": False,
                "required": list(LABELS),
                "properties": {label: {"type": "number", "minimum": 0, "maximum": 1} for label in LABELS},
            },
            "most_likely_label": label_enum_schema(),
        },
    }


def descriptive_verdict_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["chosen_label", "estimated_source_community_agreement"],
        "properties": {
            "chosen_label": label_enum_schema(),
            "estimated_source_community_agreement": {"type": "number", "minimum": 0, "maximum": 1},
        },
    }


def normative_verdict_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["chosen_label", "moral_certainty"],
        "properties": {
            "chosen_label": label_enum_schema(),
            "moral_certainty": {"type": "number", "minimum": 0, "maximum": 1},
        },
    }


def sampling_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["chosen_label"],
        "properties": {"chosen_label": label_enum_schema()},
    }


def recognition_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["recognition_status", "confidence"],
        "properties": {
            "recognition_status": {
                "type": "string",
                "enum": ["recognized_specific_item", "recognized_general_style", "not_recognized", "unsure"],
            },
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
    }


def paraphrase_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["paraphrased_situation"],
        "properties": {"paraphrased_situation": {"type": "string", "minLength": 20}},
    }


SCHEMAS_BY_MODE = {
    PromptMode.DISTRIBUTION: distribution_schema,
    PromptMode.PARAPHRASED_DISTRIBUTION: distribution_schema,
    PromptMode.DESCRIPTIVE_VERDICT: descriptive_verdict_schema,
    PromptMode.PARAPHRASED_DESCRIPTIVE_VERDICT: descriptive_verdict_schema,
    PromptMode.NORMATIVE_VERDICT: normative_verdict_schema,
    PromptMode.SAMPLING: sampling_schema,
    PromptMode.RECOGNITION_AUDIT: recognition_schema,
    PromptMode.PARAPHRASE_GENERATION: paraphrase_schema,
}

