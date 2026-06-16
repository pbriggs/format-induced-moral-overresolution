from __future__ import annotations

ROBUSTNESS_CHECKS: tuple[str, ...] = (
    "raw_unsmoothed_source_distributions",
    "laplace_smoothing_alpha_1",
    "higher_annotation_only_subset",
    "exclude_info_majority_items",
    "exclude_high_info_items",
    "posterior_draw_source_uncertainty",
    "precision_weight_by_annotation_count",
    "strict_schema_valid_only",
    "exclude_repaired_outputs",
    "exclude_recognized_specific_items",
    "original_vs_paraphrase",
)

