# Verdict-style prompts induce moral over-resolution in large language models

**Author:** Paul Briggs  
**Affiliation:** Independent researcher, Los Angeles, CA, USA  
**Corresponding author:** Paul Briggs, p.ivan.briggs@gmail.com  
**ORCID:** https://orcid.org/0009-0002-9951-8661

## Abstract

Large language models (LLMs) are increasingly asked to make ethical judgments about blame, responsibility and fairness in interpersonal situations. Some cases draw broad agreement; in others, human responses spread across answers. A reliable system should not make cases without a clear majority sound like consensus. Here we test whether LLMs preserve measured disagreement across two forms of answer: estimates of how people voted and a single verdict with estimated agreement. In a preregistered audit, five LLMs evaluated ethical situations with recorded human votes on who was in the wrong. Each model estimated the vote distribution, then chose one answer and estimated how many people would agree. Low-consensus cases were the confirmatory test. When models chose one answer, they overstated agreement: their estimates exceeded both the human vote share and their own distribution estimate for that answer. When models repeatedly answered the same low-consensus cases, their answers covered a narrower range than the human responses for those cases. These findings identify a format-specific reliability failure: LLMs can express measured human disagreement as distributions, but when asked for a verdict, they can overstate agreement and compress disagreement.


LLM users often ask for single judgments when reference judgments are divided. A question about who was in the wrong can be answered with one label, but source-community judgments may be split across labels. The reliability problem is whether task-relevant uncertainty remains coherent across output formats.

Moral judgment is a useful stress test because source-community disagreement is common, measurable and consequential. Some everyday cases draw a clear majority in the source community; others divide judgments across several answers.

Consider a routine interpersonal dispute in which source-community judgments could divide among the narrator, the other party and both parties. A distributional answer may assign probability mass across those labels. Asked for a verdict and agreement estimate, the same model may choose one label and estimate high source-community agreement. The failure is the cross-format shift: one format communicates division, whereas another makes the selected label sound more agreed upon.

Prior work has examined whether models predict moral judgments, agree with majority labels or show calibrated confidence [1-7]. This study instead asks whether uncertainty about a source-community judgment distribution remains coherent across output formats. Unlike standard calibration, it compares matched model outputs for the same items under distributional and verdict-style elicitation.

We call the tested failure mode **format-induced moral over-resolution**: a format-specific reliability failure in which a divided source-community judgment distribution becomes a more resolved agreement signal when the model is asked for a verdict. We test that shift with three matched-item endpoints. They ask whether the format shift inflates apparent agreement relative to source-community support, makes reported agreement exceed the same model's distribution-mode probability for the selected label, or compresses repeated forced-choice outputs. These endpoints test uncertainty transfer; they do not require perfect distribution calibration.

The empirical target is deliberately narrow. We use SCRUPLES Anecdotes because it provides everyday ethical situations with source-community judgments about who was in the wrong [4]. The phrase "source community" refers to the annotator/judgment population represented in SCRUPLES. These judgments are reference distributions from that data-generating process, not authoritative moral labels, universal moral norms, representative population estimates or deployment-ready normative standards. In this preregistered audit, five LLMs evaluated matched SCRUPLES items in distribution mode, descriptive verdict/agreement mode and repeated-sampling mode (Fig. 1). Low-consensus items were the primary confirmatory subset; diffuse/no-clear-consensus items were analysed separately as secondary evidence; high-consensus items served as a reference condition.

The contribution is threefold. First, the study operationalizes cross-format uncertainty transfer for source-community moral judgments. Second, it defines matched-item endpoints for surplus agreement relative to the source-community distribution, within-model incoherence across output formats, and compression in repeated forced-choice outputs. Third, it shows in a preregistered five-model audit that verdict-style elicitation inflates apparent agreement and compresses disagreement, with the clearest reliability concern when source-community judgments are divided.

## Results


### Endpoint logic and target set

We tested three ways verdict-style outputs can over-resolve source-community disagreement. First, a selected label can be accompanied by an estimate of source-community agreement that exceeds its source-community support. Second, the same model can report higher estimated source-community agreement in verdict/agreement mode than the probability it assigns to the same item and verdict-selected label in distribution mode. Third, repeated forced-choice outputs under the study protocol can be more concentrated on the five-label scale than the source-community judgment distribution.

These endpoints were evaluated with matched item-model comparisons. Low-consensus items were the confirmatory subset: cases with a majority label but substantial remaining source-community disagreement. Diffuse/no-clear-consensus items were analysed separately as secondary evidence, and high-consensus items served as a reference condition. This hierarchy keeps the primary test distinct while each endpoint compares matched item-model outputs rather than unrelated prompts.

Table 1 and Methods report the model roster, component allocation and study scale, including 47,500 target calls and 47,432 primary-valid outputs.


### Verdict prompts inflate apparent agreement

We first tested whether verdict-style elicitation makes the selected label sound more widely supported by the source community. Agreement surplus compares the model's verdict-mode estimate of source-community agreement with source-community support for the selected label.

In the low-consensus primary subset, agreement surplus was 0.370931 (95% CI, 0.361206-0.381114; Holm-adjusted P = 0.0015; n = 3,749 item-model rows; Fig. 2 and Table 2). Thus, verdict-mode agreement estimates exceeded source-community support for the chosen label by approximately 37 percentage points. The accompanying agreement estimate can make the selected label appear more supported than the source-community distribution warrants; that is the reliability concern.

The same pattern appeared outside the primary subset. Diffuse/no-clear-consensus items showed a larger secondary estimate: agreement surplus was 0.435619 (95% CI, 0.427337-0.444341; n = 2,500). High-consensus items also showed positive agreement surplus, 0.169409 (95% CI, 0.145651-0.194624; n = 1,750). The low-consensus-minus-high-consensus contrast was 0.201523 (95% CI, 0.174835-0.228568). High-consensus items therefore served as a positive reference condition, while the larger low-consensus surplus shows greater reliability concern where source-community agreement was weaker.

### Verdict agreement exceeds the model's distributional estimate

The second endpoint tested the central uncertainty-transfer question within the model's own outputs. For each matched comparison, the model, item and verdict-selected label were fixed; only the elicitation format changed. A positive distribution-agreement gap means the verdict/agreement format reported more source-community agreement for the selected label than the same model assigned to that label in distribution mode.

This comparison tests cross-format output coherence: whether two answers from the same model communicate compatible levels of source-community agreement for the same item-label pairing. Perfect calibration of the distribution-mode estimate to the SCRUPLES source-community distribution is not required.

In the low-consensus primary subset, the distribution-agreement gap was 0.232687 (95% CI, 0.224387-0.241341; Holm-adjusted P = 0.0015; n = 3,736; Fig. 3 and Table 2). A positive gap means that, for the same item and chosen label, verdict/agreement mode reported more agreement than the model's own distribution-mode probability supported.

Diffuse items showed a secondary gap of 0.226556 (95% CI, 0.216740-0.237164; n = 2,494). High-consensus items also showed a positive gap of 0.182842 (95% CI, 0.169762-0.196217; n = 1,745). The low-consensus-minus-high-consensus contrast was 0.049845 (95% CI, 0.033774-0.065329). Because this endpoint is internal to the model's outputs, H1b anchors the reliability claim: the same model can communicate different levels of apparent agreement about the same item-label pairing depending on output format.

### Repeated forced-choice outputs compress source-community disagreement

The first two endpoints concern explicit agreement estimates. The third asked whether compression also appeared when models repeatedly chose a label. Sampling compression was source-community entropy minus the entropy of repeated forced-choice model outputs on the five-label scale. Positive values mean repeated model labels occupied a narrower effective label range than source-community votes for the same items.

In the low-consensus primary subset, sampling compression was 1.264638 bits (95% CI, 1.218425-1.309054; Holm-adjusted P = 0.0015; n = 750 item-model summaries; Fig. 4 and Table 2). Diffuse items showed stronger secondary compression, 1.507379 bits (95% CI, 1.452200-1.562768; n = 500). High-consensus items also showed positive compression, 0.563708 bits (95% CI, 0.495005-0.633547; n = 350). The low-consensus-minus-high-consensus contrast was 0.700930 bits (95% CI, 0.618287-0.783543).

This endpoint extends the evidence beyond stated agreement. Under the study's repeated forced-choice protocol, outputs across fresh calls were more concentrated than source-community judgments, with larger compression in the low-consensus primary subset than in the high-consensus reference condition. The endpoint should not be read as stochastic sampling from an internal model distribution; it measures diversity across repeated fresh calls under the recorded prompt and label-order randomization protocol.

### Pattern across models and output validity

The aggregate pattern appeared across the evaluated models. Each evaluated model showed positive low-consensus agreement surplus, positive low-consensus distribution-agreement gap and positive low-consensus sampling compression. Model-level low-consensus agreement surplus ranged from 0.326454 to 0.445325. Low-consensus distribution-agreement gaps ranged from 0.215187 to 0.271943. Low-consensus sampling compression ranged from 0.920001 to 1.408416. Leave-one-model-out summaries preserved the direction of the aggregate pattern for all three endpoints. These summaries support a shared behavioural pattern across the evaluated roster, without supporting inferential comparisons by provider, route or model lineage.

Output validity was also high across the audit, limiting concern that the pattern reflected broad parsing failure. Of 47,500 outputs, 47,432 were primary-valid (validity rate = 0.998568), comprising 38,790 strict-schema outputs and 8,642 extracted-JSON outputs. The minimum model/mode primary-valid rate was 0.969. Invalid statuses were 52 probability-out-of-bounds outputs, 10 probability-sum errors, 4 invalid-JSON outputs and 2 empty responses. Refusals and off-schema labels were both zero. Repair fields were tracked; `repair_attempted` and `repair_successful` were both zero, so no repaired outputs entered the final analysis. Validity by model and prompt mode is summarized in Extended Data Fig. 3 and Extended Data Table 1.

### Robustness and diagnostics

Robustness checks asked whether the endpoint pattern could be attributed to data handling, reference-distribution construction, item composition, distribution-mode degeneracy or prompt surface form. They support the three endpoint results above as robustness checks; the primary endpoints remain the three low-consensus tests.

Parsing and schema heterogeneity were addressed with a strict-valid-only analysis. This restricted the data to outputs that satisfied the strict schema, testing whether extracted-JSON outputs drove the endpoint pattern. The direction of all three low-consensus endpoints was preserved: agreement surplus 0.376030, distribution-agreement gap 0.223867 and sampling compression 1.268188.

The source-community reference distribution was also checked against alternative constructions from SCRUPLES vote counts. Low-consensus endpoint effects were recomputed using raw proportions, Jeffreys smoothing and Laplace smoothing, and positive low-consensus effects were preserved across these constructions. This sensitivity analysis concerns how source-community vote counts were converted into reference distributions; it is not a test of whether distribution-mode model outputs were calibrated to those distributions.

Item-composition checks asked whether the pattern depended on annotation density or on the `info` label. The directional endpoint pattern was preserved in high-annotation-only analyses, after excluding `info`-majority items and after excluding high-`info` items.

Distribution-mode diagnostics assessed non-degeneracy and item sensitivity in distributional outputs. Source entropy was higher in diffuse items (mean 1.955481 bits) than in high-consensus items (0.823596 bits). Model distribution entropy also varied by bin, with higher entropy in diffuse (1.515785 bits) and low-consensus items (1.476755 bits) than in high-consensus items (1.200675 bits). These diagnostics, summarized in Extended Data Fig. 1, support non-degeneracy and item sensitivity. They are support analyses, not a distribution-prediction benchmark and not evidence that distribution-mode estimates were perfectly calibrated to source-community distributions.

The paraphrase audit addressed surface-form sensitivity, with limitations described below. The audit provided aggregate surface-form evidence in paraphrased items (Extended Data Fig. 2), with 2,500 target calls and 2,495 valid outputs. In paraphrased low-consensus items, agreement surplus was 0.366821 (95% CI, 0.334632-0.397075) and the distribution-agreement gap was 0.212124 (95% CI, 0.192023-0.231651). In paraphrased diffuse items, the corresponding estimates were 0.418159 (95% CI, 0.396906-0.443057) and 0.200502 (95% CI, 0.174963-0.225410).

Within the limited matched original-vs-paraphrase overlap, chosen-label stability was 0.655 in low-consensus rows and 0.467 in diffuse rows. Because matched original-vs-paraphrase coverage was limited (29 low-consensus rows and 15 diffuse rows), these results should be read as aggregate surface-form evidence rather than a definitive paired original-vs-paraphrase test. Contamination was not directly measured.


## Discussion

This study identifies output format as a reliability risk when reference judgments are divided. The reliability risk is that uncertainty available in one elicitation format can be sharpened, lost or made incoherent across formats when the interface asks for a verdict. In the evaluated models under the tested prompt formats, distributional prompting elicited non-degenerate, item-sensitive estimates over source-community labels, whereas verdict-style elicitation reported stronger apparent source-community agreement and repeated forced-choice outputs compressed disagreement.

The result concerns uncertainty transfer and output reliability. SCRUPLES provides source-community judgments from a particular data-generating process. They are source-community reference distributions from that process, not moral truth, universal norms, representative population estimates or deployment-ready normative standards. When the reference distribution is divided, a verdict-style prompt can make the output appear more settled than either the source-community distribution or the model's own distribution-mode estimate supports.

This distinction matters for evaluation and benchmark design. Majority-label accuracy can reward a model for selecting the most common label while missing whether it communicates the disagreement around that label. A one-format uncertainty test can miss the same problem: a model may produce a distribution when explicitly prompted yet communicate a conflicting level of agreement when asked for a verdict or agreement estimate on the same case. The within-model comparison is especially important because it holds the model, item and verdict-selected label fixed while changing the elicitation format. Evaluations of LLM reliability should therefore test cross-format coherence alongside majority-label performance, confidence calibration and distribution-mode-only uncertainty tests.

The findings also matter for interface design. Users often ask for verdicts in settings where source-community disagreement is relevant to the task. In such settings, distributional interfaces, explicit disagreement summaries and checks on verdict/agreement outputs may reduce the risk that a divided source-community reference distribution is turned into an overconfident agreement signal. The relevant design constraint is that verdict interfaces should not communicate stronger source-community agreement than the reference distribution or the model's own distributional answer supports.

Several limitations bound the interpretation. The study uses one source-community dataset, five evaluated models and a finite set of prompt templates, so the findings are bounded by the tested dataset, models and prompt formats. The source community is not a universal or representative population sample.

Contamination was not directly measured. The paraphrase audit addresses surface-form sensitivity rather than training-set membership, and the small matched original-vs-paraphrase overlap means that paraphrase results should be read as aggregate surface-form evidence only. Although item familiarity could affect absolute label probabilities, it would not by itself explain the within-item, same-model pattern in which a model's verdict-mode agreement estimate exceeds its independently elicited distribution-mode probability for the same item and label. Finally, this is a model-output reliability audit rather than a user study; whether cross-format differences affect users' beliefs about social consensus, confidence or decision-making remains an empirical question.

The implication for model-output reliability is concrete: uncertainty should be evaluated in the formats where users encounter model outputs. An evaluation should ask whether a model can state a distribution when explicitly prompted and whether reported uncertainty remains coherent when the interface invites a verdict, summary or estimate of agreement for the same item. Otherwise, the same model can appear uncertainty-aware in one format while communicating a more resolved agreement signal in another.

## Methods

### Preregistration and analysis scope

The study was preregistered on OSF as a target-scoped computational audit. It used existing SCRUPLES source-community judgments and newly collected LLM API outputs; no new human participants were recruited. The analysis uses the frozen 50k target-scoped exports from `post_run/analysis_exports/50k/`.

Milestones were operational checks for monitoring and release discipline. Inferential claims use the frozen 50k target-scoped analysis. Primary endpoint definitions and the low-consensus confirmatory subset remained fixed after inspection of the final 50k results, and subsequent presentation changes did not alter the frozen numerical outputs.

The primary confirmatory endpoints were agreement surplus, distribution-agreement gap and sampling compression in low-consensus items. Diffuse/no-clear-consensus items were theoretically important secondary evidence and remained separate from the primary endpoint definition. Combined low-consensus and diffuse aggregates were used only as descriptive divided-item summaries where needed.

### Dataset, eligibility and label schema

The source dataset was SCRUPLES Anecdotes, a corpus of everyday ethical situations with source-community judgments about who was in the wrong [4]. Items were eligible when they had usable situation text, available source-community counts, canonical label mapping and no data-integrity issue preventing item-level analysis. These judgments were treated as reference distributions from the SCRUPLES data-generating process, not as moral truth, universal norms, representative population estimates or deployment-ready normative labels.

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

For each item, source-community vote counts were converted to primary source-community distributions using Jeffreys-smoothed Dirichlet posterior means with alpha = 0.5:

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

Item selection and label-order assignment used the milestone seed `20260615`. Eligible items were selected within disagreement bins to satisfy the frozen component allocations, and the released target manifests record the resulting item IDs. Beyond the eligibility rules above, target-list membership was governed by the frozen allocation plan rather than by inspection of model outputs.

Low-consensus items were the primary confirmatory subset, diffuse/no-clear-consensus items remained secondary, and high-consensus items served as the reference condition.

The core cross-format component used 350 high-consensus, 400 moderate-consensus, 750 low-consensus and 500 diffuse/no-clear-consensus items. The repeated-sampling, paraphrase-audit and normative-certainty components used component-specific target sets. The paraphrase audit used a stratified subset for aggregate surface-form checks.

### Model roster and collection

The amended frozen roster contained five models: `claude-sonnet-4-6`, `deepseek/deepseek-v3.2`, `gpt-5.5`, `grok-4.3` and `qwen/qwen3.7-max`. Each model had 9,500 target calls. API routes and call windows are reported in Table 1a.

Temperature was 0.0 for all exported rows. Top-p was blank/null in the final model roster. Provider and route fields record access provenance and are not analysed as cross-provider group effects. Exact model snapshot dates were not available in the local final roster and are not inferred beyond the recorded first and last call timestamps.

Full API-parameter fields, structured-output settings where applicable, maximum-token settings, retry-policy fields, reasoning-effort fields when present and collection timestamps are reported in the Supplementary Information and exported roster. The Supplementary Information and run manifests document the roster amendment and final completion/analysis provenance. The final analysis uses only the amended frozen five-model roster.

### Prompt modes and request construction

Distribution mode asked each model to estimate the source-community probability distribution over the five labels. Descriptive verdict/agreement mode asked the model to choose one label and estimate the proportion of source-community judges who would agree with that choice. Repeated-sampling mode elicited ten single-label forced-choice outputs for each repeated-sampling item-model pair. Normative-certainty prompts elicited a separate moral-certainty construct for secondary descriptive analysis.

Requests were fresh and stateless across prompt modes. The verdict/agreement prompt did not include the model's own distribution-mode answer. Prompt templates, schemas, label order, rendered prompt hashes, model IDs, API route, timestamps and decoding parameters were recorded in run records. Prompts requested structured final outputs and did not request chain-of-thought.

For repeated sampling, the ten outputs for each item-model pair were ten separate fresh calls under the sampling prompt. Label order was assigned separately for each prompt assignment using the recorded seed procedure, and the local label-order seed included `sample_id`. Invalid outputs were handled under the same parsing and validity rules as other components before entropy summaries were computed.

The sampling-compression endpoint measures diversity across repeated forced-choice outputs under the recorded prompt and label-order randomization protocol, not stochastic sampling from an internal model distribution.

For paraphrase analyses, paraphrased versions of a stratified item subset were generated with the study's paraphrase-generation prompt mode. They were then evaluated with the paraphrased distribution and paraphrased descriptive verdict/agreement modes, which reused the same response schemas and validity rules as the corresponding original-item prompts. Because matched original-vs-paraphrase overlap was limited, the paraphrase component was treated as aggregate surface-form evidence rather than as a definitive paired original-vs-paraphrase test. This component did not test training-set membership; contamination was not directly measured.

Rendered prompt hashes were computed after inserting item text and randomized label order. Public materials describe prompt structure and release-safe templates while excluding rendered prompts containing source anecdotes.

### Parsing, validity and exclusions

Strict JSON schema enforcement was used where supported. Otherwise, JSON was extracted from model responses and validated against the required fields and ranges. Outputs were excluded from primary analyses if the response was empty, invalid JSON, out of range, outside the validation tolerance for five-label probability sums, missing required fields, a refusal, an off-schema label or a terminal/API failure without a valid response.

For distribution-mode outputs, all five label probabilities had to be castable to floats and within the closed interval [0, 1]. Values outside that interval were marked as `probability_out_of_bounds`.

Probability vectors were accepted when their total fell within the inclusive interval [0.99, 1.01]. Accepted vectors whose totals differed from 1.0 by more than 1e-12 were renormalized to sum to one before downstream use. The 1e-12 threshold was only the renormalization threshold, not the exclusion tolerance. Vectors with totals below 0.99 or above 1.01 were marked as `probability_sum_error` and excluded from primary analyses. This tolerance was the hard-coded default in the collection-time parser; the final 50k exporter inherited stored parser validity statuses rather than revalidating probability sums with a second tolerance.

The final 50k run planned, attempted and completed 47,500 target calls. Run provenance recorded 0 API errors, 0 terminal failures, retry rate 0.0, executor status passed and database integrity ok.

Primary-valid outputs were 47,432 of 47,500: 38,790 strict-schema outputs and 8,642 extracted-JSON outputs. Invalid status counts were 52 `probability_out_of_bounds` outputs, 10 `probability_sum_error` outputs, 4 invalid-JSON outputs and 2 empty responses. Refusals and off-schema labels were zero. Repair fields were tracked, but `repair_attempted=0` and `repair_successful=0`; the final 50k analysis contained no repaired outputs. Validity by model and prompt mode is reported in Extended Data Table 1.

Strict-schema support varied across access routes. To address the possibility that extracted-JSON outputs drove the endpoint pattern, the robustness analyses included a strict-valid-only subset. That analysis preserved the direction of all three low-consensus endpoints and is reported in Results and the Supplementary Information.

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

This endpoint compares the same model, item and verdict-selected label across two elicitation formats. It tests output coherence; perfect calibration of the distribution-mode estimate to the source-community distribution is not required.

For repeated sampling, source-community entropy was compared with the entropy of repeated forced-choice model outputs:

```text
sampling_compression =
    source_community_entropy
    - repeated_sample_model_entropy
```

Entropy values are reported on the five-label scale in bits. Positive values indicate that repeated forced-choice outputs under the study protocol are more concentrated than the source-community distribution.

### Statistical inference

Primary inference used item-cluster bootstrap confidence intervals with 2,000 bootstrap iterations and seed `20260621`. For bin-specific estimates, item IDs were resampled with replacement within the bin and all relevant model/prompt rows for resampled items were retained.

For contrasts, each bootstrap replicate recomputed the relevant bin means and subtracted the high-consensus reference estimate. This procedure avoids treating item-model rows as fully independent observations.

The three low-consensus primary endpoints were tested using one-sided positive-effect bootstrap P values, Holm-adjusted across the three endpoints. Because 2,000 bootstrap iterations impose a finite floor, adjusted P values are reported as Holm-adjusted P = 0.0015.

Contrasts comparing low-consensus or diffuse items with high-consensus items used the same bootstrap framework. Mixed-effects model-ready rows are provided as transparency files; mixed-effects model results are outside the reported analyses.

### Robustness and secondary analyses

Robustness analyses addressed parsing/schema validity, source-community distribution construction, annotation and `info` sensitivity, distribution-mode non-degeneracy and surface-form sensitivity. They included strict-valid-only subsets; raw, Jeffreys-smoothed and Laplace-smoothed source-community distributions; high-annotation-only subsets; exclusion of `info`-majority items; exclusion of high-`info` items; distribution-quality diagnostics; non-API baselines; and aggregate paraphrase analyses.

Distribution-quality diagnostics included Jensen-Shannon divergence, total variation distance, entropy and Brier summaries, with uniform, global-base-rate and source-majority-oracle baselines. These diagnostics assessed non-degeneracy and item sensitivity rather than perfect distribution calibration.

Normative certainty was analysed as a secondary descriptive construct distinct from estimated source-community agreement. No formal recognition audit was run for the final 50k analysis, and contamination was not directly measured.

## Data availability

Derived analysis files and reproducibility records are available through the OSF project (`https://osf.io/rwhax/overview`), OSF registration home (`https://osf.io/rwhax/registrations`), GitHub repository (`https://github.com/pbriggs/format-induced-moral-overresolution`), the post-50k execution/completion archive (`https://doi.org/10.5281/zenodo.20786461`) and the paper-analysis archive (`https://doi.org/10.5281/zenodo.20789625`). The corresponding release tags are `post-50k-completion-v1` and `paper-analysis-50k-v1`.

Public derived/reviewable materials include frozen target lists and run manifests with sensitive details removed where needed, release-safe prompt templates and schema files, endpoint tables, bootstrap confidence intervals, adjusted tests, parsed-output/validity-status and exclusion summaries, robustness summaries, paraphrase-audit summaries, distribution-quality diagnostics, baseline diagnostics, normative-certainty summaries, manuscript-table CSVs, figure-ready CSVs and rendered figures. The Supplementary Information lists the main source-data and analysis files for Supplementary Tables and Extended Data. Analysis code is described in the Code Availability statement. The repository license is CC0 1.0 Universal unless superseded by OSF project settings. Redistribution of dataset and model-output material remains subject to third-party terms, privacy considerations and institutional review requirements.

The source SCRUPLES data should be accessed through the original dataset source subject to its terms [4]. Raw SCRUPLES anecdotes, rendered prompts containing anecdote text, newly collected raw model/provider responses, full call ledgers and full SQLite run stores are not redistributed in unrestricted form where doing so could conflict with SCRUPLES/AllenAI terms, model-provider terms, privacy/sensitivity considerations or institutional review requirements. Restricted verification materials can be provided to editors or reviewers upon reasonable request under appropriate non-redistribution conditions and subject to applicable third-party terms.

## Code availability

Analysis code and figure-generation scripts are available at `https://github.com/pbriggs/format-induced-moral-overresolution` and archived under release tag `paper-analysis-50k-v1` with DOI `https://doi.org/10.5281/zenodo.20789625`. The repository includes preprocessing code, prompt templates, schema files, target-scoped export scripts, parsing and validation code, bootstrap procedures, manuscript tables and figure-rendering scripts. API credentials and provider-specific secrets are not included.

The final 50k analysis can be regenerated locally from the completed run database, when available in an authorized local or reviewer environment, with the offline analysis commands:

```powershell
$env:PYTHONPATH='src'
$env:PYTHONDONTWRITEBYTECODE='1'
python -m analysis.final_50k_exports --bootstrap-iterations 2000
python -m analysis.render_final_figures
```

These commands regenerate analysis tables and figures from completed-run data without making new provider calls.

Full local setup instructions are provided in `README.md`, `.env.example` and `docs/DATA_SETUP.md`. They cover dependency installation, SCRUPLES data placement and environment variables for optional provider-call reproduction. Optional provider-call reruns require the user's own provider credentials and may produce new model outputs rather than exactly reproducing the frozen 50k collection.

## AI assistance disclosure

The author used AI tools for editorial drafting support, code/checklist support, manuscript organization and revision planning. The author reviewed, verified and takes responsibility for all analyses, claims, interpretations and final manuscript text. No AI tool is listed as an author.

## Ethics and human-subjects statement

No new human participants were recruited for this computational audit, and the author did not interact with human participants. The study analysed an existing SCRUPLES dataset of source-community judgments and newly collected model outputs. No formal institutional review board or ethics-committee determination was obtained for this independent computational study. Raw anecdotes, rendered prompts and raw model/provider responses are treated cautiously because they may contain sensitive interpersonal content and may be subject to dataset terms, provider terms and privacy considerations.

## Funding

The author received no external funding for this work. API and computing costs were paid personally by the author.

## Competing interests

The author declares no competing interests.

## Author contributions

P.B. conceived the study, designed the protocol, implemented the data-collection and analysis pipeline, conducted the analyses, interpreted the results, prepared the figures and tables, and wrote and revised the manuscript.

## Acknowledgements

The author thanks Nicholas Lourie, Ronan Le Bras and Yejin Choi, and the Allen Institute for AI, for releasing the SCRUPLES dataset and code. The source-community judgments analysed here derive from the SCRUPLES Anecdotes source community and are treated as source-community reference distributions rather than broader normative standards.

## References

1. Jiang, L. et al. Investigating machine moral judgement through the Delphi experiment. *Nature Machine Intelligence* **7**, 145-160 (2025). https://doi.org/10.1038/s42256-024-00969-6
2. Steyvers, M. et al. What large language models know and what people think they know. *Nature Machine Intelligence* **7**, 221-231 (2025). https://doi.org/10.1038/s42256-024-00976-7
3. Kumaran, D. et al. Competing biases underlie overconfidence and underconfidence in LLMs. *Nature Machine Intelligence* **8**, 614-627 (2026). https://doi.org/10.1038/s42256-026-01217-9
4. Lourie, N., Le Bras, R. & Choi, Y. SCRUPLES: A corpus of community ethical judgments on 32,000 real-life anecdotes. *Proceedings of the AAAI Conference on Artificial Intelligence* **35**, 13470-13479 (2021). https://doi.org/10.1609/aaai.v35i15.17589
5. Abdulhai, M., Serapio-Garcia, G., Crepy, C., Valter, D., Canny, J. & Jaques, N. Moral foundations of large language models. arXiv:2310.15337 (2023). https://arxiv.org/abs/2310.15337
6. Takemoto, K. The moral machine experiment on large language models. *Royal Society Open Science* **11**, 231393 (2024). https://doi.org/10.1098/rsos.231393
7. Zaim bin Ahmad, M. S. & Takemoto, K. Large-scale moral machine experiment on large language models. *PLoS One* **20**, e0322776 (2025). https://doi.org/10.1371/journal.pone.0322776

## Main display items

**Fig. 1 | Study design for testing uncertainty transfer across prompt formats.** SCRUPLES source-community vote distributions were grouped by source-community disagreement bin and evaluated in matched item-model comparisons across prompt formats. Distribution mode elicited five-label source-community probability estimates; descriptive verdict/agreement mode elicited one label and an estimated source-community agreement value; repeated-sampling mode elicited repeated forced-choice outputs for the same item-model pair. The three primary endpoints are agreement surplus, distribution-agreement gap and sampling compression. Together, they compare source-community support, distribution-mode probabilities, verdict/agreement estimates and repeated-output entropy. Paraphrase-audit results provide supporting aggregate surface-form evidence, and normative-certainty results are secondary descriptive evidence; neither component is a primary endpoint. This schematic is a design overview; quantitative endpoint results are reported in Figs. 2–4 and Table 2.

**Fig. 2 | Verdict prompts inflate apparent source-community agreement.** Agreement surplus by source-community disagreement bin and model. Bars show aggregate means across the evaluated models; overlaid points show model-level means. Positive values mean that the verdict-mode estimated source-community agreement exceeds source-community support for the model's chosen label. In the low-consensus primary subset, mean agreement surplus was 0.370931 (95% item-cluster bootstrap CI, 0.361206-0.381114; n = 3,749 item-model rows; Holm-adjusted P = 0.0015).

**Fig. 3 | Verdict prompts overstate agreement relative to the same model's distribution-mode estimate.** Distribution-agreement gap by source-community disagreement bin and model. Bars show aggregate means across the evaluated models; overlaid points show model-level means. Positive values mean that the verdict-mode agreement estimate exceeds the same model's distribution-mode probability for the same item and verdict-selected label. The endpoint tests output coherence across formats rather than calibration of distribution-mode estimates to the SCRUPLES source-community distribution. In the low-consensus primary subset, mean distribution-agreement gap was 0.232687 (95% item-cluster bootstrap CI, 0.224387-0.241341; n = 3,736 item-model rows; Holm-adjusted P = 0.0015).

**Fig. 4 | Repeated forced-choice outputs compress source-community disagreement.** Sampling compression by source-community disagreement bin and model. Bars show aggregate means across the evaluated models; overlaid points show model-level means for source-community entropy minus entropy of repeated forced-choice outputs on the five-label scale in bits. Positive values mean that repeated forced-choice outputs are more concentrated than source-community judgments under the study protocol. In the low-consensus primary subset, mean sampling compression was 1.264638 bits (95% item-cluster bootstrap CI, 1.218425-1.309054; n = 750 item-model summaries; Holm-adjusted P = 0.0015).

**Table 1 | Frozen model roster and target allocation.** The roster reports the evaluated model IDs, access routes, collection windows and target calls. Provider/route fields record provenance only; provider-family, route and model-family comparisons are outside the analysis. The allocation table reports the frozen study components used for the target-scoped audit.

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
| Paraphrase audit | 250 | 2,500 | Aggregate surface-form evidence |
| Normative certainty | 1,000 | 5,000 | Secondary descriptive analysis |
| Total |  | 47,500 | Frozen 50k target-scoped analysis |

**Table 2 | Primary endpoint estimates, contrasts, confidence intervals and adjusted tests.**

| Endpoint | Low-consensus primary mean (95% CI) | Holm-adjusted P | Diffuse secondary mean (95% CI) | High-consensus reference mean (95% CI) | Low–high contrast (95% CI) |
|---|---:|---:|---:|---:|---:|
| Agreement surplus | 0.370931 (0.361206-0.381114) | 0.0015 | 0.435619 (0.427337-0.444341) | 0.169409 (0.145651-0.194624) | 0.201523 (0.174835-0.228568) |
| Distribution-agreement gap | 0.232687 (0.224387-0.241341) | 0.0015 | 0.226556 (0.216740-0.237164) | 0.182842 (0.169762-0.196217) | 0.049845 (0.033774-0.065329) |
| Sampling compression, bits | 1.264638 (1.218425-1.309054) | 0.0015 | 1.507379 (1.452200-1.562768) | 0.563708 (0.495005-0.633547) | 0.700930 (0.618287-0.783543) |

Estimates use the frozen 50k target-scoped analysis. Low-consensus values are the primary confirmatory estimates; diffuse/no-clear-consensus values are secondary evidence and remain separate from the primary endpoint definition; high-consensus values are positive estimates for the reference condition. Confidence intervals are item-cluster bootstrap intervals with 2,000 bootstrap iterations. P values are one-sided positive-effect bootstrap P values, Holm-adjusted across the three low-consensus primary endpoints; with 2,000 bootstrap iterations, Holm-adjusted P values are reported at the finite bootstrap floor of 0.0015.

## Extended Data and Supplementary Information

The Supplementary Information provides reviewer-facing methodological detail, source-data references and release-safe reproducibility information for the Extended Data figures, Extended Data table and Supplementary Tables. The corresponding source-data files are listed in the Supplementary Information rather than repeated in full in the main manuscript.

**Extended Data Fig. 1 | Distribution-quality diagnostics.** Diagnostic distances and entropy summaries by source-community disagreement bin and model show that distribution-mode outputs varied by item and bin and were not merely uniform or fixed base-rate responses. This is a diagnostic support analysis, not a distribution-prediction benchmark.

**Extended Data Fig. 2 | Aggregate paraphrase-audit effects.** Aggregate paraphrase-audit agreement surplus and distribution-agreement gap estimates preserve the direction of the main effects. The figure should be interpreted with the limited matched-coverage caveat stated in the Results and Supplementary Information.

**Extended Data Fig. 3 | Validity by model and prompt mode.** Primary-valid output rates by model and prompt mode show high validity and limited invalid outputs in the frozen 50k target-scoped analysis.

**Extended Data Table 1 | Validity and exclusion summary.** Reports validity by model/mode, invalid status counts, minimum model/mode validity, refusal count, off-schema count, API errors, terminal failures and repair fields.

**Supplementary Table 1 | Full model roster, API parameters, model-level endpoints and leave-one-model-out summaries.** Provides model provenance, API-parameter reporting and cross-model consistency checks without making provider-family or model-family claims.

**Supplementary Table 2 | Source-community distribution smoothing robustness.** Reports raw-proportion, Jeffreys-smoothed and Laplace-smoothed source-community distribution sensitivity checks.

**Supplementary Table 3 | Annotation and `info` robustness.** Reports high-annotation-only, `info`-majority exclusion and high-`info` exclusion checks.

**Supplementary Table 4 | Paraphrase audit.** Reports paraphrase target calls, valid outputs, aggregate effects, confidence intervals, chosen-label stability and the matched-coverage caveat.

**Supplementary Table 5 | Distribution quality and baselines.** Reports distribution-quality diagnostics and uniform, global-base-rate and source-majority-oracle baselines.

**Supplementary Table 6 | Normative certainty.** Reports the secondary moral-certainty construct; moral certainty is not equivalent to estimated source-community agreement.

**Supplementary Table 7 | Validity and exclusions.** Reports validity and exclusion summaries and cross-references Extended Data Table 1.

**Supplementary Table 8 | Model-ready secondary rows.** Provides model-ready secondary rows as transparency files; these files do not contain reported mixed-effects model results.

**Supplementary Notes.** The Supplementary Information provides supporting methodological detail for prompt and schema reproducibility, source-community preprocessing, item allocation, model provenance, parsing and exclusions, endpoint definitions, bootstrap inference, robustness checks, paraphrase limitations, distribution-quality diagnostics, normative-certainty secondary analysis and public/restricted materials boundaries.
