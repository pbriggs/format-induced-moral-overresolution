# Run Manifest Pre-25k Freeze v1

Date: 2026-06-18

This file freezes the post-13k / pre-25k study state for `format-induced-moral-overresolution`. It supplements the pre-3k freeze, the Gemini-to-Grok amendment, the pre-6k freeze, and the pre-13k freeze. It should be uploaded to OSF before running the 25k milestone.

## 0. Archive Identifiers

- OSF project: `https://osf.io/rwhax/`
- Prior GitHub release/tag: `post-6k-pre13k-freeze-v1`
- Prior GitHub release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-6k-pre13k-freeze-v1`
- New GitHub release/tag to create: `post-13k-pre25k-freeze-v1`
- New GitHub release URL to create: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-13k-pre25k-freeze-v1`
- New Zenodo DOI: `https://doi.org/10.5281/zenodo.20753877`
- Git commit at freeze: `SHA 6ce0a365fdb4fcd839433e340bf914b2fa50e995`
- Author: Paul Briggs
- License: CC0 1.0 Universal, unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## 1. Prior Protocol Records

This pre-25k freeze inherits from:

- `run_manifest_pre3k_freeze_v2.md`
- `run_manifest_amendment_2026-06-17_gemini_to_grok_v1.md`
- `run_manifest_pre6k_freeze_v1.md`
- `run_manifest_pre13k_freeze_v1.md`
- `docs/BUG_FIX_LOG.md`
- `docs/STUDY_PROCESS.md`
- `runs/call_milestones_3_6_13_35k.md`

The amended model roster remains in force. Previously collected Gemini rows remain historical pre-amendment artifacts and are not relabeled.

## 2. Frozen Model Roster For 25k

Use exactly this `STUDY_MODEL_IDS` value for 25k:

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

## 3. 13k Milestone Decision

The 13k milestone completed under `RUN_ID=production_milestones_cumulative_v1`.

Summary from the cumulative `runs/production_milestones_cumulative_v1/milestone_report_13k.json`:

- planned: `13000`
- attempted: `13000`
- completed successful / non-error calls: `13000`
- API errors: `0`
- terminal failures: `0`
- retry rate: `0.0`
- overall validity rate: `0.9986153846153846`
- minimum model/mode validity rate: `0.96`
- low/diffuse distribution-agreement gap mean: `0.23699616407299598`
- high-consensus distribution-agreement gap mean: `0.17104999999999998`
- low/diffuse agreement-surplus mean: `0.4001053958721217`
- high-consensus agreement-surplus mean: `0.1586096865110363`
- positive gap models: `5`
- positive surplus models: `5`
- positive sampling-compression models: `5`
- paraphrase outputs: `1000`
- valid paraphrase outputs: `996`
- unique label orders: `120`
- decision: `continue`

Interpretation: 13k is a serious pre-confirmatory diagnostic milestone. The directional pattern is strong enough to justify the 25k lean journal-capable run, while remaining short of a final confirmatory claim.

## 4. 13k Final Artifact Hashes

These 13k artifacts should be uploaded to OSF under a 13k milestone outputs folder.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/milestone_report_13k.md` | `1FA453D76FD7210DE1019044A9CA9891A836342CDB8D76213C846531D65F53F1` | 15063 |
| `runs/production_milestones_cumulative_v1/milestone_report_13k.json` | `31BD808CCCDC0EFBA63A0E46CB124B5F974970050CC2339FDF4F50A4C3CEEEBA` | 21996 |
| `runs/production_milestones_cumulative_v1/execution_summary_13k.json` | `3665D0B47E21DBBC9EFB655B35B8780542D2B43B92A4172FF9DBB3C7C0BA7E31` | 2979 |
| `runs/production_milestones_cumulative_v1/run_summary_13k.json` | `2E94770CA38A4B91C22790FDF6425D3DFCE7AA255E4C495C7AE9C6B7ACFCA098` | 1982 |
| `runs/production_milestones_cumulative_v1/selected_items_13k.jsonl` | `4424276596534735FC270FFBDEEEA22FEF170788E10F5D3E3ED379E84EE488A5` | 339162 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_13k.jsonl` | `E5BAF36D2A5A2024DA8619AB22184D08798C983B7EB1F7DEB9DBAC03F04AA5E5` | 1404000 |
| `runs/production_milestones_cumulative_v1/call_ledger_13k.csv` | `91E5FE1B6AF096794AF59E6B464405A28A60F40A1100C584BAD95304C28C277D` | 52056087 |
| `runs/production_milestones_cumulative_v1/call_ledger_13k.jsonl` | `25F772E1A6F7451F5AFB813AA3C1B6420261A9E5BD4593B638B555F52FDFF2FE` | 74947133 |

The call ledgers include rendered prompts and raw model outputs. Upload/share according to OSF visibility settings, provider terms, privacy considerations, and institutional review requirements.

## 5. 25k Planned-Call Freeze

The 25k target list was planned before provider execution with:

```powershell
$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
.\start_milestone_run.bat 25k
```

Planning summary:

- `RUN_ID`: `production_milestones_cumulative_v1`
- milestone: `25k`
- planned calls for milestone: `24750`
- completed non-error calls carried forward from 13k: `13000`
- pending calls before 25k execution: `11750`
- provider-executable pending calls before paraphrase materialization: `11500`
- blocked prework calls before paraphrase materialization: `250`
- newly inserted planned calls: `0` in the final idempotent planning pass
- earlier planned calls outside current target: `600`

The `600` earlier planned calls outside the current 25k target are superseded pre-amendment/historical rows in the same run database. Current progress and reporting should be scoped to `target_api_call_ids_25k.jsonl`.

25k component allocation:

| Component | Items |
|---|---:|
| core cross-format | 1500 |
| repeated sampling | 150 |
| paraphrase audit | 125 |
| pilot buffer | 100 |

Bin allocation:

| Component | high consensus | moderate consensus | low consensus | diffuse |
|---|---:|---:|---:|---:|
| core cross-format | 250 | 300 | 550 | 400 |
| repeated sampling | 25 | 30 | 55 | 40 |
| paraphrase audit | 20 | 25 | 50 | 30 |
| pilot buffer | 8 | 28 | 25 | 39 |

The 25k target includes `250` paraphrase-audit calls whose prompt material depends on newly materialized paraphrases. Run the paraphrase materialization command before executing the full 25k milestone.

## 6. 25k Pre-Materialization Planning Artifact Hashes

These hashes freeze the 25k target list and planning outputs before paraphrase materialization. Files that contain rendered paraphrase prompts, ledgers, or execution reports are expected to change after `materialize_paraphrases.bat 25k` and provider execution.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/run_summary_25k.json` | `2BC07995A3E32553C91AF26A5772E44E6C094830E5F200D68D44C83EF515CBD6` | 2156 |
| `runs/production_milestones_cumulative_v1/pending_api_calls_25k.jsonl` | `45EB019EE350AD70B4D0ECC1DE1B2C8A9AD8C9B1DF0AB133619F1152C5DEAE3B` | 40704710 |
| `runs/production_milestones_cumulative_v1/selected_items_25k.jsonl` | `07C119156D3C9F504A7831FEC70D27DDB474F382353E9B539B334DCCEE86E4D5` | 635725 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_25k.jsonl` | `611AB23490FCFE7DDB94F3F069BF2FBDD16ADAC193BC790D31C59F29715D520C` | 2673000 |
| `runs/production_milestones_cumulative_v1/call_ledger_25k.csv` | `F0408DEFF3506BEFCBFAE7ADB8AE4FBB46CF06E0A3657F7CA0D49C4E08C14905` | 65140812 |
| `runs/production_milestones_cumulative_v1/call_ledger_25k.jsonl` | `F85C2B8BB7CEE4B1B0E43F38CCCDC4F90C49185B0B61AC0D4705E42C40477A59` | 109085608 |
| `runs/production_milestones_cumulative_v1/milestone_report_25k.md` | `F9ACDE3EA8668943501428874BF645276C2CE944E012A743DD25BCB20A994752` | 15146 |
| `runs/production_milestones_cumulative_v1/milestone_report_25k.json` | `75E29FFF1BCC3CABA448E56FB46CE2FE3A3D5115775E616409CD0CFE9C377B1F` | 22063 |

## 7. Code / Protocol File Hashes At Freeze

| File | SHA256 | Bytes |
|---|---|---:|
| `docs/BUG_FIX_LOG.md` | `C6F1E5ACE4D8DC6B823DABAD0A586BE9355B95B87B68464CAC60DCDE0E38EDE2` | 7864 |
| `execute_remaining_milestone_run.bat` | `384718B333DCD526C1A6D88952DE3280EB3F69FF48442374352A4AF4CAFDF654` | 3388 |
| `src/production/providers.py` | `9D282521CEC7C67DC9F4CD00B815ACAD5ED58ECCB3C907480D4CC00E1981FEFD` | 13747 |
| `src/production/progress_status.py` | `11E698188B0E9780E2F92FE83FBEB3ED16037172B74710E3C20A4DC29D107495` | 8175 |
| `src/production/reporting.py` | `D8C2C6A2A4772DA7AC83FD92CB2057C95D60211C567ADC2CE3E33D3F369D50EF` | 28552 |
| `src/production/run_milestone.py` | `87CB8B3E5E89802F38DA9D6EA08D2DE6CED99C4F5D8B17D70526ECC3145B085C` | 24399 |
| `tests/test_core_pipeline.py` | `65469E939A8862ABB000D0597A703675DFB99FED0CBA47151E16DAC0A93567AA` | 48155 |

Post-13k operational fixes include:

- retrying `http.client.IncompleteRead` / chunked-transfer failures as transport errors;
- distinguishing completed executable shards from remaining prework-blocked calls;
- counting non-error empty HTTP 200 model responses as completed invalid outputs for completion/replanning gates;
- using temp-table target filters for large milestone reports and ledgers to avoid SQLite variable limits.

## 8. Execution Commands For 25k

After this manifest is uploaded to OSF, first materialize the remaining 25k paraphrase prework:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
$env:PARAPHRASE_HELPER_MODEL_ID='grok-4.3'
Remove-Item Env:\PARAPHRASE_MAX_ITEMS -ErrorAction SilentlyContinue

.\materialize_paraphrases.bat 25k
```

Then execute the remaining provider calls:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:SHARD_COUNT='20'
Remove-Item Env:\SKIP_MODEL_IDS -ErrorAction SilentlyContinue

$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'

.\execute_remaining_milestone_run.bat 25k
```

Expected additional provider calls before 25k completion:

- paraphrase helper prework: up to `25` xAI helper calls
- study calls: `11750`

## 9. Release Notes For GitHub

Suggested release:

- tag: `post-13k-pre25k-freeze-v1`
- title: `Post-13k milestone and pre-25k freeze v1`

Suggested release notes:

```text
Completed the amended 13k milestone for production_milestones_cumulative_v1.

Decision: continue to 25k.

Key 13k checks:
- 13000/13000 target calls complete
- 0 API errors and 0 terminal failures
- overall validity rate 0.9986
- minimum model/mode validity rate 0.96
- low/diffuse agreement surplus 0.4001 versus high-consensus agreement surplus 0.1586
- low/diffuse distribution-agreement gap 0.2370 versus high-consensus gap 0.1710
- positive gap, surplus, and sampling-compression signs in all five models
- paraphrase audit available: 1000 outputs, 996 valid

This release also includes post-13k operational/reporting fixes:
- retry chunked-transfer IncompleteRead transport failures
- distinguish prework-blocked calls from completed executable shards
- count non-error empty HTTP 200 model responses as completed invalid outputs for completion gates
- support large target-ID report/ledger generation via SQLite temp target tables

The 25k target list and pre-materialization planning artifacts are frozen in run_manifest_pre25k_freeze_v1.md.
```

## 10. OSF Upload Checklist

Upload this manifest and the following run artifacts to OSF. Because `runs/` is gitignored, these artifacts are not expected to appear in the GitHub release.

Recommended OSF folder: `milestones/13k_post_and_25k_pre_freeze/`

- `run_manifest_pre25k_freeze_v1.md`
- `runs/production_milestones_cumulative_v1/milestone_report_13k.md`
- `runs/production_milestones_cumulative_v1/milestone_report_13k.json`
- `runs/production_milestones_cumulative_v1/execution_summary_13k.json`
- `runs/production_milestones_cumulative_v1/run_summary_13k.json`
- `runs/production_milestones_cumulative_v1/selected_items_13k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_13k.jsonl`
- `runs/production_milestones_cumulative_v1/call_ledger_13k.csv`
- `runs/production_milestones_cumulative_v1/call_ledger_13k.jsonl`
- `runs/production_milestones_cumulative_v1/run_summary_25k.json`
- `runs/production_milestones_cumulative_v1/selected_items_25k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_25k.jsonl`
- `runs/production_milestones_cumulative_v1/pending_api_calls_25k.jsonl`

After creating the GitHub release and Zenodo archive, update OSF with the GitHub release URL and Zenodo DOI. If OSF has no dedicated DOI field, add them to the project wiki/description or upload a small note file beside this manifest.

## 11. Next Decision Point

The 25k milestone is the lean journal-capable sample. Continue beyond 25k only if:

- provider/API stability remains acceptable;
- validity remains above protocol thresholds;
- low-consensus/diffuse effects remain larger than high-consensus effects;
- repeated-sampling compression remains positive in most models;
- paraphrase/audit results preserve the direction of the main effect;
- the result is not driven by a single model or provider family.
