# Verdict-style prompts induce moral over-resolution in large language models

**Author:** Paul Briggs  
**Affiliation:** Independent researcher, Los Angeles, CA, USA  
**Corresponding author:** Paul Briggs, p.ivan.briggs@gmail.com  
**ORCID:** https://orcid.org/0009-0002-9951-8661

## Abstract

Large language models (LLMs) are increasingly asked to make ethical judgments about blame, responsibility and fairness in interpersonal situations. Some cases draw broad agreement; in others, human responses spread across answers. A reliable system should not make cases without a clear majority sound like consensus. Here we test whether LLMs preserve measured disagreement across two forms of answer: estimates of how people voted and a single verdict with estimated agreement. In a preregistered audit, five LLMs evaluated ethical situations with recorded human votes on who was in the wrong. Each model estimated the vote distribution, then chose one answer and estimated how many people would agree. Low-consensus cases were the confirmatory test. When models chose one answer, they overstated agreement: their estimates exceeded both the human vote share and their own distribution estimate for that answer. When models repeatedly answered the same low-consensus cases, their answers covered a narrower range than the human responses for those cases. These findings identify a format-specific reliability failure: LLMs can express measured human disagreement as distributions, but when asked for a verdict, they can overstate agreement and compress disagreement.


A reliability criterion for systems that report judgments is that task-relevant uncertainty should remain coherent across the formats through which users encounter their outputs. Moral judgment provides a useful stress test because disagreement is common, measurable and consequential: some everyday cases have a clear majority, whereas others divide the source community across several answers. In those divided cases, a verdict interface can create a misleading signal if it makes a reference distribution sound more settled than it is.

Prior work has examined whether models predict moral judgments, agree with majority labels or show calibrated confidence [1-7]. This study asks a different question: whether uncertainty about a source-community judgment distribution transfers across output formats. Unlike standard calibration, which compares confidence with correctness, the present audit compares matched model outputs for the same items under distributional and verdict-style elicitation.

We call the tested failure mode **format-induced moral over-resolution**. A model may assign probability mass across several source-community labels when asked for a distribution, yet report stronger apparent agreement when asked for a single verdict and an estimate of how much of the source community would agree. We quantify this failure mode with three matched-item endpoints: agreement surplus relative to the source-community distribution, distribution-agreement gap between the model's own output formats, and sampling compression in repeated forced-choice labels.

The empirical target is deliberately narrow. We use SCRUPLES Anecdotes because it provides everyday ethical situations with source-community judgments about who was in the wrong [4]. The phrase "source community" refers to the annotator/judgment population represented in SCRUPLES. These judgments are reference distributions from that data-generating process, not authoritative moral labels, universal moral norms, representative population estimates or deployment-ready normative standards. In the audit, five LLMs evaluated matched items in distribution mode, descriptive verdict/agreement mode and repeated-sampling mode (Fig. 1). Low-consensus items were the registered confirmatory subset; diffuse/no-clear-consensus items were analysed separately as secondary evidence.

The contribution is threefold. First, the study operationalizes cross-format uncertainty transfer for source-community moral judgments. Second, it defines matched-item endpoints that separate surplus agreement relative to the source-community distribution, within-model incoherence across output formats, and compression in repeated forced-choice labels. Third, it shows in a preregistered five-model audit that verdict-style elicitation inflates apparent agreement and compresses disagreement, with the clearest reliability concern arising when source-community judgments are divided.

## Results


### Endpoint logic and target set

A verdict-style output can over-resolve a source-community distribution in three linked ways. First, it can report more agreement for a selected label than the source-community distribution supports. Second, it can report more agreement than the same model's distribution-mode probability for that label. Third, repeated forced-choice outputs can occupy a narrower effective label range than the source-community votes.

The low-consensus bin was the primary confirmatory subset because these items have a majority label but still substantial source-community disagreement. Diffuse/no-clear-consensus items were kept separate as secondary evidence, and high-consensus items served as a reference condition. Each endpoint therefore compares matched item-model outputs rather than unrelated prompts, while preserving the primary/secondary distinction.

The frozen target-scoped audit contained 47,500 target calls and 47,432 primary-valid outputs. Its core cross-format component evaluated 2,000 unique items with five models in distribution and verdict/agreement modes.

Repeated sampling, paraphrase and normative certainty were included as supporting or secondary components rather than additional primary endpoints. Repeated sampling supports the sampling-compression endpoint, the paraphrase component is used only as aggregate surface-form evidence, and normative certainty remains a separate secondary descriptive construct rather than estimated source-community agreement. Component allocation and the frozen model roster are reported in Table 1.


### Verdict prompts inflate apparent agreement

Agreement surplus addresses the first step in the over-resolution argument: does verdict-style elicitation merely select one label, or does it also attach inflated source-community agreement to that label? For each verdict/agreement output, agreement surplus was the model's estimated source-community agreement minus the source-community support for the selected label.

In the low-consensus primary subset, agreement surplus was 0.370931 (95% CI, 0.361206-0.381114; Holm-adjusted P = 0.0015; n = 3,749 item-model rows; Fig. 2 and Table 2). Thus, verdict-mode agreement estimates exceeded source-community support for the chosen label by approximately 37 percentage points. The reliability problem is not only that verdict mode returns one label; it is that the accompanying agreement estimate makes that label appear more socially supported than it is in the source-community distribution.

Diffuse/no-clear-consensus items showed a larger secondary estimate: agreement surplus was 0.435619 (95% CI, 0.427337-0.444341; n = 2,500). High-consensus items also showed positive agreement surplus, 0.169409 (95% CI, 0.145651-0.194624; n = 1,750). The low-consensus-minus-high-consensus contrast was 0.201523 (95% CI, 0.174835-0.228568). Over-resolution was therefore not confined to divided items, but the surplus was larger where source-community agreement was weaker.

### Verdict agreement exceeds the model's distributional estimate

Agreement surplus compares verdict-mode reports with the source-community distribution. The distribution-agreement gap is the central within-model test: for the same model, the same item and the label selected in verdict mode, do the distribution and verdict/agreement outputs communicate compatible levels of source-community agreement? This endpoint does not require distribution-mode estimates to be perfectly calibrated to the SCRUPLES source-community distribution. It asks whether the model's own distributional estimate remains coherent with its verdict/agreement estimate.

In low-consensus items, the distribution-agreement gap was 0.232687 (95% CI, 0.224387-0.241341; Holm-adjusted P = 0.0015; n = 3,736; Fig. 3 and Table 2). A positive gap means that the verdict/agreement format reported more source-community agreement with the chosen label than the same model's distribution-mode probability for that label.

Diffuse items showed a secondary gap of 0.226556 (95% CI, 0.216740-0.237164; n = 2,494). High-consensus items also showed a positive gap of 0.182842 (95% CI, 0.169762-0.196217; n = 1,745). The low-consensus-minus-high-consensus contrast was 0.049845 (95% CI, 0.033774-0.065329). This is why H1b anchors the reliability claim: the same model can communicate different levels of apparent agreement about the same label depending on the output format.

### Repeated sampling compresses source-community disagreement

The first two endpoints test explicit agreement reports. The third asks whether over-resolution is also visible in repeated forced-choice behaviour. Sampling compression was defined as source-community entropy minus repeated-sample model entropy on the five-label scale. Positive values mean that repeated model labels occupied a narrower effective range of labels than the source-community votes for the same items.

In the low-consensus primary subset, sampling compression was 1.264638 bits (95% CI, 1.218425-1.309054; Holm-adjusted P = 0.0015; n = 750 item-model summaries; Fig. 4 and Table 2). Diffuse items showed stronger secondary compression, 1.507379 bits (95% CI, 1.452200-1.562768; n = 500). High-consensus items also showed positive compression, 0.563708 bits (95% CI, 0.495005-0.633547; n = 350). The low-consensus-minus-high-consensus contrast was 0.700930 bits (95% CI, 0.618287-0.783543).

This endpoint extends the evidence beyond explicit agreement estimates. Under the study's repeated forced-choice protocol, model outputs were more concentrated than source-community judgments, especially in divided items. The endpoint should not be read as stochastic sampling from an internal model distribution; it measures diversity across repeated fresh calls under the recorded prompt and label-order randomization protocol.

### Pattern across models and output validity

The aggregate pattern was not driven by a single evaluated model. Each evaluated model showed positive low-consensus agreement surplus, positive low-consensus distribution-agreement gap and positive low-consensus sampling compression. Model-level low-consensus agreement surplus ranged from 0.326454 to 0.445325. Low-consensus distribution-agreement gaps ranged from 0.215187 to 0.271943. Low-consensus sampling compression ranged from 0.920001 to 1.408416. Leave-one-model-out summaries preserved the direction of the aggregate pattern for all three endpoints. These summaries support a shared behavioural pattern across the evaluated roster, without supporting inferential comparisons by provider, route or model lineage.

Output validity also did not suggest a broad parsing failure. Of 47,500 outputs, 47,432 were primary-valid (validity rate = 0.998568), comprising 38,790 strict-schema outputs and 8,642 extracted-JSON outputs. The minimum model/mode primary-valid rate was 0.969. Invalid statuses were 52 probability-out-of-bounds outputs, 10 probability-sum errors, 4 invalid-JSON outputs and 2 empty responses. Refusals and off-schema labels were both zero. Repair fields were tracked; `repair_attempted` and `repair_successful` were both zero, so no repaired outputs entered the final analysis. Validity by model and prompt mode is summarized in Extended Data Fig. 3 and Extended Data Table 1.

### Robustness and diagnostics

Robustness checks addressed five reviewer-facing concerns rather than adding new endpoints. For parsing/schema validity, strict-valid-only analyses preserved the direction of all three low-consensus endpoints, with agreement surplus 0.376030, distribution-agreement gap 0.223867 and sampling compression 1.268188. For source-community distribution construction, sensitivity checks using raw proportions, Jeffreys smoothing and Laplace smoothing preserved positive low-consensus effects. For annotation and `info` sensitivity, the directional pattern was preserved under high-annotation-only, `info`-majority exclusion and high-`info` exclusion analyses.

For distribution-mode non-degeneracy, outputs were not merely fixed uniform or base-rate responses. Source entropy was higher in diffuse items (mean 1.955481 bits) than in high-consensus items (0.823596 bits), and model distribution entropy also varied by bin, with higher entropy in diffuse (1.515785 bits) and low-consensus items (1.476755 bits) than in high-consensus items (1.200675 bits). These diagnostics, summarized in Extended Data Fig. 1, support the premise that distributional prompting elicited non-degenerate, item-sensitive distributions that varied with source-community disagreement. They are support analyses, not a calibration claim and not evidence that the estimates were calibrated to source-community distributions.

For surface-form sensitivity, the paraphrase audit provided aggregate evidence (Extended Data Fig. 2). The paraphrase audit comprised 2,500 target calls and 2,495 valid outputs. In paraphrased low-consensus items, agreement surplus was 0.366821 (95% CI, 0.334632-0.397075) and the distribution-agreement gap was 0.212124 (95% CI, 0.192023-0.231651). In paraphrased diffuse items, the corresponding estimates were 0.418159 (95% CI, 0.396906-0.443057) and 0.200502 (95% CI, 0.174963-0.225410). Within the limited matched overlap, chosen-label stability was 0.655 in low-consensus rows and 0.467 in diffuse rows. Because original-vs-paraphrase matched coverage was limited (29 low-consensus rows and 15 diffuse rows), these results should be read as aggregate surface-form evidence rather than a definitive paired original-vs-paraphrase test. Contamination was not directly measured.

## Discussion

This study identifies output format as a reliability risk when disagreement is part of the target. The failure is not simply that moral cases are difficult. It is that uncertainty available in one elicitation format can be lost when the interface asks for a verdict. Across five evaluated models, distributional prompting elicited non-degenerate, item-sensitive estimates over source-community labels, but verdict-style elicitation reported stronger apparent agreement and repeated forced-choice outputs compressed disagreement.

The central result is not a claim about which moral label is correct. SCRUPLES provides source-community judgments from a particular data-generating process, and those judgments should not be treated as universal norms or representative population estimates. The result is about uncertainty transfer: when the reference distribution is divided, verdict-style prompts can make LLM outputs appear more settled than either the source-community distribution or the model's own distribution-mode estimate supports.

This distinction matters for evaluation. Majority-label accuracy can reward a model for selecting the most common label while missing whether the model communicates the degree of disagreement around that label. A model should not pass an uncertainty evaluation in one format if its verdict interface communicates a conflicting level of agreement on the same cases. Matched-format tests are therefore needed alongside accuracy, calibration and confidence metrics.

The findings also matter for interface design. Users often ask for verdicts in settings where disagreement is relevant to the task. In such settings, distributional interfaces, explicit disagreement summaries and checks for cross-format coherence can reduce the risk that a model converts divided source-community evidence into an overconfident social signal. The implication is not that LLMs should never provide verdicts, but that verdict interfaces should not communicate stronger agreement than the reference distribution or the model's own distributional answer supports.

Several limitations bound the interpretation. The study uses one source-community dataset, five models and a finite set of prompt templates. It does not establish that every LLM or deployed interface behaves the same way. The source community is not a universal or representative population sample. Contamination was not directly measured; the paraphrase audit addresses surface-form sensitivity, not training-set membership. Although item familiarity could affect absolute label probabilities, it would not by itself explain the within-item, same-model pattern in which a model's verdict-mode agreement estimate exceeds its independently elicited distribution-mode probability for the same label. The matched original-vs-paraphrase overlap is small, so paraphrase results should be read as aggregate evidence only. Finally, this is a model-output reliability audit rather than a user study. Future work should test whether cross-format differences affect user beliefs about social consensus, confidence and decision-making.

The implication for model-output reliability is concrete: uncertainty should be evaluated in the formats where users actually encounter it. An evaluation should not ask only whether a model can state a distribution when explicitly prompted. It should also ask whether reported uncertainty remains coherent when the interface invites a verdict, summary or estimate of agreement for the same item. Otherwise, a system can appear uncertainty-aware in one format while communicating a more resolved social signal in another.

## Methods

### Preregistration and analysis scope

The study was preregistered on OSF and implemented as a target-scoped computational audit using existing SCRUPLES source-community judgments and newly collected LLM API outputs. No new human participants were recruited. The analysis uses the frozen 50k target-scoped exports from `post_run/analysis_exports/50k/`.

Milestones were operational checks for monitoring and release discipline; inferential claims use the frozen 50k target-scoped analysis. Primary endpoint definitions and the low-consensus confirmatory subset were not revised after inspecting the final 50k results. Subsequent presentation changes did not alter the frozen numerical outputs.

The primary confirmatory endpoints were agreement surplus, distribution-agreement gap and sampling compression in low-consensus items. Diffuse/no-clear-consensus items were theoretically important secondary evidence and remained separate from the primary endpoint definition. Combined low-consensus and diffuse aggregates were used only as descriptive divided-item summaries where needed.

### Dataset, eligibility and label schema

The source dataset was SCRUPLES Anecdotes, a corpus of everyday ethical situations with source-community judgments about who was in the wrong [4]. Items were eligible when they had usable situation text, available source-community counts, canonical label mapping and no data-integrity issue preventing item-level analysis.

The canonical label schema was:

```text
author      = the author/narrator was in the wrong
other       = the other party was in the wrong
everybody   = everybody/both sides were in the wrong
nobody      = nobody was in the wrong
info        = not enough information/cannot tell
```

The `info` label was retained in the primary distributions because removing it would alter the observed disagreement structure.

### Source-community distributions, bins and item allocation

For each item, source-community vote counts were converted into primary source-community distributions using Jeffreys-smoothed Dirichlet posterior means with alpha = 0.5:

```text
theta_i | c_i ~ Dirichlet(c_i + 0.5)
primary_source_distribution_i = E[theta_i | c_i]
```

Robustness checks used raw proportions and Laplace smoothing with alpha = 1.0. Items were stratified by top-label support:

```text
high consensus:             top-label support >= 0.80
moderate consensus:         top-label support >= 0.65 and < 0.80
low consensus:              top-label support >= 0.50 and < 0.65
diffuse/no-clear-consensus: top-label support < 0.50
```

Item selection and label-order assignment used the milestone seed `20260615`. Eligible items were selected within disagreement bins to satisfy the frozen component allocations, and the released target manifests record the resulting item IDs. Beyond the eligibility rules above, target-list membership was governed by the frozen allocation plan rather than by inspection of model outputs. The core cross-format component used 350 high-consensus, 400 moderate-consensus, 750 low-consensus and 500 diffuse/no-clear-consensus items. The repeated-sampling, paraphrase-audit and normative-certainty components used component-specific target sets, with the paraphrase audit using a stratified subset for aggregate surface-form checks.

### Model roster and collection

The amended frozen roster contained five models: `claude-sonnet-4-6`, `deepseek/deepseek-v3.2`, `gpt-5.5`, `grok-4.3` and `qwen/qwen3.7-max`. Each model had 9,500 target calls. API routes and call windows are reported in Table 1a. Temperature was 0.0 for all exported rows. Top-p was blank/null in the final model roster. Provider and route fields record access provenance and are not analysed as cross-provider group effects. Exact model snapshot dates were not available in the local final roster and are not inferred beyond the recorded first and last call timestamps.

Full API-parameter fields, structured-output settings where applicable, maximum-token settings, retry-policy fields, reasoning-effort fields when present and collection timestamps are reported in the Supplementary Information and exported roster. Run manifests document the preregistered roster amendment and final completion/analysis provenance. The final analysis uses only the amended frozen five-model roster; the completion and analysis provenance records are `run_manifest_post50k_completion_v1.md` and `run_manifest_paper_analysis_50k_v1.md`.

### Prompt modes and request construction

Distribution mode asked each model to estimate the source-community probability distribution over the five labels. Descriptive verdict/agreement mode asked the model to choose one label and estimate the proportion of the source community that would agree with that choice. Repeated-sampling mode elicited ten single-label outputs for each repeated-sampling item-model pair. Normative-certainty prompts elicited a separate moral-certainty construct for secondary descriptive analysis.

Requests were stateless or fresh across prompt modes; the verdict/agreement prompt did not include the model's own distribution-mode answer. Prompt templates, schemas, label order, rendered prompt hashes, model IDs, API route, timestamps and decoding parameters were recorded in run records. Prompts requested structured final outputs and did not request chain-of-thought.

For repeated sampling, the ten outputs for each item-model pair were ten separate fresh calls under the sampling prompt. Label order was assigned separately for each prompt assignment using the recorded seed procedure, and the local label-order seed included `sample_id`. Invalid outputs were handled under the same parsing and validity rules as other components before entropy summaries were computed.

For paraphrase analyses, paraphrased versions of a stratified item subset were generated with the study's paraphrase-generation prompt mode and then evaluated with the paraphrased distribution and paraphrased descriptive verdict/agreement modes. These modes reused the same response schemas and validity rules as the corresponding original-item prompts. Because matched original-vs-paraphrase overlap was limited, the paraphrase component was treated as aggregate surface-form evidence rather than as a definitive paired robustness test.

Rendered prompt hashes were computed after inserting item text and randomized label order. Public materials describe prompt structure and release-safe templates, but do not reproduce rendered prompts containing source anecdotes.

### Parsing, validity and exclusions

Strict JSON schema enforcement was used where supported. Otherwise, JSON was extracted from model responses and validated against the required fields and ranges. Outputs were excluded from primary analyses if they were empty, invalid JSON, out of range, outside the validation tolerance for five-label probability sums, missing required fields, refusals, off-schema labels or terminal/API failures without a valid response.

For distribution-mode outputs, all five label probabilities had to be castable to floats and within the closed interval [0, 1]; violations were marked as probability-out-of-bounds errors. Probability vectors were accepted when their total fell within the inclusive interval [0.99, 1.01]. Accepted vectors whose totals differed from 1.0 by more than 1e-12 were renormalized to sum to one before downstream use. Vectors with totals below 0.99 or above 1.01 were marked as probability-sum errors and excluded from primary analyses. This tolerance was the hard-coded default in the collection-time parser; the final 50k exporter inherited stored parser validity statuses rather than revalidating probability sums with a second tolerance.

The final 50k run planned, attempted and completed 47,500 target calls. Run provenance recorded 0 API errors, 0 terminal failures, retry rate 0.0, executor status passed and database integrity ok. Primary-valid outputs were 47,432 of 47,500: 38,790 strict-schema outputs and 8,642 extracted-JSON outputs. Invalid status counts were 52 probability-out-of-bounds outputs, 10 probability-sum errors, 4 invalid-JSON outputs and 2 empty responses. Refusals and off-schema labels were zero. Repair fields were tracked, but `repair_attempted=0` and `repair_successful=0`; the final 50k analysis contained no repaired outputs. Validity by model and prompt mode is reported in Extended Data Table 1.

Strict-schema support varied across access routes. To address the possibility that extracted JSON outputs drove the effects, the robustness analyses included a strict-valid-only subset. That analysis preserved the direction of all three low-consensus endpoints and is reported in Results and the Supplementary Information.

### Endpoint definitions

For each verdict/agreement output, source-community support for the model's chosen label was computed from the smoothed source-community distribution. Agreement surplus was defined as:

```text
agreement_surplus =
    verdict_mode_estimated_source_community_agreement
    - source_support_for_model_chosen_label
```

For each item-model pair with both distribution-mode and verdict/agreement-mode outputs, distribution-agreement gap was defined as:

```text
distribution_agreement_gap =
    verdict_mode_estimated_agreement
    - distribution_mode_probability_for_same_verdict_label
```

This endpoint compares the same model, item and verdict-selected label across two elicitation formats. It tests output coherence, not whether the distribution-mode estimate perfectly matches the source-community distribution.

For repeated sampling, source-community entropy was compared with repeated-sample model entropy:

```text
sampling_compression =
    source_community_entropy
    - repeated_sample_model_entropy
```

Entropy values are reported on the five-label scale in bits. Positive values indicate that repeated forced-choice model outputs are more concentrated than the source-community distribution.

### Statistical inference

Primary inference used item-cluster bootstrap confidence intervals with 2,000 bootstrap iterations and seed `20260621`. For bin-specific estimates, item IDs were resampled with replacement within the bin and all relevant model/prompt rows for the resampled items were retained. For contrasts, each bootstrap replicate recomputed the relevant bin means and subtracted the high-consensus reference estimate. This procedure avoids treating item-model rows as fully independent observations.

The three low-consensus primary endpoints were tested using one-sided positive-effect bootstrap P values, Holm-adjusted across the three endpoints. Because 2,000 bootstrap iterations impose a finite floor, adjusted P values are reported as Holm-adjusted P = 0.0015.

Contrasts comparing low-consensus or diffuse items with high-consensus items used the same bootstrap framework and support the claim that over-resolution is larger in divided items. Mixed-effects model-ready rows are provided as transparency files, but no mixed-effects model result is reported here.

### Robustness and secondary analyses

Robustness analyses addressed parsing/schema validity, source-community distribution construction, annotation and `info` sensitivity, distribution-mode non-degeneracy and surface-form sensitivity. These included strict-valid-only outputs; raw, Jeffreys-smoothed and Laplace-smoothed source-community distributions; high-annotation-only subsets; exclusion of `info`-majority items; exclusion of high-`info` items; distribution-quality diagnostics; non-API baselines; and aggregate paraphrase analyses.

Distribution-quality diagnostics included Jensen-Shannon divergence, total variation distance, entropy and Brier summaries, with uniform, global-base-rate and source-majority-oracle baselines. These diagnostics were used to assess whether distribution-mode outputs were non-degenerate and item-sensitive, not to claim perfect distribution calibration.

Normative certainty was analysed only as a secondary descriptive construct and is not equivalent to estimated source-community agreement. No formal recognition audit was run for the final 50k analysis, and contamination was not directly measured.

## Data availability

Code, run manifests and derived analysis files are available through the OSF project (`https://osf.io/rwhax/overview`), OSF registration home (`https://osf.io/rwhax/registrations`), GitHub repository (`https://github.com/pbriggs/format-induced-moral-overresolution`), the post-50k execution/completion archive (`https://doi.org/10.5281/zenodo.20786461`) and the paper-analysis archive (`https://doi.org/10.5281/zenodo.20789625`). The corresponding release tags are `post-50k-completion-v1` and `paper-analysis-50k-v1`.

Public archives provide derived metrics sufficient to verify the reported analyses. Public derived materials include prompt templates, schema files, run manifests with sensitive details removed where needed, analysis code, endpoint tables, bootstrap confidence intervals, validity summaries, robustness analyses, paraphrase-audit summaries, distribution-quality diagnostics, manuscript-table CSVs, figure-ready CSVs and rendered figures. The repository license is CC0 1.0 Universal unless superseded by OSF project settings; redistribution of dataset and model-output material remains subject to third-party terms, privacy considerations and institutional review requirements.

The source SCRUPLES data should be accessed through the original dataset source subject to its terms [4]. Raw SCRUPLES anecdotes, rendered prompts containing anecdote text, raw provider responses, full call ledgers and SQLite data are not redistributed in unrestricted form where doing so could conflict with SCRUPLES/AllenAI terms, model-provider terms, privacy/sensitivity considerations or institutional review requirements. Restricted verification materials can be provided to editors or reviewers upon reasonable request under appropriate non-redistribution conditions and subject to applicable third-party terms.

## Code availability

Analysis code and figure-generation scripts are available at `https://github.com/pbriggs/format-induced-moral-overresolution` and archived under release tag `paper-analysis-50k-v1` with DOI `https://doi.org/10.5281/zenodo.20789625`. The repository includes preprocessing code, prompt templates, schema files, target-scoped export scripts, bootstrap procedures, manuscript tables and figure-rendering scripts. API credentials and provider-specific secrets are not included.

The final 50k analysis can be regenerated locally from the completed run database, when available in an authorized local or reviewer environment, with the offline analysis commands:

```powershell
$env:PYTHONPATH='src'
$env:PYTHONDONTWRITEBYTECODE='1'
python -m analysis.final_50k_exports --bootstrap-iterations 2000
python -m analysis.render_final_figures
```

These commands regenerate analysis tables and figures from completed-run data; they do not make new provider calls.

Full local setup instructions, including dependency installation, SCRUPLES data placement and environment variables for optional provider-call reproduction, are provided in `README.md`, `.env.example` and `docs/DATA_SETUP.md`. Optional provider-call reruns require the user's own provider credentials and may produce new model outputs rather than exactly reproducing the frozen 50k collection.

## AI assistance disclosure

The author used AI tools for editorial drafting support, code/checklist support, manuscript organization and revision planning. The author reviewed, verified and takes responsibility for all analyses, claims, interpretations and final manuscript text. No AI tool is listed as an author.

## Ethics and human-subjects statement

No new human participants were recruited for this computational audit, and the author did not interact with human participants. The study analysed an existing public dataset of source-community judgments and newly collected model outputs. No formal institutional review board or ethics-committee determination was obtained for this independent computational study. Raw anecdotes, rendered prompts and raw provider responses are treated cautiously because they may contain sensitive interpersonal content and may be subject to dataset terms, provider terms and privacy considerations.

## Funding

The author received no external funding for this work. API and computing costs were paid personally by the author.

## Competing interests

The author declares no competing interests.

## Author contributions

P.B. conceived the study, designed the protocol, implemented the data-collection and analysis pipeline, conducted the analyses, interpreted the results, prepared the figures and tables, and wrote and revised the manuscript.

## Acknowledgements

The author thanks Nicholas Lourie, Ronan Le Bras and Yejin Choi, and the Allen Institute for AI, for releasing the SCRUPLES dataset and code. The source-community judgments analysed here derive from community members' judgments in the SCRUPLES Anecdotes corpus; they are treated as source-community reference distributions, not as broader normative standards.

## References

1. Jiang, L. et al. Investigating machine moral judgement through the Delphi experiment. *Nature Machine Intelligence* **7**, 145-160 (2025). https://doi.org/10.1038/s42256-024-00969-6
2. Steyvers, M. et al. What large language models know and what people think they know. *Nature Machine Intelligence* **7**, 221-231 (2025). https://doi.org/10.1038/s42256-024-00976-7
3. Kumaran, D. et al. Competing biases underlie overconfidence and underconfidence in LLMs. *Nature Machine Intelligence* **8**, 614-627 (2026). https://doi.org/10.1038/s42256-026-01217-9
4. Lourie, N., Le Bras, R. & Choi, Y. SCRUPLES: A corpus of community ethical judgments on 32,000 real-life anecdotes. *Proceedings of the AAAI Conference on Artificial Intelligence* **35**, 13470-13479 (2021). https://doi.org/10.1609/aaai.v35i15.17589
5. Abdulhai, M., Serapio-Garcia, G., Crepy, C., Valter, D., Canny, J. & Jaques, N. Moral foundations of large language models. arXiv:2310.15337 (2023). https://arxiv.org/abs/2310.15337
6. Takemoto, K. The moral machine experiment on large language models. *Royal Society Open Science* **11**, 231393 (2024). https://doi.org/10.1098/rsos.231393
7. Zaim bin Ahmad, M. S. & Takemoto, K. Large-scale moral machine experiment on large language models. *PLoS One* **20**, e0322776 (2025). https://doi.org/10.1371/journal.pone.0322776

## Main display items

**Fig. 1 | Study design for testing uncertainty transfer across prompt formats.** SCRUPLES source-community vote distributions were grouped by source-community disagreement bin and evaluated in matched item-model comparisons across prompt formats. Distribution mode elicited five-label source-community probability estimates; descriptive verdict/agreement mode elicited a single label and an estimated source-community agreement value; repeated sampling elicited repeated single-label outputs for the same item-model pair. The primary endpoints compare source-community support, model-estimated distribution probabilities, verdict agreement estimates and repeated-sample entropy. Paraphrase-audit and normative-certainty components are supporting and secondary components rather than primary endpoints. This schematic is a design overview; quantitative results are reported in Figs. 2–4 and Table 2.

**Fig. 2 | Verdict prompts inflate perceived source-community agreement.** Agreement surplus by source-community disagreement bin and model. Bars show aggregate means across the evaluated models and overlaid points show model-level means. Positive values mean verdict-mode estimated agreement exceeds observed source-community support for the model's chosen label. In the low-consensus primary subset, mean agreement surplus was 0.370931 (95% item-cluster bootstrap CI, 0.361206-0.381114; n = 3,749 item-model rows; Holm-adjusted P = 0.0015).

**Fig. 3 | Verdict prompts overstate agreement relative to the model's own distribution.** Distribution-agreement gap by source-community disagreement bin and model. Bars show aggregate means across the evaluated models and overlaid points show model-level means. Positive values mean the verdict-mode agreement estimate exceeds the same model's distribution-mode probability for the verdict label. In the low-consensus primary subset, mean distribution-agreement gap was 0.232687 (95% item-cluster bootstrap CI, 0.224387-0.241341; n = 3,736 item-model rows; Holm-adjusted P = 0.0015).

**Fig. 4 | Repeated model labels compress source-community disagreement.** Sampling compression by source-community disagreement bin and model. Bars show aggregate means across the evaluated models and overlaid points show model-level means for source-community entropy minus repeated-sample model entropy on the five-label scale in bits. Positive values mean repeated model labels are more concentrated than source-community judgments. In the low-consensus primary subset, mean sampling compression was 1.264638 bits (95% item-cluster bootstrap CI, 1.218425-1.309054; n = 750 item-model summaries; Holm-adjusted P = 0.0015).

**Table 1 | Frozen model roster and target allocation.** The roster records the evaluated model IDs, access routes, collection windows and target calls. Provider/route fields are provenance fields rather than provider-family or model-family comparisons. The allocation table reports the frozen study components used for the target-scoped analysis.

**Table 1a | Frozen model roster.**

| Model ID | Provider/route | API route | First call UTC | Last call UTC | Target calls |
|---|---|---|---|---|---:|
| `claude-sonnet-4-6` | Anthropic | `https://api.anthropic.com/v1/messages` | 2026-06-16T22:25:08.996871+00:00 | 2026-06-21T15:33:15.162406+00:00 | 9,500 |
| `deepseek/deepseek-v3.2` | OpenRouter-compatible route | `https://openrouter.ai/api/v1/chat/completions` | 2026-06-16T22:25:04.892615+00:00 | 2026-06-21T15:33:02.923140+00:00 | 9,500 |
| `gpt-5.5` | OpenAI | `https://api.openai.com/v1/responses` | 2026-06-16T22:25:12.406257+00:00 | 2026-06-21T15:33:16.432159+00:00 | 9,500 |
| `grok-4.3` | xAI | `https://api.x.ai/v1/responses` | 2026-06-17T17:55:15.846572+00:00 | 2026-06-21T15:32:59.334062+00:00 | 9,500 |
| `qwen/qwen3.7-max` | OpenRouter-compatible route | `https://openrouter.ai/api/v1/chat/completions` | 2026-06-16T22:25:15.735026+00:00 | 2026-06-21T15:33:13.991444+00:00 | 9,500 |

Temperature was 0.0 for all exported model-roster rows; top-p was blank/null. Provider/route fields record access provenance and are not analysed as cross-provider group effects; model snapshot dates are not inferred beyond the recorded first and last call timestamps. Total target calls were 47,500.

**Table 1b | Target allocation by study component.**

| Component | Unique items | Target calls | Manuscript role |
|---|---:|---:|---|
| Core cross-format | 2,000 | 20,000 | H1a and H1b |
| Repeated sampling | 400 | 20,000 | H1c |
| Paraphrase audit | 250 | 2,500 | Aggregate surface-form robustness |
| Normative certainty | 1,000 | 5,000 | Secondary descriptive analysis |
| Total |  | 47,500 | Frozen 50k target-scoped analysis |

**Table 2 | Primary endpoint estimates, contrasts, confidence intervals and adjusted tests.**

| Endpoint | Low-consensus primary mean (95% CI) | Holm-adjusted P | Diffuse secondary mean (95% CI) | High-consensus reference mean (95% CI) | Low–high contrast (95% CI) |
|---|---:|---:|---:|---:|---:|
| Agreement surplus | 0.370931 (0.361206-0.381114) | 0.0015 | 0.435619 (0.427337-0.444341) | 0.169409 (0.145651-0.194624) | 0.201523 (0.174835-0.228568) |
| Distribution-agreement gap | 0.232687 (0.224387-0.241341) | 0.0015 | 0.226556 (0.216740-0.237164) | 0.182842 (0.169762-0.196217) | 0.049845 (0.033774-0.065329) |
| Sampling compression, bits | 1.264638 (1.218425-1.309054) | 0.0015 | 1.507379 (1.452200-1.562768) | 0.563708 (0.495005-0.633547) | 0.700930 (0.618287-0.783543) |

Estimates use the frozen 50k target-scoped analysis. Low-consensus values are the primary confirmatory estimates; diffuse/no-clear-consensus values are secondary evidence and remain separate from the primary endpoint definition. Confidence intervals are item-cluster bootstrap intervals with 2,000 bootstrap iterations. P values are one-sided positive-effect bootstrap P values, Holm-adjusted across the three low-consensus primary endpoints; with 2,000 bootstrap iterations, Holm-adjusted P values are reported at the finite bootstrap floor of 0.0015.

## Extended Data and Supplementary Information

The Supplementary Information provides reviewer-facing methodological detail, source-data references and release-safe reproducibility information for the Extended Data figures, Extended Data table and Supplementary Tables. Source-data paths for the items below are listed in the Supplementary Information rather than repeated in full in the main manuscript.

**Extended Data Fig. 1 | Distribution-quality diagnostics.** Diagnostic distances and entropy summaries by source-community disagreement bin and model show that distribution-mode outputs varied by item/bin and were not merely uniform or fixed base-rate responses. This is a diagnostic support analysis, not a distribution-prediction benchmark.

**Extended Data Fig. 2 | Aggregate paraphrase-audit effects.** Aggregate paraphrase-audit agreement surplus and distribution-agreement gap estimates preserve the direction of the main effects. The figure should be interpreted with the limited matched-coverage caveat stated in the Results and Supplementary Information.

**Extended Data Fig. 3 | Validity by model and prompt mode.** Primary-valid output rates by model and prompt mode show high validity and limited invalid outputs in the frozen 50k target-scoped analysis.

**Extended Data Table 1 | Validity and exclusion summary.** Validity by model/mode, invalid status counts, minimum model/mode validity, refusal count, off-schema count, API errors, terminal failures and repair fields.

**Supplementary Table 1 | Full model roster, API parameters, model-level endpoints and leave-one-model-out summaries.** Supports model provenance, API-parameter reporting and cross-model consistency checks without making provider-family or model-family claims.

**Supplementary Table 2 | Source-community distribution smoothing robustness.** Reports raw-proportion, Jeffreys-smoothed and Laplace-smoothed source-community distribution sensitivity checks.

**Supplementary Table 3 | Annotation and `info` robustness.** Reports high-annotation-only, `info`-majority exclusion and high-`info` exclusion checks.

**Supplementary Table 4 | Paraphrase audit.** Reports paraphrase target calls, valid outputs, aggregate effects, confidence intervals, chosen-label stability and the matched-coverage caveat.

**Supplementary Table 5 | Distribution quality and baselines.** Reports distribution-quality diagnostics and uniform, global-base-rate and source-majority-oracle baselines.

**Supplementary Table 6 | Normative certainty.** Reports the secondary moral-certainty construct; moral certainty is not equivalent to estimated source-community agreement.

**Supplementary Table 7 | Validity and exclusions.** Reports validity and exclusion summaries and cross-references Extended Data Table 1.

**Supplementary Table 8 | Model-ready secondary rows.** Provides model-ready secondary rows as transparency files; these files do not contain reported mixed-effects model results.

**Supplementary Notes.** The Supplementary Information provides supporting methodological detail for prompt and schema reproducibility, source-community preprocessing, item allocation, model provenance, parsing and exclusions, endpoint definitions, bootstrap inference, robustness checks, paraphrase limitations, distribution-quality diagnostics, normative-certainty secondary analysis and public/restricted materials boundaries.
