# Quantitative Figure Polish Preflight, 50k

## Current Style Inconsistencies

- Main endpoint figures share the same data grammar, but titles are relatively large, legends occupy the plotting area, and model markers use default-bright colors that compete with aggregate bars.
- Support figures use the same visual weight as main figures, so diagnostics and paraphrase checks do not feel subordinate.
- Gridlines and spines are serviceable but can be lighter and more consistent across the figure family.
- The validity figure uses near-ceiling bars on a truncated y-axis, which can exaggerate very small differences in valid-primary rates.
- Fig. 1 is now visually restrained and compatible enough; no Fig. 1 changes are proposed in this pass.

## Figures Requiring Polish Only

- `figure_agreement_surplus_by_bin_model_50k`
- `figure_distribution_gap_by_bin_model_50k`
- `figure_sampling_compression_by_bin_model_50k`
- `figure_distribution_quality_distances_50k`
- `figure_paraphrase_audit_effects_50k`

## Figure Requiring Modest Display Redesign

- `figure_validity_rate_by_model_50k`: convert from truncated bar chart to a restrained dot/lollipop-style transparency figure using the same model-level mean validity rates. This is a display-format polish change only; it does not change the data, model roster, or interpretation.

## Proposed Changes

- Introduce shared quantitative style helpers for sans-serif typography, muted palette, light horizontal gridlines, minimal spines, compact legends, and consistent export behavior.
- Coordinate Figs. 2-4 with the same size, title/axis/tick sizes, aggregate bar color, CI styling, model color/marker mapping, and legend placement above the plotting area.
- Keep aggregate all-model bars and existing aggregate CIs in Figs. 2-4; keep model-level points without model-level CIs.
- Make diagnostics and paraphrase audit quieter through smaller titles, muted colors, compact legends, and restrained line/bar weights.
- Redesign validity as a dot/lollipop display with exact percent labels, preserving the same averaged validity rates derived from the existing CSV.

## Interpretation Risk

- No proposed change affects numerical values, endpoint definitions, bin order, model roster, or scientific claims.
- The validity display redesign reduces a visual exaggeration risk from the previous truncated bar chart.
