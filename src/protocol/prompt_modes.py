from __future__ import annotations

from enum import StrEnum


class PromptMode(StrEnum):
    DISTRIBUTION = "distribution_mode"
    DESCRIPTIVE_VERDICT = "descriptive_verdict_mode"
    NORMATIVE_VERDICT = "normative_verdict_mode"
    SAMPLING = "sampling_mode"
    RECOGNITION_AUDIT = "recognition_audit"
    PARAPHRASE_GENERATION = "paraphrase_generation"
    PARAPHRASED_DISTRIBUTION = "paraphrased_distribution_mode"
    PARAPHRASED_DESCRIPTIVE_VERDICT = "paraphrased_descriptive_verdict_mode"

