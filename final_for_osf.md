You are basically ready, but I would **not "just run to the end" yet**. Do one more clean freeze before the 3k run.

## What to do with OSF now

First, confirm the registration is fully archived/approved. If it is still pending, OSF says admin contributors can approve it, otherwise it auto-approves after 48 hours; OSF also warns not to add/edit/delete files during archiving because that can cause archiving failure. ([OSF Support][1])

After that, you have two defensible paths:

**Best path:** treat **3k and 6k as pilots**, **13k as diagnostic**, and make **25k / 35k / 50k** the confirmatory run. That matches your milestone document, which explicitly warns that repeated milestone looks create researcher-degree-of-freedom problems unless staged monitoring was preregistered.

**Also acceptable:** treat the whole sequence as preregistered and cumulative, but only if your item list, call order, stop/continue rules, and milestone reporting rules are frozen before the first call. Your protocol already says the 3k, 6k, 13k, and 25k target call sets are cumulative by planned call ID, and that staged milestones are exploratory unless separately preregistered as staged feasibility checks.

My recommendation: **run 3k as an exploratory engineering pilot**, not confirmatory. That is safest.

## Before the 3k run, freeze one file

Create and upload a `run_manifest_v1.json` or `run_manifest_v1.md` to the editable OSF project and GitHub. It should include:

1. exact model roster, provider/API route, model IDs, version strings if available;
2. API parameters and structured-output settings;
3. prompt template files and hashes;
4. JSON schemas / response fields;
5. random seed and stratified item-selection method;
6. the exact 3k planned call list;
7. label order/counterbalancing rule;
8. retry and one-repair rule;
9. exclusion rules;
10. whether the 3k output is **pilot/exploratory** or part of a cumulative confirmatory sequence.

This directly matches your OSF protocol's requirement to freeze prompt templates, schemas, model roster/replacement rules, randomization, parsing/repair rules, repeated-sampling subset rules, analysis specs, run manifest, and version hashes before confirmatory collection.

## What data to collect and preserve

For every API call, store a row-level ledger with:

| Category | Fields to store |
|---|---|
| Call identity | `run_id`, `planned_call_id`, `milestone`, `call_type`, `is_pilot`, `is_confirmatory` |
| Item metadata | `item_id`, source dataset version/hash, disagreement bin, source-community counts, smoothed probabilities, entropy, majority label, majority support |
| Prompt metadata | prompt mode, prompt template hash, rendered prompt hash, canonical label order, item order seed |
| Model metadata | provider, model ID, API route, model version/date if available |
| API settings | temperature or equivalent, top-p if used, max tokens, structured-output setting, seed if supported |
| Timing/cost | UTC timestamp, latency, input tokens, output tokens, cost estimate |
| Raw output | raw response text/JSON, finish reason, refusal/safety signal if any |
| Parsed output | chosen label, label probabilities, estimated source-community agreement, moral certainty if used, sampling label |
| Validity | strict valid, repaired valid, malformed, off-schema, refusal, API error |
| Retry/repair | retry number, repair attempted, repair prompt hash, final usable status |
| Exclusion status | included/excluded, exclusion reason |

Your protocol already says the final report should disclose attempted calls, valid parsed outputs, retries, repairs, exclusions, model availability changes, and deviations from the frozen manifest.

## What to upload publicly

Use **GitHub for living code**, but use **OSF/Zenodo for archival citation**.

GitHub is good for code, issues, commit history, and reproducibility. For citable fixed versions, GitHub's docs recommend Zenodo because it can archive a public GitHub repository and issue a DOI for each release. ([GitHub Docs][2]) OSF also lets you add linked resources such as data, analytic code, supplements, materials, and papers to the registration via the Resources tab. ([OSF Support][1])

Suggested public repo structure:

```text
README.md
LICENSE
CITATION.cff
osf/
  osf_registration.md
  run_manifest_v1.md
  milestone_decision_rules.md
prompts/
  distribution_mode.md
  descriptive_verdict_agreement_mode.md
  sampling_mode.md
schemas/
  distribution_schema.json
  verdict_schema.json
  sampling_schema.json
data_public/
  item_metadata_no_raw_text.csv
  source_distribution_table.csv
  call_ledger_public.csv
  parsed_outputs.csv
  exclusion_log.csv
analysis/
  compute_metrics.py
  milestone_report.py
  confirmatory_models.py
reports/
  milestone_3k_report.md
  milestone_6k_report.md
```

Be careful with raw SCRUPLES anecdotes and raw model outputs. Your OSF protocol says raw anecdotes and raw model outputs should be shared only if permitted by dataset license, provider terms, privacy considerations, and ethical review. A safer default is: public code, prompts, manifests, derived metrics, aggregate tables, and exclusion logs; restricted or omitted raw anecdote text unless you confirm redistribution rights.

## What to register after each milestone

Do **not** create a brand-new OSF registration after every milestone. Instead, create a dated milestone report and upload/link it as a project file or GitHub release. Each report should include:

1. calls attempted and completed;
2. retry rate;
3. JSON validity by model and mode;
4. malformed/refusal/off-schema rate;
5. distribution entropy by disagreement bin;
6. agreement surplus by bin/model;
7. distribution-agreement gap by bin/model;
8. sampling compression if available;
9. paraphrase/label-order check result if available;
10. decision: continue, revise, stop, or redesign.

That list matches your milestone document's reporting plan.

## Bottom line

You can start once the registration is archived/approved and the `run_manifest_v1` is frozen. I would run **3k as exploratory**, generate the milestone report, and only make changes through a clearly timestamped OSF update before any later confirmatory collection. OSF supports registration updates with a justification, but files attached to the registration itself cannot currently be added/removed during an update, so keep living materials in the OSF project/GitHub and link fixed releases back to the registration. ([OSF Support][1])

[1]: https://help.osf.io/article/330-welcome-to-registrations "Welcome to Registrations & Preregistrations! - OSF Support"
[2]: https://docs.github.com/repositories/archiving-a-github-repository/referencing-and-citing-content "Referencing and citing content - GitHub Docs"
