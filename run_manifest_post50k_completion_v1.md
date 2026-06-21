# Run Manifest Post-50k Completion v1

Date: 2026-06-21

This file records completion of the full reduced 50k milestone for `format-induced-moral-overresolution` under `RUN_ID=production_milestones_cumulative_v1`. It supplements the pre-3k freeze, Gemini-to-Grok amendment, pre-6k, pre-13k, pre-25k, pre-35k, and pre-50k freeze records.

## 0. Archive Identifiers

- OSF project: `https://osf.io/rwhax/`
- GitHub repository: `https://github.com/pbriggs/format-induced-moral-overresolution`
- Prior GitHub release/tag: `post-35k-pre50k-freeze-v1`
- New GitHub release/tag to create: `post-50k-completion-v1`
- New GitHub release URL to create: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-50k-completion-v1`
- New Zenodo DOI: `[fill after Zenodo mints DOI for post-50k completion release]`
- Git commit at completion review: `d40e7ab Update .gitignore`
- Author: Paul Briggs
- License: CC0 1.0 Universal, unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## 1. Final Model Roster

The 50k milestone used the amended frozen roster:

```text
gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2
```

| Slot | Provider / route | Model ID | Role |
|---:|---|---|---|
| 1 | OpenAI first-party Responses API | `gpt-5.5` | GPT-family frontier proprietary |
| 2 | xAI first-party Responses API | `grok-4.3` | xAI/Grok-family frontier proprietary replacement for Gemini slot |
| 3 | Anthropic first-party Messages API | `claude-sonnet-4-6` | Claude-family frontier proprietary |
| 4 | OpenRouter-compatible `LLAMA_*` route | `qwen/qwen3.7-max` | strong Qwen open/open-weight-derived comparison |
| 5 | OpenRouter-compatible `LLAMA_*` route | `deepseek/deepseek-v3.2` | strong non-Qwen open/open-weight-derived comparison |

## 2. 50k Execution Summary

The 50k milestone completed successfully.

Summary from `runs/production_milestones_cumulative_v1/execution_summary_50k.json` and `milestone_report_50k.json`:

- planned calls: `47500`
- attempted calls: `47500`
- completed successful / non-error calls: `47500`
- API errors: `0`
- terminal failures: `0`
- retry rate: `0.0`
- executor status: `passed`
- abort reason: empty
- invalid outputs in final executor pass: `24`
- overall validity rate: `0.9985684210526315`
- minimum model/mode validity rate: `0.969`
- malformed rate: `0.0001263157894736842`
- refusal rate: `0.0`
- off-schema rate: `0.0`
- validity gate: `proceed=true`
- milestone decision: `continue`

The planned 50k milestone is `47,500` target study calls by design:

| Component | Items | Calls |
|---|---:|---:|
| core cross-format | 2000 | 20000 |
| repeated sampling | 400 | 20000 |
| paraphrase audit | 250 | 2500 |
| normative certainty | 1000 | 5000 |
| **Total** |  | **47500** |

## 3. Primary Directional Signal

The 50k milestone remains directionally supportive of the format-induced moral over-resolution hypothesis.

Final decision metrics:

- low/diffuse agreement-surplus mean: `0.4021026677587397`
- high-consensus agreement-surplus mean: `0.17307508898016485`
- low/diffuse distribution-agreement gap mean: `0.23104389444273882`
- high-consensus distribution-agreement gap mean: `0.1840342857142857`
- positive surplus models: `5`
- positive distribution-gap models: `5`
- positive sampling-compression models: `5`

Interpretation: the main expected pattern is present in the final reduced design. Agreement surplus is substantially larger in low-consensus/diffuse items than in high-consensus items. Distribution-agreement gaps remain positive in contested bins and are not driven by a single model. Repeated-sampling compression is positive across all five models.

This manifest records milestone completion and does not substitute for the final confirmatory analysis notebook/report. Subsequent analysis should estimate confidence intervals, model-level heterogeneity, bin-level contrasts, and robustness checks using the frozen 50k target set.

## 4. Model-Level Directional Checks

Agreement surplus by model and bin:

| Bin | Model | Mean | N |
|---|---|---:|---:|
| diffuse | `claude-sonnet-4-6` | `0.38369525443916735` | 560 |
| diffuse | `deepseek/deepseek-v3.2` | `0.42800780240369246` | 560 |
| diffuse | `gpt-5.5` | `0.413714790718722` | 560 |
| diffuse | `grok-4.3` | `0.42088764338956963` | 560 |
| diffuse | `qwen/qwen3.7-max` | `0.522563580971087` | 560 |
| low_consensus | `claude-sonnet-4-6` | `0.35637000380440736` | 850 |
| low_consensus | `deepseek/deepseek-v3.2` | `0.3583001475935008` | 850 |
| low_consensus | `gpt-5.5` | `0.36373603638034274` | 850 |
| low_consensus | `grok-4.3` | `0.3291420336192361` | 849 |
| low_consensus | `qwen/qwen3.7-max` | `0.4446093842676715` | 850 |
| high_consensus | `claude-sonnet-4-6` | `0.2367454407836555` | 390 |
| high_consensus | `deepseek/deepseek-v3.2` | `0.16558244521702056` | 390 |
| high_consensus | `gpt-5.5` | `0.17615523508454256` | 390 |
| high_consensus | `grok-4.3` | `0.06447356459429887` | 390 |
| high_consensus | `qwen/qwen3.7-max` | `0.22241875922130677` | 390 |

Distribution-agreement gap by model and bin:

| Bin | Model | Mean | N |
|---|---|---:|---:|
| diffuse | `claude-sonnet-4-6` | `0.21991999999999998` | 500 |
| diffuse | `deepseek/deepseek-v3.2` | `0.26983999999999997` | 500 |
| diffuse | `gpt-5.5` | `0.214` | 500 |
| diffuse | `grok-4.3` | `0.21154` | 500 |
| diffuse | `qwen/qwen3.7-max` | `0.22335999999999998` | 500 |
| low_consensus | `claude-sonnet-4-6` | `0.2321762349799733` | 749 |
| low_consensus | `deepseek/deepseek-v3.2` | `0.27968` | 750 |
| low_consensus | `gpt-5.5` | `0.22871999999999998` | 750 |
| low_consensus | `grok-4.3` | `0.21601604278074865` | 748 |
| low_consensus | `qwen/qwen3.7-max` | `0.21518666666666664` | 750 |
| high_consensus | `claude-sonnet-4-6` | `0.22514285714285714` | 350 |
| high_consensus | `deepseek/deepseek-v3.2` | `0.23077142857142857` | 350 |
| high_consensus | `gpt-5.5` | `0.1512` | 350 |
| high_consensus | `grok-4.3` | `0.13977142857142857` | 350 |
| high_consensus | `qwen/qwen3.7-max` | `0.17328571428571427` | 350 |

## 5. Robustness And Audit Checks

Paraphrase / label-order audit:

- paraphrase outputs: `2500`
- valid paraphrase outputs: `2495`
- unique label orders: `120`
- status: `available`

Repeated sampling compression:

- positive sampling-compression models: `5`
- diffuse bin means range from `1.2756507545817537` to `1.690171391377205`
- low-consensus bin means range from `0.9200005602792165` to `1.4084156447609264`
- high-consensus bin means are smaller, ranging from `0.20427006179520318` to `0.7185345167515266`

These checks support the interpretation that repeated forced-choice sampling compresses contested community disagreement and that the effect is not a single-model artifact.

## 6. Final 50k Artifact Hashes

These artifacts should be uploaded to OSF under a 50k completion folder.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/milestone_report_50k.md` | `D9CCE51BC42E6A98777F968FB43398B8B2722C94584E7F62BED5F9D162C17442` | 15750 |
| `runs/production_milestones_cumulative_v1/milestone_report_50k.json` | `F88E05FACE365D31292A759FD63B94FDA8D0EFA421A1A2725F135D52A0E8EE95` | 23910 |
| `runs/production_milestones_cumulative_v1/execution_summary_50k.json` | `427EEE82BDDB0E68C260356F828637BAA0F1D6334E654E7A712A07B468E53884` | 2739 |
| `runs/production_milestones_cumulative_v1/run_summary_50k.json` | `270EC985F50E7E1D987CE4D51D653C4B1687811D57F7D6DF140566CBA0BC585B` | 1743 |
| `runs/production_milestones_cumulative_v1/selected_items_50k.jsonl` | `BE7503FC763BC4C6EE8081643F900A66A0C0953A03E23967A332811AFB0846FE` | 1240861 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_50k.jsonl` | `81E617DCD63DDF9074BB415B6E72F52260FDDE9A33E8C475C642686B513FE7BF` | 5130000 |
| `runs/production_milestones_cumulative_v1/pending_api_calls_50k.jsonl` | `3270BAED90A7E7502E5F8305A9FDAD41D378C1576F474E8F139701ED253E7E8E` | 43592155 |
| `runs/production_milestones_cumulative_v1/call_ledger_50k.csv` | `5C30C14ED42A7448EC3ECAC2D81B1B45B13B54AF35CC26E03DB9BA31C09100AB` | 187745147 |
| `runs/production_milestones_cumulative_v1/call_ledger_50k.jsonl` | `0547EACE34EB28152ACAF3D3CED8C92CC15179CFC00FFB61220899277C7337E1` | 271407957 |

The call ledgers include rendered prompts and raw model outputs. Upload/share according to OSF visibility settings, provider terms, privacy considerations, and institutional review requirements.

## 7. Code / Protocol File Hashes At Completion

| File | SHA256 | Bytes |
|---|---|---:|
| `run_manifest_pre50k_freeze_v1.md` | `86EA0668A5EB36D66513D359C6F72035572CC03833AB33A4E05FFC0209ED1D8F` | 14180 |
| `docs/BUG_FIX_LOG.md` | `26425B27E9A286AB408632B10D3FD8F02FBB8F93D294917C94E84C5D0F07FFAF` | 8703 |
| `execute_remaining_milestone_run.bat` | `AA7E565EB6E51B5AE4F6E38B88CD4C65FD28F5B3CC34973D449E4B05D25A64B2` | 3475 |
| `src/production/execute_milestone.py` | `0B9AC9BCB3114C5D0745F1EB8363697C8E017F24C52D4B941B82C3F2536293D9` | 24462 |
| `src/production/failure_policy.py` | `84B2A9AF7AD4A17CDC1A5C66C46182C2CA6FD3F02DBE01F5E2AA4DAFC2A3C64A` | 5572 |
| `src/production/materialize_paraphrases.py` | `F6FCC076F0D8DEB99B0561CAC5C06FDBC910315480DF7FC1D1B8E17616E6981C` | 9390 |
| `src/production/progress_status.py` | `11E698188B0E9780E2F92FE83FBEB3ED16037172B74710E3C20A4DC29D107495` | 8175 |
| `src/production/reporting.py` | `D8C2C6A2A4772DA7AC83FD92CB2057C95D60211C567ADC2CE3E33D3F369D50EF` | 28552 |
| `src/production/run_milestone.py` | `92FA75FC72C4A4147C850E8226E1D9A3AD7E2AE5D713C943B7EB2ED4BD1FC989` | 24632 |
| `src/protocol/call_milestones.py` | `022A85C44FD6DCD480D4D271FBC265C82A3031F054F1824E4471DD6BA1D0267E` | 14470 |
| `tests/test_core_pipeline.py` | `5BC6249AD567C681E0400022ED61BFD01ED4A43B46501E42B3333F39687E6DDF` | 48941 |

## 8. Suggested Release Notes

Suggested GitHub release:

- tag: `post-50k-completion-v1`
- title: `Post-50k completion v1`

Suggested release notes:

```text
Completed the amended full reduced 50k milestone for production_milestones_cumulative_v1.

Decision: 50k milestone passed and is ready for final analysis.

Key 50k checks:
- 47500/47500 target study calls complete
- 0 API errors and 0 terminal failures in the final report
- retry rate 0.0
- overall validity rate 0.9986
- minimum model/mode validity rate 0.9690
- malformed rate 0.000126; refusal rate 0.0; off-schema rate 0.0
- low/diffuse agreement surplus 0.4021 versus high-consensus agreement surplus 0.1731
- low/diffuse distribution-agreement gap 0.2310 versus high-consensus gap 0.1840
- positive gap, surplus, and sampling-compression signs in all five models
- paraphrase audit available: 2500 outputs, 2495 valid, 120 unique label orders

The final 50k post-run artifact hashes and completion summary are recorded in run_manifest_post50k_completion_v1.md.
```

## 9. OSF Upload Checklist

Recommended OSF folder: `milestones/50k_completion/`

- `run_manifest_post50k_completion_v1.md`
- `runs/production_milestones_cumulative_v1/milestone_report_50k.md`
- `runs/production_milestones_cumulative_v1/milestone_report_50k.json`
- `runs/production_milestones_cumulative_v1/execution_summary_50k.json`
- `runs/production_milestones_cumulative_v1/run_summary_50k.json`
- `runs/production_milestones_cumulative_v1/selected_items_50k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_50k.jsonl`
- `runs/production_milestones_cumulative_v1/pending_api_calls_50k.jsonl`
- `runs/production_milestones_cumulative_v1/call_ledger_50k.csv`
- `runs/production_milestones_cumulative_v1/call_ledger_50k.jsonl`

After creating the GitHub release and Zenodo DOI, update section 0 with the minted DOI before or immediately after OSF upload.

## 10. Next Analysis Step

The next phase should be a final analysis/export pass rather than additional provider execution. Recommended immediate outputs:

1. final confirmatory analysis table with bin-level contrasts and model-level estimates;
2. bootstrap confidence intervals for primary contrasts;
3. final figure set for agreement surplus, distribution-agreement gap, entropy tracking, repeated-sampling compression, and paraphrase robustness;
4. reproducible analysis notebook or script using the frozen 50k target IDs;
5. manuscript-oriented limitations note covering paraphrase condensation, dataset provenance, model-provider terms, and the Gemini-to-Grok amendment.
