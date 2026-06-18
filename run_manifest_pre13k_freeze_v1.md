# Run Manifest Pre-13k Freeze v1

Date: 2026-06-17

This file freezes the post-6k / pre-13k study state for `format-induced-moral-overresolution`. It supplements the pre-3k freeze, the Gemini-to-Grok amendment, and the pre-6k freeze. It should be uploaded to OSF before running the 13k milestone.

## 0. Archive Identifiers

- OSF project: `https://osf.io/rwhax/`
- Prior GitHub release/tag: `post-3k-milestone-v1`
- Prior GitHub release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-3k-milestone-v1`
- Prior Zenodo DOI: `https://doi.org/10.5281/zenodo.20738342`
- New GitHub release/tag to create: `post-6k-pre13k-freeze-v1`
- New GitHub release URL to create: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-6k-pre13k-freeze-v1`
- New Zenodo DOI: `https://doi.org/10.5281/zenodo.20740440`
- Git commit at freeze: `SHA 4ea1d0f17e34d438bb860b0d5ec8f6c7e8ff04b7`
- Author: Paul Briggs
- License: CC0 1.0 Universal, unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## 1. Prior Protocol Records

This pre-13k freeze inherits from:

- `run_manifest_pre3k_freeze_v2.md`
- `run_manifest_amendment_2026-06-17_gemini_to_grok_v1.md`
- `run_manifest_pre6k_freeze_v1.md`
- `docs/BUG_FIX_LOG.md`
- `docs/STUDY_PROCESS.md`

The amended model roster remains in force. Previously collected Gemini rows remain historical pre-amendment artifacts and are not relabeled.

## 2. Frozen Model Roster For 13k

Use exactly this `STUDY_MODEL_IDS` value for 13k:

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

Required provider environment variables:

- `OPENAI_API_KEY`, `OPENAI_MODEL`
- `XAI_API_KEY`, `XAI_MODEL=grok-4.3`, optional `XAI_BASE_URL=https://api.x.ai/v1`
- `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`
- `LLAMA_API_KEY`, `LLAMA_MODEL`, optional `LLAMA_BASE_URL`

## 3. 6k Milestone Decision

The 6k milestone completed under `RUN_ID=production_milestones_cumulative_v1`.

Summary from the cumulative `runs/production_milestones_cumulative_v1/milestone_report_6k.json`:

- planned: `6000`
- attempted: `6000`
- completed successful: `6000`
- API errors: `0`
- terminal failures: `0`
- overall validity rate: `0.9983333333333333`
- minimum model/mode validity rate: `0.96`
- low/diffuse distribution-agreement gap mean: `0.22922554245283017`
- high-consensus distribution-agreement gap mean: `0.17203333333333332`
- low/diffuse agreement-surplus mean: `0.3977102313713058`
- high-consensus agreement-surplus mean: `0.14979498100296268`
- positive gap models: `5`
- positive surplus models: `5`
- positive sampling-compression models: `5`
- paraphrase outputs: `500`
- valid paraphrase outputs: `498`
- unique paraphrase label orders: `120`
- decision: `continue`

Interpretation: 6k is the first substantive directional signal check. The pattern is directionally supportive of the hypothesis and supports continuing to 13k, but it is not a final confirmatory test.

## 4. 6k Final Artifact Hashes

These 6k artifacts should be uploaded to OSF under a 6k milestone outputs folder.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/milestone_report_6k.md` | `91EE9CBA3B1C27424783C62A8F0166CD078084AD8F09B23803CEFEEACF983AAE` | 14968 |
| `runs/production_milestones_cumulative_v1/milestone_report_6k.json` | `0D7AFAF0F16CA078A502BFFDF14C6F7D7C5C0F96C830902A9B390B1C127AEE39` | 21882 |
| `runs/production_milestones_cumulative_v1/execution_summary_6k.json` | `DBBE2F6DE0052416D20E607945A8F9F4363A194827A510538104B9733E77663D` | 2951 |
| `runs/production_milestones_cumulative_v1/run_summary_6k.json` | `E31F1683CE7A193213247DDDAD1F3F40718338BF3C3470D21691BEC80576D222` | 1963 |
| `runs/production_milestones_cumulative_v1/selected_items_6k.jsonl` | `6DC840162EED8BBE72541560E30A73DBEEEB184F8714550DAC393CB836FF151A` | 169136 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_6k.jsonl` | `F3298036B83725013320D850C2E91211749366771194507625CC73B6E951D198` | 642000 |
| `runs/production_milestones_cumulative_v1/call_ledger_6k.csv` | `6934ABFC85BFB43F25C642B1B25B17B22ADF5F2BB6726A07224A8A94059A6B71` | 24153185 |
| `runs/production_milestones_cumulative_v1/call_ledger_6k.jsonl` | `39FE7B5F55E9DD7E42E50D79815EAA2EA25B5ED1362AC986C6E3E76BB3EB0B8D` | 34715615 |

The call ledgers include rendered prompts and raw model outputs. Upload/share according to OSF visibility settings, provider terms, privacy considerations, and institutional review requirements.

## 5. 13k Planned-Call Freeze

The 13k target list was planned before provider execution with:

```powershell
$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
.\start_milestone_run.bat 13k
```

Planning summary:

- `RUN_ID`: `production_milestones_cumulative_v1`
- milestone: `13k`
- planned calls for milestone: `13000`
- completed successful calls carried forward from 6k: `6000`
- pending calls before 13k execution: `7000`
- provider-executable pending calls before paraphrase materialization: `6500`
- blocked prework calls before paraphrase materialization: `500`
- newly inserted planned calls: `7000`
- earlier planned calls outside current target: `600`

The `600` earlier planned calls outside the current 13k target are superseded pre-amendment/historical rows in the same run database. Current progress and reporting should be scoped to `target_api_call_ids_13k.jsonl`.

13k component allocation:

| Component | Items |
|---|---:|
| core cross-format | 800 |
| repeated sampling | 100 |
| paraphrase audit | 100 |

Bin allocation:

| Component | high consensus | moderate consensus | low consensus | diffuse |
|---|---:|---:|---:|---:|
| core cross-format | 120 | 150 | 320 | 210 |
| repeated sampling | 15 | 20 | 40 | 25 |
| paraphrase audit | 15 | 20 | 40 | 25 |

The 13k target includes `500` paraphrase-audit calls whose prompt material depends on newly materialized paraphrases. Run the paraphrase materialization command before executing the full 13k milestone.

## 6. 13k Pre-Materialization Planning Artifact Hashes

These hashes freeze the 13k target list and planning outputs before paraphrase materialization. Files that contain rendered paraphrase prompts, ledgers, or execution reports are expected to change after `materialize_paraphrases.bat 13k` and provider execution.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/run_summary_13k.json` | `6DCC5795A23305EBEF7A31637C11FEF0921D8D5C29C0DE14290B0E7B1B347C1B` | 1988 |
| `runs/production_milestones_cumulative_v1/pending_api_calls_13k.jsonl` | `A4A825E1B27088D040BD5FB9BDE7600D9250A02DBF23F6B5F08C8A96988AED45` | 23919760 |
| `runs/production_milestones_cumulative_v1/selected_items_13k.jsonl` | `4424276596534735FC270FFBDEEEA22FEF170788E10F5D3E3ED379E84EE488A5` | 339162 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_13k.jsonl` | `E5BAF36D2A5A2024DA8619AB22184D08798C983B7EB1F7DEB9DBAC03F04AA5E5` | 1404000 |
| `runs/production_milestones_cumulative_v1/call_ledger_13k.csv` | `512CEFDB29EA46DB9763079E75AD86211372AA61E109E7D0F28C39EEB9A918AF` | 31957565 |
| `runs/production_milestones_cumulative_v1/call_ledger_13k.jsonl` | `6C6C41D54F6AF232273E4A2728CD8B44EC55DC0356E63ED8B8AE67B55B21DA46` | 55060995 |
| `runs/production_milestones_cumulative_v1/milestone_report_13k.md` | `81BAB834DCB6C2F340595F9B6C9BF6FFACFE62261DF7FFD5EEA2C12F7DFF2091` | 15052 |
| `runs/production_milestones_cumulative_v1/milestone_report_13k.json` | `69233958933E6CA64BCC72240C4BC31A6C88A9316D9D9CA84C64E3CBAD0D364A` | 21950 |

## 7. Code / Protocol File Hashes At Freeze

| File | SHA256 | Bytes |
|---|---|---:|
| `docs/BUG_FIX_LOG.md` | `ED917BDCE7EE40E48D9218718655F8AB037D41979A58513E59E3788E0AE190E7` | 6456 |
| `src/protocol/call_milestones.py` | `022A85C44FD6DCD480D4D271FBC265C82A3031F054F1824E4471DD6BA1D0267E` | 14470 |
| `src/pilot/pilot_diagnostics.py` | `3A87CAEB2093467A97E529CC32D627EF7860827FEA879B0E01035B43DCE399A7` | 7641 |
| `src/production/reporting.py` | `8A2B8D67091CAEF605D7BB5A2688EAF45E1C5B289096D9F1EB3A084DEF1813C8` | 28079 |
| `src/production/progress_status.py` | `EA2A2062C4FB97A0A2BA08D699293D41995C6DA5BBE4FCD47A559D29D8877029` | 7812 |

The 6k milestone review added an explicit post-6k decision criterion requiring the low-consensus/diffuse agreement surplus mean to exceed the high-consensus agreement surplus mean. It also fixed cumulative progress/reporting for milestones whose target IDs span earlier milestone rows.

## 8. Execution Commands For 13k

After this manifest is uploaded to OSF, first materialize the remaining 13k paraphrase prework:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
$env:PARAPHRASE_HELPER_MODEL_ID='grok-4.3'
Remove-Item Env:\PARAPHRASE_MAX_ITEMS -ErrorAction SilentlyContinue

.\materialize_paraphrases.bat 13k
```

Then execute the remaining provider calls:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:SHARD_COUNT='20'
Remove-Item Env:\SKIP_MODEL_IDS -ErrorAction SilentlyContinue

$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'

.\execute_remaining_milestone_run.bat 13k
```

Expected additional provider calls before 13k completion:

- paraphrase helper prework: up to `50` xAI helper calls
- study calls: `7000`

## 9. Release Notes For GitHub

Suggested release:

- tag: `post-6k-pre13k-freeze-v1`
- title: `Post-6k milestone and pre-13k freeze v1`

Suggested release notes:

```text
Completed the amended 6k milestone for production_milestones_cumulative_v1.

Decision: continue to 13k.

Key 6k checks:
- 6000/6000 target calls complete
- 0 API errors and 0 terminal failures in the cumulative 6k report
- overall validity rate 0.9983
- low/diffuse agreement surplus 0.3977 versus high-consensus agreement surplus 0.1498
- low/diffuse distribution-agreement gap 0.2292 versus high-consensus gap 0.1720
- positive gap, surplus, and sampling-compression signs in all five models

This release also includes the 6k milestone-review code updates:
- cumulative progress/reporting scoped correctly by target API call IDs
- high-consensus agreement-surplus metric added to milestone reports
- 6k+ decision rule requiring contested agreement surplus to exceed high-consensus surplus
- regression tests for cumulative progress and the new decision criterion

The 13k target list and pre-materialization planning artifacts are frozen in run_manifest_pre13k_freeze_v1.md.
```

## 10. OSF Upload Checklist

Upload this manifest and the following run artifacts to OSF. Because `runs/` is gitignored, these artifacts are not expected to appear in the GitHub release.

Recommended OSF folder: `milestones/6k_post_and_13k_pre_freeze/`

- `run_manifest_pre13k_freeze_v1.md`
- `runs/production_milestones_cumulative_v1/milestone_report_6k.md`
- `runs/production_milestones_cumulative_v1/milestone_report_6k.json`
- `runs/production_milestones_cumulative_v1/execution_summary_6k.json`
- `runs/production_milestones_cumulative_v1/run_summary_6k.json`
- `runs/production_milestones_cumulative_v1/selected_items_6k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_6k.jsonl`
- `runs/production_milestones_cumulative_v1/call_ledger_6k.csv`
- `runs/production_milestones_cumulative_v1/call_ledger_6k.jsonl`
- `runs/production_milestones_cumulative_v1/run_summary_13k.json`
- `runs/production_milestones_cumulative_v1/selected_items_13k.jsonl`
- `runs/production_milestones_cumulative_v1/target_api_call_ids_13k.jsonl`
- `runs/production_milestones_cumulative_v1/pending_api_calls_13k.jsonl`

After creating the GitHub release and Zenodo archive, update OSF with the GitHub release URL and Zenodo DOI. If OSF has no dedicated DOI field, add them to the project wiki/description or upload a small note file beside this manifest.

## 11. Next Decision Point

The 13k milestone is the next major check. Continue beyond 13k only if:

- provider/API stability remains acceptable;
- validity remains above protocol thresholds;
- distribution outputs remain non-degenerate;
- agreement estimates remain interpretable;
- low-consensus/diffuse effects remain larger than high-consensus effects;
- the pattern is not driven by a single model.
