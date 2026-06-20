# Run Manifest Pre-35k Freeze v1

Date: 2026-06-19

This file freezes the post-25k / pre-35k study state for `format-induced-moral-overresolution`. It supplements the pre-3k freeze, the Gemini-to-Grok amendment, the pre-6k freeze, the pre-13k freeze, and the pre-25k freeze. It should be uploaded to OSF before running the 35k milestone.

## 0. Archive Identifiers

- OSF project: `https://osf.io/rwhax/`
- Prior GitHub release/tag: `post-13k-pre25k-freeze-v1`
- Prior GitHub release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-13k-pre25k-freeze-v1`
- Prior Zenodo DOI: `[fill if minted for post-13k/pre-25k release]`
- New GitHub release/tag to create: `post-25k-pre35k-freeze-v1`
- New GitHub release URL to create: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-25k-pre35k-freeze-v1`
- New Zenodo DOI: `https://doi.org/10.5281/zenodo.20768498`
- Git commit at freeze: `[fill after committing this manifest and 25k/35k code updates]`
- Author: Paul Briggs
- License: CC0 1.0 Universal, unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## 1. Prior Protocol Records

This pre-35k freeze inherits from:

- `run_manifest_pre3k_freeze_v2.md`
- `run_manifest_amendment_2026-06-17_gemini_to_grok_v1.md`
- `run_manifest_pre6k_freeze_v1.md`
- `run_manifest_pre13k_freeze_v1.md`
- `run_manifest_pre25k_freeze_v1.md`
- `docs/BUG_FIX_LOG.md`
- `docs/STUDY_PROCESS.md`
- `runs/call_milestones_3_6_13_35k.md`

The amended model roster remains in force. Previously collected Gemini rows remain historical pre-amendment artifacts and are not relabeled.

## 2. Frozen Model Roster For 35k

Use exactly this `STUDY_MODEL_IDS` value for 35k:

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

## 3. 25k Milestone Decision

The 25k milestone completed under `RUN_ID=production_milestones_cumulative_v1`.

Summary from the cumulative `runs/production_milestones_cumulative_v1/milestone_report_25k.json`:

- planned: `24750`
- attempted: `24750`
- completed successful / non-error calls: `24750`
- API errors: `0`
- terminal failures: `0`
- retry rate: `0.0`
- overall validity rate: `0.9987070707070707`
- minimum model/mode validity rate: `0.968`
- low/diffuse distribution-agreement gap mean: `0.23102065174531256`
- high-consensus distribution-agreement gap mean: `0.18257692307692305`
- low/diffuse agreement-surplus mean: `0.4004025517167311`
- high-consensus agreement-surplus mean: `0.17253614715512358`
- positive gap models: `5`
- positive surplus models: `5`
- positive sampling-compression models: `5`
- paraphrase outputs: `1250`
- valid paraphrase outputs: `1245`
- unique label orders: `120`
- decision: `continue`

Interpretation: 25k is a lean journal-capable milestone. The directional pattern remains stable enough to justify the 35k bridge run, while the 35k milestone remains a stronger minimum-defensible sample before considering the full reduced 50k design.

## 4. 25k Final Artifact Hashes

These 25k artifacts should be uploaded to OSF under a 25k milestone outputs folder.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/milestone_report_25k.md` | `01FC9B81E50A884D8A3D144ADE4DAAE486A46B88E8B00C66B66A6AD35923594A` | 15141 |
| `runs/production_milestones_cumulative_v1/milestone_report_25k.json` | `D9842DB03AFB6C3284283E035489B257B9C075DE2024ED687BB2B8D4A1E65CFB` | 22110 |
| `runs/production_milestones_cumulative_v1/execution_summary_25k.json` | `E7D865574B9CFADAF65FE7447C5FD4A06E263AB084D40F0CB2C839EAEF8E0DDD` | 2711 |
| `runs/production_milestones_cumulative_v1/run_summary_25k.json` | `37904159F75A9D0CA4DE1A616811963C5176D7162A7FF8E9581EC28EE7F835D9` | 1717 |
| `runs/production_milestones_cumulative_v1/selected_items_25k.jsonl` | `07C119156D3C9F504A7831FEC70D27DDB474F382353E9B539B334DCCEE86E4D5` | 635725 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_25k.jsonl` | `611AB23490FCFE7DDB94F3F069BF2FBDD16ADAC193BC790D31C59F29715D520C` | 2673000 |
| `runs/production_milestones_cumulative_v1/call_ledger_25k.csv` | `81BD92AD62F7C07DD7F103C30553A535D3EDD710483BDB77CBAB0AC1054CB454` | 100135771 |
| `runs/production_milestones_cumulative_v1/call_ledger_25k.jsonl` | `BBC7F1C8F6244FFCE8826F21134B8C54E07609D02ACA14C87A42440189BCAED3` | 143737686 |

The call ledgers include rendered prompts and raw model outputs. Upload/share according to OSF visibility settings, provider terms, privacy considerations, and institutional review requirements.

## 5. 35k Planned-Call Freeze

The 35k target list was planned before provider execution with:

```powershell
$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
.\start_milestone_run.bat 35k
```

Planning summary:

- `RUN_ID`: `production_milestones_cumulative_v1`
- milestone: `35k`
- planned calls for milestone: `35000`
- completed non-error calls carried forward into the 35k target: `23750`
- pending calls before 35k execution: `11250`
- provider-executable pending calls before paraphrase materialization: `10500`
- blocked prework calls before paraphrase materialization: `750`
- newly inserted planned calls: `11250`
- earlier planned calls outside current target: `1600`

The `1600` earlier planned calls outside the current 35k target include superseded pre-amendment/historical rows and 25k-only reserve/pilot-buffer rows that are not part of the 35k target definition. The 25k milestone completed `24750` calls, but the 35k target carries forward `23750` calls because the 25k pilot-buffer component is not included in the 35k milestone target. Current progress and reporting should be scoped to `target_api_call_ids_35k.jsonl`.

35k component allocation:

| Component | Items |
|---|---:|
| core cross-format | 1500 |
| repeated sampling | 300 |
| paraphrase audit | 200 |
| normative certainty | 500 |
| label-order reserve | 50 |

Bin allocation:

| Component | high consensus | moderate consensus | low consensus | diffuse |
|---|---:|---:|---:|---:|
| core cross-format | 250 | 300 | 550 | 400 |
| repeated sampling | 50 | 60 | 110 | 80 |
| paraphrase audit | 30 | 40 | 80 | 50 |
| normative certainty | 80 | 100 | 190 | 130 |
| label-order reserve | 4 | 15 | 14 | 17 |

The 35k target includes `750` paraphrase-audit calls whose prompt material depends on newly materialized paraphrases. Run the paraphrase materialization command before executing the full 35k milestone.

## 6. 35k Pre-Materialization Planning Artifact Hashes

These hashes freeze the 35k target list and planning outputs before paraphrase materialization. Files that contain rendered paraphrase prompts, ledgers, or execution reports are expected to change after `materialize_paraphrases.bat 35k` and provider execution.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/run_summary_35k.json` | `2943A9173D0A6A4C068CEC91EE372AADE56C477CBF035FDEB8360C7B929F2756` | 2360 |
| `runs/production_milestones_cumulative_v1/pending_api_calls_35k.jsonl` | `45390DD3F518BFCAB292A3AD9F8DE395460C626A640E7DA76696EA48AC26115B` | 36522040 |
| `runs/production_milestones_cumulative_v1/selected_items_35k.jsonl` | `9A74A143B95022AF60077CFBC1523C46164DB31A09DCDDE8A2B1B491ACC434B2` | 866318 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_35k.jsonl` | `32D04DE3462166907C1ED098874700A91B024CF66C2BC577E6AF2A09E89FCAC4` | 3780000 |
| `runs/production_milestones_cumulative_v1/call_ledger_35k.csv` | `21A2E49D80D1CE5CD25AB18CDDD4E1710A36CFA2C54E20A77E004CC106868F1E` | 108377231 |
| `runs/production_milestones_cumulative_v1/call_ledger_35k.jsonl` | `C21A6F34F0F67D84DF73F94855454EE1D060C9DF7D1CD4C7F3B6AAFBDCFE336C` | 170357579 |
| `runs/production_milestones_cumulative_v1/milestone_report_35k.md` | `84FDECAB8DBA54FC443FBC2B0D715F7ABC09E4729E57B28947B18D7493196EC8` | 15175 |
| `runs/production_milestones_cumulative_v1/milestone_report_35k.json` | `E63A34811F8186D8BE34B6E6932462DAD065901884D33B8581FD7ACF99A8547F` | 22211 |

## 7. Code / Protocol File Hashes At Freeze

| File | SHA256 | Bytes |
|---|---|---:|
| `docs/BUG_FIX_LOG.md` | `849067410E4FCA51C63C7A8E3631F07E7E3428C2FB43B8FB849E03DD01A27CBD` | 8683 |
| `execute_remaining_milestone_run.bat` | `384718B333DCD526C1A6D88952DE3280EB3F69FF48442374352A4AF4CAFDF654` | 3388 |
| `src/production/execute_milestone.py` | `8EA406A987B073BA485750AD40A00030F2EEA82C3DC5F0B6F377DED028ABA63B` | 23876 |
| `src/production/failure_policy.py` | `84B2A9AF7AD4A17CDC1A5C66C46182C2CA6FD3F02DBE01F5E2AA4DAFC2A3C64A` | 5572 |
| `src/production/progress_status.py` | `11E698188B0E9780E2F92FE83FBEB3ED16037172B74710E3C20A4DC29D107495` | 8175 |
| `src/production/reporting.py` | `D8C2C6A2A4772DA7AC83FD92CB2057C95D60211C567ADC2CE3E33D3F369D50EF` | 28552 |
| `src/production/run_milestone.py` | `92FA75FC72C4A4147C850E8226E1D9A3AD7E2AE5D713C943B7EB2ED4BD1FC989` | 24632 |
| `tests/test_core_pipeline.py` | `5BC6249AD567C681E0400022ED61BFD01ED4A43B46501E42B3333F39687E6DDF` | 48941 |

Post-25k operational fixes include:

- classifying OpenRouter `403 Key limit exceeded` as retryable account/key-limit errors rather than terminal authorization failures;
- adding visible phase/call heartbeats during execution;
- skipping expensive full-report/ledger exports during internal executor resume planning;
- preserving completed invalid/non-error outputs as completed calls for resume semantics.

## 8. Execution Commands For 35k

After this manifest is uploaded to OSF, first materialize the remaining 35k paraphrase prework:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
$env:PARAPHRASE_HELPER_MODEL_ID='grok-4.3'
Remove-Item Env:\PARAPHRASE_MAX_ITEMS -ErrorAction SilentlyContinue

.\materialize_paraphrases.bat 35k
```

Then execute the remaining provider calls:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:SHARD_COUNT='1'
Remove-Item Env:\SKIP_MODEL_IDS -ErrorAction SilentlyContinue

$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'

.\execute_remaining_milestone_run.bat 35k
```

Expected additional provider calls before 35k completion:

- paraphrase helper prework: up to `75` xAI helper calls
- study calls: `11250`

## 9. Release Notes For GitHub

Suggested release:

- tag: `post-25k-pre35k-freeze-v1`
- title: `Post-25k milestone and pre-35k freeze v1`

Suggested release notes:

```text
Completed the amended 25k milestone for production_milestones_cumulative_v1.

Decision: continue to 35k.

Key 25k checks:
- 24750/24750 target calls complete
- 0 API errors and 0 terminal failures in the final report
- overall validity rate 0.9987
- minimum model/mode validity rate 0.968
- low/diffuse agreement surplus 0.4004 versus high-consensus agreement surplus 0.1725
- low/diffuse distribution-agreement gap 0.2310 versus high-consensus gap 0.1826
- positive gap, surplus, and sampling-compression signs in all five models
- paraphrase audit available: 1250 outputs, 1245 valid

This release also includes post-25k operational fixes:
- OpenRouter key-limit 403 responses are classified as retryable account-limit errors
- executor heartbeat now reports planning, execution start, per-call start, completion, and export phases
- internal executor planning skips expensive ledger/report exports so resumed runs reach provider calls quickly

The 35k target list and pre-materialization planning artifacts are frozen in run_manifest_pre35k_freeze_v1.md.
```

## 10. OSF Upload Checklist

Upload this manifest and the following run artifacts to OSF. Because `runs/` is gitignored, these artifacts are not expected to appear in the GitHub release.

Recommended OSF folder: `milestones/25k_post_and_35k_pre_freeze/`

- `run_manifest_pre35k_freeze_v1.md`
- `runs/production_milestones_cumulative_v1/milestone_report_25k.md`
- `runs/production_milestones_cumulative_v1/milestone_report_25k.json`
- `runs/production_milestones_cumulative_v1/execution_summary_25k.json`
- `runs/production_milestones_cumulative_v1/run_summary_25k.json`
- `runs/production_milestones_cumulative_v1/selected_items_25k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_25k.jsonl`
- `runs/production_milestones_cumulative_v1/call_ledger_25k.csv`
- `runs/production_milestones_cumulative_v1/call_ledger_25k.jsonl`
- `runs/production_milestones_cumulative_v1/run_summary_35k.json`
- `runs/production_milestones_cumulative_v1/selected_items_35k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_35k.jsonl`
- `runs/production_milestones_cumulative_v1/pending_api_calls_35k.jsonl`

After creating the GitHub release and Zenodo archive, update OSF with the GitHub release URL and Zenodo DOI. If OSF has no dedicated DOI field, add them to the project wiki/description or upload a small note file beside this manifest.

## 11. Next Decision Point

The 35k milestone is the minimum-defensible bridge between the lean 25k run and the full reduced 50k run. Continue beyond 35k only if:

- provider/API stability remains acceptable;
- validity remains above protocol thresholds;
- low-consensus/diffuse effects remain larger than high-consensus effects;
- repeated-sampling compression remains positive in most models;
- paraphrase/audit results preserve the direction of the main effect;
- normative-certainty results remain secondary and do not confuse the core descriptive agreement interpretation;
- the result is not driven by a single model or provider family.
