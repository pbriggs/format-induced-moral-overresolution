# Run Manifest Pre-50k Freeze v1

Date: 2026-06-20

This file freezes the post-35k / pre-50k study state for `format-induced-moral-overresolution`. It supplements the pre-3k freeze, the Gemini-to-Grok amendment, the pre-6k freeze, the pre-13k freeze, the pre-25k freeze, and the pre-35k freeze. It should be uploaded to OSF before running the 50k milestone.

## 0. Archive Identifiers

- OSF project: `https://osf.io/rwhax/`
- Prior GitHub release/tag: `post-25k-pre35k-freeze-v1`
- Prior GitHub release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-25k-pre35k-freeze-v1`
- New GitHub release/tag to create: `post-35k-pre50k-freeze-v1`
- New GitHub release URL to create: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-35k-pre50k-freeze-v1`
- New Zenodo DOI: `https://doi.org/10.5281/zenodo.20777786`
- Git commit at freeze: `1297235 Update run_manifest_pre35k_freeze_v1.md`
- Author: Paul Briggs
- License: CC0 1.0 Universal, unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## 1. Prior Protocol Records

This pre-50k freeze inherits from:

- `run_manifest_pre3k_freeze_v2.md`
- `run_manifest_amendment_2026-06-17_gemini_to_grok_v1.md`
- `run_manifest_pre6k_freeze_v1.md`
- `run_manifest_pre13k_freeze_v1.md`
- `run_manifest_pre25k_freeze_v1.md`
- `run_manifest_pre35k_freeze_v1.md`
- `docs/BUG_FIX_LOG.md`
- `docs/STUDY_PROCESS.md`
- `runs/call_milestones_3_6_13_35k.md`

The amended model roster remains in force. Previously collected Gemini rows remain historical pre-amendment artifacts and are not relabeled.

## 2. Frozen Model Roster For 50k

Use exactly this `STUDY_MODEL_IDS` value for 50k:

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

## 3. 35k Milestone Decision

The 35k milestone completed under `RUN_ID=production_milestones_cumulative_v1`.

Summary from `runs/production_milestones_cumulative_v1/milestone_report_35k.json`:

- target calls complete: `35000/35000`
- API errors: `0`
- terminal failures: `0`
- overall validity rate: `0.9987142857142857`
- minimum model/mode validity rate: `0.97`
- low/diffuse distribution-agreement gap mean: `0.23200109709787506`
- high-consensus distribution-agreement gap mean: `0.1831259842519685`
- low/diffuse agreement-surplus mean: `0.39894909079933144`
- high-consensus agreement-surplus mean: `0.17114071791649715`
- positive gap models: `5`
- positive surplus models: `5`
- positive sampling-compression models: `5`
- decision: `continue`

Interpretation: the 35k bridge milestone remains strongly directionally supportive and satisfies the continuation criteria for the full reduced 50k milestone. The 50k run is the preferred first-paper design and strengthens item coverage, repeated sampling, paraphrase audit coverage, and the secondary normative-certainty endpoint.

## 4. 35k Final Artifact Hashes

These 35k artifacts should be uploaded to OSF under a 35k milestone outputs folder.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/milestone_report_35k.md` | `01DDA6E7ED6D98E775E069159B1418FF7ACEFC297E2014C8E889E787C551E703` | 15842 |
| `runs/production_milestones_cumulative_v1/milestone_report_35k.json` | `A2C53019F047B7A1ACA1FD43D3D771093364E4EA6137C1EA699C7E44BE6837CE` | 24097 |
| `runs/production_milestones_cumulative_v1/execution_summary_35k.json` | `D070A36BDCAD032BC3920BF7694A9C1441DFFA6578EC1810C3E3166EA5C56941` | 2929 |
| `runs/production_milestones_cumulative_v1/run_summary_35k.json` | `E9859FA84DD0C098F361C34A23CF81D097A6DE849AE65273A7DD108E1D3606F0` | 1919 |
| `runs/production_milestones_cumulative_v1/selected_items_35k.jsonl` | `9A74A143B95022AF60077CFBC1523C46164DB31A09DCDDE8A2B1B491ACC434B2` | 866318 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_35k.jsonl` | `32D04DE3462166907C1ED098874700A91B024CF66C2BC577E6AF2A09E89FCAC4` | 3780000 |
| `runs/production_milestones_cumulative_v1/call_ledger_35k.csv` | `43050316C5D6F0435CD9932AB74C6DF56FAEB92EDBE28E05E2A19AE2A7A76F56` | 138108414 |
| `runs/production_milestones_cumulative_v1/call_ledger_35k.jsonl` | `7730803F6C2BEA3CB6E165E639D5899028E832A8FE753D93F573F9776FB4E18E` | 199755610 |

The call ledgers include rendered prompts and raw model outputs. Upload/share according to OSF visibility settings, provider terms, privacy considerations, and institutional review requirements.

## 5. 50k Planned-Call Freeze

The 50k target list was planned before provider execution with:

```powershell
$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
.\start_milestone_run.bat 50k
```

Planning summary:

- `RUN_ID`: `production_milestones_cumulative_v1`
- milestone: `50k`
- planned calls for milestone: `47500`
- completed non-error calls carried forward into the 50k target: `34500`
- pending calls before 50k execution: `13000`
- provider-executable pending calls before paraphrase materialization: `12500`
- blocked prework calls before paraphrase materialization: `500`
- newly inserted planned calls: `13000`
- earlier planned calls outside current target: `2100`

The `2100` earlier planned calls outside the current 50k target include superseded pre-amendment/historical rows and earlier reserve rows that are not part of the 50k target definition. Current progress and reporting should be scoped to `target_api_call_ids_50k.jsonl`.

50k component allocation:

| Component | Items | Calls |
|---|---:|---:|
| core cross-format | 2000 | 20000 |
| repeated sampling | 400 | 20000 |
| paraphrase audit | 250 | 2500 |
| normative certainty | 1000 | 5000 |
| **Total** |  | **47500** |

Bin allocation:

| Component | high consensus | moderate consensus | low consensus | diffuse |
|---|---:|---:|---:|---:|
| core cross-format | 350 | 400 | 750 | 500 |
| repeated sampling | 70 | 80 | 150 | 100 |
| paraphrase audit | 40 | 50 | 100 | 60 |
| normative certainty | 160 | 200 | 380 | 260 |

The 50k target includes `500` paraphrase-audit calls whose prompt material depends on newly materialized paraphrases. Run the paraphrase materialization command before executing the remaining 50k provider calls.

## 6. 50k Pre-Materialization Planning Artifact Hashes

These hashes freeze the 50k target list and planning outputs before paraphrase materialization. Files that contain rendered paraphrase prompts, ledgers, or execution reports are expected to change after `materialize_paraphrases.bat 50k` and provider execution.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/run_summary_50k.json` | `F171115184E693E20CBB478B320578E995FE13575E8DF77510B82B66925EB774` | 2184 |
| `runs/production_milestones_cumulative_v1/pending_api_calls_50k.jsonl` | `4C5C3E07C53F571C5D52FF8A6ED1BE7C14AF7BC089AA4016AEA7BAE70783828B` | 44056045 |
| `runs/production_milestones_cumulative_v1/selected_items_50k.jsonl` | `BE7503FC763BC4C6EE8081643F900A66A0C0953A03E23967A332811AFB0846FE` | 1240861 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_50k.jsonl` | `81E617DCD63DDF9074BB415B6E72F52260FDDE9A33E8C475C642686B513FE7BF` | 5130000 |
| `runs/production_milestones_cumulative_v1/call_ledger_50k.csv` | `520F1A78423E166C3DC88573A02244F6B2B25B3B14ABCFF8B70B3724BF0C043C` | 150546364 |
| `runs/production_milestones_cumulative_v1/call_ledger_50k.jsonl` | `DD90DBA82CF7FC803DF6156679EBA2A9DFB6D50285685B63C6A99076BFBA3418` | 234601956 |
| `runs/production_milestones_cumulative_v1/milestone_report_50k.md` | `85914C69026400FABD32C519DE9538D47D895EAA936795FBF6A1862C3B8C5B50` | 15830 |
| `runs/production_milestones_cumulative_v1/milestone_report_50k.json` | `36865854B2A803D165ACB49E070C927438F7AA98F3158EBDDC315A4DA19D9E43` | 24056 |

## 7. Code / Protocol File Hashes At Freeze

| File | SHA256 | Bytes |
|---|---|---:|
| `docs/BUG_FIX_LOG.md` | `849067410E4FCA51C63C7A8E3631F07E7E3428C2FB43B8FB849E03DD01A27CBD` | 8683 |
| `execute_remaining_milestone_run.bat` | `384718B333DCD526C1A6D88952DE3280EB3F69FF48442374352A4AF4CAFDF654` | 3388 |
| `materialize_paraphrases.bat` | `D312A30F101060AA4833B5DD78EB2DA6FE10F2A5E9632EC89EF9860986CA3F92` | 943 |
| `src/production/execute_milestone.py` | `8EA406A987B073BA485750AD40A00030F2EEA82C3DC5F0B6F377DED028ABA63B` | 23876 |
| `src/production/failure_policy.py` | `84B2A9AF7AD4A17CDC1A5C66C46182C2CA6FD3F02DBE01F5E2AA4DAFC2A3C64A` | 5572 |
| `src/production/materialize_paraphrases.py` | `F6FCC076F0D8DEB99B0561CAC5C06FDBC910315480DF7FC1D1B8E17616E6981C` | 9390 |
| `src/production/progress_status.py` | `11E698188B0E9780E2F92FE83FBEB3ED16037172B74710E3C20A4DC29D107495` | 8175 |
| `src/production/reporting.py` | `D8C2C6A2A4772DA7AC83FD92CB2057C95D60211C567ADC2CE3E33D3F369D50EF` | 28552 |
| `src/production/run_milestone.py` | `92FA75FC72C4A4147C850E8226E1D9A3AD7E2AE5D713C943B7EB2ED4BD1FC989` | 24632 |
| `src/protocol/call_milestones.py` | `022A85C44FD6DCD480D4D271FBC265C82A3031F054F1824E4471DD6BA1D0267E` | 14470 |
| `tests/test_core_pipeline.py` | `5BC6249AD567C681E0400022ED61BFD01ED4A43B46501E42B3333F39687E6DDF` | 48941 |

## 8. Execution Commands For 50k

After this manifest is uploaded to OSF, first materialize the remaining 50k paraphrase prework:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
$env:PARAPHRASE_HELPER_MODEL_ID='grok-4.3'
Remove-Item Env:\PARAPHRASE_MAX_ITEMS -ErrorAction SilentlyContinue

.\materialize_paraphrases.bat 50k
```

Then verify that no prework remains:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:PYTHONPATH='src'
python -m production.progress_status --run-id production_milestones_cumulative_v1 --milestone 50k
```

Expected after materialization:

```text
prework_blocked_left=0
db_integrity=ok
```

Then execute the remaining provider calls:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:SHARD_COUNT='1'
Remove-Item Env:\SKIP_MODEL_IDS -ErrorAction SilentlyContinue

$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'

.\execute_remaining_milestone_run.bat 50k
```

Expected additional provider calls before 50k completion:

- paraphrase helper prework: up to `50` xAI helper calls
- study calls: `13000`

Final successful 50k status should be:

```text
completed=47500/47500
left_total=0
provider_executable_left=0
prework_blocked_left=0
api_errors=0
terminal_failures=0
db_integrity=ok
```

## 9. Release Notes For GitHub

Suggested release:

- tag: `post-35k-pre50k-freeze-v1`
- title: `Post-35k milestone and pre-50k freeze v1`

Suggested release notes:

```text
Completed the amended 35k milestone for production_milestones_cumulative_v1.

Decision: continue to 50k.

Key 35k checks:
- 35000/35000 target calls complete
- 0 API errors and 0 terminal failures in the final report
- overall validity rate 0.9987
- minimum model/mode validity rate 0.9700
- low/diffuse agreement surplus 0.3989 versus high-consensus agreement surplus 0.1711
- low/diffuse distribution-agreement gap 0.2320 versus high-consensus gap 0.1831
- positive gap, surplus, and sampling-compression signs in all five models

The 50k target list and pre-materialization planning artifacts are frozen in run_manifest_pre50k_freeze_v1.md.
The 50k milestone contains 47,500 planned study calls: 20k core cross-format, 20k repeated sampling, 2.5k paraphrase audit, and 5k normative-certainty calls.
```

## 10. OSF Upload Checklist

Upload this manifest and the following run artifacts to OSF. Because `runs/` is gitignored, these artifacts are not expected to appear in the GitHub release.

Recommended OSF folder: `milestones/35k_post_and_50k_pre_freeze/`

- `run_manifest_pre50k_freeze_v1.md`
- `runs/production_milestones_cumulative_v1/milestone_report_35k.md`
- `runs/production_milestones_cumulative_v1/milestone_report_35k.json`
- `runs/production_milestones_cumulative_v1/execution_summary_35k.json`
- `runs/production_milestones_cumulative_v1/run_summary_35k.json`
- `runs/production_milestones_cumulative_v1/selected_items_35k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_35k.jsonl`
- `runs/production_milestones_cumulative_v1/call_ledger_35k.csv`
- `runs/production_milestones_cumulative_v1/call_ledger_35k.jsonl`
- `runs/production_milestones_cumulative_v1/run_summary_50k.json`
- `runs/production_milestones_cumulative_v1/pending_api_calls_50k.jsonl`
- `runs/production_milestones_cumulative_v1/selected_items_50k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_50k.jsonl`
- `runs/production_milestones_cumulative_v1/call_ledger_50k.csv`
- `runs/production_milestones_cumulative_v1/call_ledger_50k.jsonl`
- `runs/production_milestones_cumulative_v1/milestone_report_50k.md`
- `runs/production_milestones_cumulative_v1/milestone_report_50k.json`

After creating the GitHub release and Zenodo DOI, update section 0 with the minted DOI before or immediately after OSF upload.
