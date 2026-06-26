# 50k Manuscript Results Summary

Run ID: `production_milestones_cumulative_v1`
Milestone: `50k`
Target calls: 47,500

This generated summary is derived from the offline 50k exporter. It does not include raw prompt text or raw model-output text.

## Primary Endpoint Snapshot

| Endpoint | Bin | Mean | 95% CI |
|---|---|---:|---|
| agreement_surplus | low_consensus | 0.370931 | [0.361206, 0.381114] |
| agreement_surplus | diffuse | 0.435619 | [0.427337, 0.444341] |
| agreement_surplus | low_diffuse | 0.396810 | [0.389856, 0.404111] |
| agreement_surplus | high_consensus | 0.169409 | [0.145651, 0.194624] |
| distribution_agreement_gap | low_consensus | 0.232687 | [0.224387, 0.241341] |
| distribution_agreement_gap | diffuse | 0.226556 | [0.216740, 0.237164] |
| distribution_agreement_gap | low_diffuse | 0.230233 | [0.223606, 0.237057] |
| distribution_agreement_gap | high_consensus | 0.182842 | [0.169762, 0.196217] |
| sampling_compression | low_consensus | 1.264638 | [1.218425, 1.309054] |
| sampling_compression | diffuse | 1.507379 | [1.452200, 1.562768] |
| sampling_compression | low_diffuse | 1.361734 | [1.323687, 1.399195] |
| sampling_compression | high_consensus | 0.563708 | [0.495005, 0.633547] |

## Primary Contrast Snapshot

| Endpoint | Contrast | Difference | 95% CI |
|---|---|---:|---|
| agreement_surplus | low_consensus_minus_high_consensus | 0.201523 | [0.174835, 0.228568] |
| agreement_surplus | diffuse_minus_high_consensus | 0.266210 | [0.240295, 0.290503] |
| agreement_surplus | low_diffuse_minus_high_consensus | 0.227402 | [0.202947, 0.252748] |
| distribution_agreement_gap | low_consensus_minus_high_consensus | 0.049845 | [0.033774, 0.065329] |
| distribution_agreement_gap | diffuse_minus_high_consensus | 0.043713 | [0.027505, 0.060791] |
| distribution_agreement_gap | low_diffuse_minus_high_consensus | 0.047390 | [0.032586, 0.062121] |
| sampling_compression | low_consensus_minus_high_consensus | 0.700930 | [0.618287, 0.783543] |
| sampling_compression | diffuse_minus_high_consensus | 0.943671 | [0.857540, 1.032909] |
| sampling_compression | low_diffuse_minus_high_consensus | 0.798026 | [0.714619, 0.881852] |

## Validity Snapshot

| Status | N |
|---|---:|
| empty_response | 2 |
| invalid_json | 4 |
| probability_out_of_bounds | 52 |
| probability_sum_error | 10 |
| valid_extracted_json | 8642 |
| valid_strict_schema | 38790 |

| Flag | N |
|---|---:|
| malformed | 6 |
| off_schema_label | 0 |
| refusal | 0 |
| repair_attempted | 0 |
| repair_successful | 0 |

## Interpretation Notes

- Low-consensus and diffuse bins remain positive on agreement surplus, distribution-agreement gap, and sampling compression.
- High-consensus effects are smaller than low/diffuse effects for agreement surplus and sampling compression, matching the main theoretical expectation.
- Distribution-agreement gap is also positive in high-consensus items, so the manuscript should emphasize relative bin differences rather than implying the effect is absent in high-consensus items.
- Paraphrase matched-pair comparisons are available but limited by original/paraphrase overlap; use the paraphrase aggregate and CI tables as the main robustness evidence.
- The formal recognition/contamination audit was not run and should remain a limitation unless new API calls are later approved.
