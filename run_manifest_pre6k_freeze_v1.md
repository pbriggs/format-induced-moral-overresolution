# Run Manifest Pre-6k Freeze v1

Date: 2026-06-17

This file freezes the post-3k / pre-6k study state for `format-induced-moral-overresolution`. It supplements the pre-3k freeze and the Gemini-to-Grok amendment. It should be uploaded to OSF before running the 6k milestone.

## 0. Archive Identifiers

- OSF project: `https://osf.io/rwhax/`
- GitHub release/tag: `post-3k-milestone-v1`
- GitHub release URL: `https://github.com/pbriggs/format-induced-moral-overresolution/releases/tag/post-3k-milestone-v1`
- Zenodo DOI: `https://doi.org/10.5281/zenodo.20738342`
- Git commit at freeze: `dc0fe0c`
- Author: Paul Briggs
- License: CC0 1.0 Universal, unless superseded by OSF project settings. Dataset and model-output redistribution remain subject to SCRUPLES/AllenAI terms, model-provider terms, privacy considerations, and institutional review requirements.

## 1. Prior Protocol Records

This pre-6k freeze inherits from:

- `run_manifest_pre3k_freeze_v2.md`
- `run_manifest_amendment_2026-06-17_gemini_to_grok_v1.md`
- `docs/BUG_FIX_LOG.md`
- `docs/STUDY_PROCESS.md`

The Gemini-to-Grok amendment replaced future Gemini-slot collection with direct xAI `grok-4.3` because first-party Gemini availability failures prevented completion of the original Gemini slot during the exploratory 3k work. Previously collected Gemini rows remain historical pre-amendment artifacts and are not relabeled.

## 2. Frozen Model Roster For 6k

Use exactly this `STUDY_MODEL_IDS` value for 6k:

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

## 3. 3k Milestone Decision

The 3k milestone completed under `RUN_ID=production_milestones_cumulative_v1`.

Summary from `runs/production_milestones_cumulative_v1/milestone_report_3k.json`:

- planned: `3000`
- attempted: `3000`
- completed successful: `3000`
- API errors: `0`
- terminal failures: `0`
- overall validity rate: `0.9983333333333333`
- minimum model/mode validity rate: `0.96`
- failing validity cells: `[]`
- malformed rate: `0.0003333333333333333`
- refusal rate: `0.0`
- off-schema rate: `0.0`
- paraphrase outputs: `500`
- valid paraphrase outputs: `498`
- low/diffuse distribution-agreement gap mean: `0.21911212025316457`
- low/diffuse agreement-surplus mean: `0.3928812742397604`
- positive gap models: `5`
- positive surplus models: `5`
- positive sampling-compression models: `5`
- decision: `continue`

Interpretation: 3k is an exploratory engineering and measurement smoke test. The result supports continuing to 6k; it is not a confirmatory theory-level decision.

## 4. 3k Final Artifact Hashes

These 3k artifacts should be uploaded to OSF under a 3k milestone outputs folder.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/milestone_report_3k.md` | `5A42F4C83890A40CEFD74DD138F7073E0D80C6ED773D9E60D6E3B2B149F539BC` | 14851 |
| `runs/production_milestones_cumulative_v1/milestone_report_3k.json` | `1B85FD7CC2D0668C2D3218A5C14388FC854811F383C956FCA2AD23B6BCF76747` | 21758 |
| `runs/production_milestones_cumulative_v1/execution_summary_3k.json` | `77DC0B4693AFD9CAE18BCEAAB6DD756E92821EF2840D740172262EED8BE8F52D` | 2944 |
| `runs/production_milestones_cumulative_v1/run_summary_3k.json` | `CCF458DC8BE7712EC0775A68D3C4A5729290F063AC8FE43C0B7A6740F261AAF2` | 1956 |
| `runs/production_milestones_cumulative_v1/selected_items_3k.jsonl` | `F7E86C8C834C4FEE84123BB55232B7C81A68212CDD8665D1FC782B5DE96E5D8C` | 91238 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_3k.jsonl` | `CF4BC549978CD65A3628F7F6AB87FAFF9329FC211A47B4D3FE99AB5CC72AF757` | 321000 |
| `runs/production_milestones_cumulative_v1/call_ledger_3k.csv` | `06B1DBBD9C96DB9CAEE685C4D1399BA0ECFFEDFC6F1FFD484A9059C3E2FA195F` | 12001738 |
| `runs/production_milestones_cumulative_v1/call_ledger_3k.jsonl` | `5E518FC8619C86FD1AEC564413771604EAFB17B7BE50179B6DD5CFBD54DA64DF` | 17280035 |

The call ledgers include rendered prompts and raw model outputs. Upload/share according to OSF visibility settings, provider terms, privacy considerations, and institutional review requirements.

## 5. 6k Planned-Call Freeze

The 6k target list was planned before provider execution with:

```powershell
$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'
.\start_milestone_run.bat 6k
```

Planning summary:

- `RUN_ID`: `production_milestones_cumulative_v1`
- milestone: `6k`
- planned calls for milestone: `6000`
- completed successful calls carried forward from 3k: `3000`
- pending calls before 6k execution: `3000`
- provider-executable pending calls before 6k execution: `3000`
- blocked prework calls before 6k execution: `0`
- newly inserted planned calls: `3000`
- earlier planned calls outside current target: `600`

The `600` earlier planned calls outside the current 6k target are superseded pre-amendment/historical rows in the same run database. Current progress and reporting should be scoped to `target_api_call_ids_6k.jsonl`.

6k component allocation:

| Component | Items |
|---|---:|
| core cross-format | 400 |
| repeated sampling | 50 |
| paraphrase audit | 50 |

Bin allocation:

| Component | high consensus | moderate consensus | low consensus | diffuse |
|---|---:|---:|---:|---:|
| core cross-format | 60 | 80 | 160 | 100 |
| repeated sampling | 8 | 10 | 20 | 12 |
| paraphrase audit | 8 | 10 | 20 | 12 |

The 6k paraphrase-audit prework is already materialized from the 3k paraphrase workflow; no 6k calls are prework-blocked at this freeze.

## 6. 6k Pre-Execution Planning Artifact Hashes

These hashes freeze the pre-execution 6k target list and planning outputs. Some files, especially ledgers and reports, are expected to be overwritten with final execution contents after 6k completes.

| Artifact | SHA256 | Bytes |
|---|---|---:|
| `runs/production_milestones_cumulative_v1/run_summary_6k.json` | `BFA1B0DA6C08A7B51C9BD98450E25320EE48E0F32246BF26CB07A25086DE4C98` | 1972 |
| `runs/production_milestones_cumulative_v1/pending_api_calls_6k.jsonl` | `7B6E140EE65BD52C862B648D6B5381CE86B902AD74AB42B4F10C616FE625F8C4` | 10199235 |
| `runs/production_milestones_cumulative_v1/selected_items_6k.jsonl` | `6DC840162EED8BBE72541560E30A73DBEEEB184F8714550DAC393CB836FF151A` | 169136 |
| `runs/production_milestones_cumulative_v1/target_api_call_ids_6k.jsonl` | `F3298036B83725013320D850C2E91211749366771194507625CC73B6E951D198` | 642000 |
| `runs/production_milestones_cumulative_v1/call_ledger_6k.csv` | `607AEFE5782B34EA41E73BA939B26D10526DDE070C52431E81C20034F69EE7A3` | 15350968 |
| `runs/production_milestones_cumulative_v1/call_ledger_6k.jsonl` | `2992737BCD134CA0E813F0F09084EBFDF3BFCCF72905036DE300B6E0D2ED0821` | 26004265 |
| `runs/production_milestones_cumulative_v1/milestone_report_6k.md` | `D1B099F8655355039F7E670DC46B8E2C0114E24CD2C81D4620EC5EE04E366FC8` | 14934 |
| `runs/production_milestones_cumulative_v1/milestone_report_6k.json` | `497B9B84FCA9E56684EEB4DD97852CE92B314F2B7389B9A0DE6DE621A022014E` | 21826 |

## 7. Code / Protocol File Hashes At Freeze

| File | SHA256 |
|---|---|
| `run_manifest_amendment_2026-06-17_gemini_to_grok_v1.md` | `DF0FDAA1B50D526B9E6A985D7C12C39879A3D01A0B5715417BF37E7E2088E3EF` |
| `docs/BUG_FIX_LOG.md` | `B051193C198612037FEDBDE618A8856257C27C22400888D7A30CD3EB6386CE42` |
| `docs/STUDY_PROCESS.md` | `0E60C52B3058D6A799FCCA571173CA4D6A6FEB65F391A65FBB10F4876013EF68` |
| `src/prompts/prompt_templates.py` | `7F673DD3CA14D3780B53C05D16B67DF2AF98C7C750FC97256938A9976F32599B` |
| `src/prompts/schemas.py` | `58A3C91E42CB8264253F1C705A6C6D2162405FC6167E61C9EC28F5EEFEF02619` |
| `src/parsing/validate_json.py` | `90D63B945ADF60B51CAF551FBD478541D61C7FF47F783E66092CA8B801443270` |
| `src/production/config.py` | `18E3BB888C39ACA6595C630FDFE5758BAA77F79418123D2792B43204BF8324FE` |
| `src/production/providers.py` | `DA9D369DE6D4C4A1B51D39D548F24D7AFC980747110627DC563FA2925BB73530` |
| `src/production/run_milestone.py` | `544F19E633B72EAE906CBD833F7DE5DBEC3C4749EF4109BAF3DD74AC804E7D81` |
| `src/production/execute_milestone.py` | `8818C66453AE0CAD760ED47DFA70BBC97E262B3BA1C7422A482CD72AC3024429` |
| `src/production/progress_status.py` | `C43E6EDE20E63BBE5EA95EB60650C6F3652D8F1669C1538086816654A0F321C7` |
| `src/production/materialize_paraphrases.py` | `F6FCC076F0D8DEB99B0561CAC5C06FDBC910315480DF7FC1D1B8E17616E6981C` |

## 8. Execution Command For 6k

After this manifest is uploaded to OSF, run:

```powershell
Set-Location "C:\Users\pivan\OneDrive\Documents\VSCode\public_repo\format-induced-moral-overresolution\"

$env:MOCK_PROVIDER='0'
$env:RUN_ID='production_milestones_cumulative_v1'
$env:SHARD_COUNT='20'
Remove-Item Env:\SKIP_MODEL_IDS -ErrorAction SilentlyContinue

$env:STUDY_MODEL_IDS='gpt-5.5,grok-4.3,claude-sonnet-4-6,qwen/qwen3.7-max,deepseek/deepseek-v3.2'

.\execute_remaining_milestone_run.bat 6k
```

Expected additional provider calls: `3000`.

## 9. Next Decision Point

The 6k milestone remains exploratory. It should be used as a first directional signal check and operational robustness check after the amended roster, not as a final confirmatory test.

Continue beyond 6k only if:

- provider/API stability remains acceptable;
- validity remains above protocol thresholds;
- distribution outputs remain non-degenerate;
- agreement estimates remain interpretable;
- low-consensus/diffuse directional signals remain positive across enough models under the milestone decision rule.
