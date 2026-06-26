# Verdict-style prompts induce moral over-resolution in large language models

**Author:** Paul Briggs  
**Affiliation:** Independent researcher, Los Angeles, CA, USA  
**Corresponding author:** Paul Briggs, p.ivan.briggs@gmail.com  
**ORCID:** https://orcid.org/0009-0002-9951-8661

## Abstract

Large language models are often asked to judge everyday disputes by choosing who was in the wrong. For such cases, source-community votes range from near-unanimous to deeply divided. A verdict-style answer should not make that disagreement sound more settled than the votes support. In a preregistered audit, five LLMs evaluated matched ethical scenarios in distribution mode, verdict/agreement mode and repeated-sampling mode. In verdict/agreement mode, models estimated more source-community agreement for their chosen label than the recorded votes supported, and more than each model’s own distribution-mode estimate for that label. Repeated forced-choice outputs were also more concentrated than source-community votes, with the clearest concern in divided cases. These findings identify a format-specific reliability failure: verdict-style interfaces can make divided cases appear more settled than the source-community votes support.


## Main

Large language models are asked to judge everyday disputes by choosing who was in the wrong. Source-community votes on the same cases vary in consensus: in some cases a large majority of votes points to one label; in others, votes divide across several. When a model is asked to choose one label and estimate how much the source community agrees, it can report high agreement for a case where the votes were divided. That mismatch is the reliability concern this study examines.

Asking for one answer changes what a model communicates about its uncertainty. Given the same case, a model asked to distribute probability across labels may assign substantial weight to several; asked for one label and an agreement estimate, the same model may choose one label and report strong source-community agreement. Those two answers came from the same model on the same case; the prompt mode changed, not the case or the model. When the same case produces different apparent levels of source-community agreement depending on how the question is framed, the verdict-style format can make the case appear more settled than the source-community votes indicate.

Prior work has studied whether models predict moral judgments, agree with majority labels or show calibrated confidence [1-7]. These studies ask how well model outputs match a reference distribution from one format. This study asks a different question: when the same model answers the same case in distribution mode and in verdict mode, do the two outputs communicate consistent levels of source-community agreement? Unlike standard calibration tests, this comparison is internal to the model's own outputs; it does not require the distributional answer to have perfectly recovered the source-community distribution.

The failure mode this study tests is format-induced moral over-resolution: a verdict-style prompt can make a divided case appear more settled than the source-community votes — or the model's own distributional answer — would indicate. Three matched-item endpoints test whether and how much verdict-style outputs over-resolve source-community disagreement. Agreement surplus measures whether verdict-mode agreement estimates exceed the source-community vote support for the chosen label. The distribution-agreement gap measures whether those estimates also exceed the same model’s own distribution-mode probability for the same label; because it compares the same model, item and chosen label across elicitation formats, it is the most direct cross-format coherence test. Sampling compression measures whether repeated forced-choice outputs are more concentrated than the source-community vote distribution.

The study uses SCRUPLES Anecdotes, a corpus of everyday ethical situations with recorded votes on who was in the wrong [4]. "Source community" here refers to the annotator population represented in SCRUPLES; the resulting vote distributions are reference data from that data-generating process, not moral truth, universal norms or representative population estimates. In this preregistered audit, five LLMs evaluated matched SCRUPLES items in distribution mode, descriptive verdict/agreement mode and repeated-sampling mode (Fig. 1). Low-consensus items — cases with a majority label but substantial remaining disagreement in the source-community votes — were the primary confirmatory subset. Diffuse/no-clear-consensus items were analysed separately as secondary evidence; high-consensus items served as a reference condition.

## Results


### Endpoint logic and target set

The three endpoints — agreement surplus, distribution-agreement gap and sampling compression — were evaluated on matched item-model comparisons. Low-consensus items (cases with a majority label but substantial remaining source-community disagreement) were the primary confirmatory subset; diffuse/no-clear-consensus items were analysed separately as secondary evidence; high-consensus items served as a reference condition. This hierarchy keeps the confirmatory test distinct from the secondary and reference conditions. Table 1 and Methods report the model roster, component allocation and scale, including 47,500 target calls and 47,432 primary-valid outputs.


### Verdict prompts inflate apparent agreement

Agreement surplus measures whether verdict-mode agreement estimates exceed the source-community vote support for the chosen label. In the low-consensus primary subset, agreement surplus was 0.370931 (95% CI, 0.361206-0.381114; Holm-adjusted P = 0.0015; n = 3,749 item-model rows; Fig. 2 and Table 2): verdict-mode estimates exceeded source-community vote support for the chosen label by approximately 37 percentage points. The accompanying agreement estimate can make the chosen label appear more widely supported than the source-community votes show.

The same direction appeared outside the primary subset. Diffuse/no-clear-consensus items showed a larger secondary estimate: agreement surplus was 0.435619 (95% CI, 0.427337-0.444341; n = 2,500). High-consensus items also showed positive agreement surplus, 0.169409 (95% CI, 0.145651-0.194624; n = 1,750), with a low-consensus-minus-high-consensus contrast of 0.201523 (95% CI, 0.174835-0.228568). High-consensus items therefore served as a positive reference condition, while the larger low-consensus surplus shows greater reliability concern where source-community agreement was weaker.

### Verdict agreement exceeds the model's distributional estimate

The distribution-agreement gap compares each model's verdict-mode agreement estimate with the same model's distribution-mode probability for the same item and chosen label. A positive gap means the verdict/agreement format reported more estimated source-community agreement for the chosen label than the same model assigned to that label in distribution mode.

This comparison is internal to the model's own outputs: it holds model, item and chosen label constant while the elicitation format differs. Because of that structure, this comparison does not require perfect calibration of the distribution-mode estimate to the source-community distribution. It tests whether the same model communicates compatible levels of source-community agreement for the same case and chosen label across two elicitation formats.

In the low-consensus primary subset, the distribution-agreement gap was 0.232687 (95% CI, 0.224387-0.241341; Holm-adjusted P = 0.0015; n = 3,736; Fig. 3 and Table 2): for the same item and chosen label, verdict/agreement mode reported more agreement than the same model's distribution-mode probability supported.

Diffuse items showed a secondary gap of 0.226556 (95% CI, 0.216740-0.237164; n = 2,494). High-consensus items also showed a positive gap of 0.182842 (95% CI, 0.169762-0.196217; n = 1,745), with a low-consensus-minus-high-consensus contrast of 0.049845 (95% CI, 0.033774-0.065329). High-consensus items remained a positive reference condition; the larger low-consensus contrast indicates a greater coherence concern when source-community votes were more divided. Within the three-endpoint design, this gap is the most direct evidence that the same model can report different levels of apparent source-community agreement for the same case and label depending on how the question is framed.

### Repeated forced-choice outputs compress source-community disagreement

The first two endpoints concern stated agreement estimates. The third asks whether the same concentration pattern appears when models are asked only to choose labels repeatedly, without stating agreement. Sampling compression is source-community entropy minus the entropy of repeated forced-choice outputs on the five-label scale; positive values mean outputs were more concentrated across labels than source-community votes for the same items.

In the low-consensus primary subset, sampling compression was 1.264638 bits (95% CI, 1.218425-1.309054; Holm-adjusted P = 0.0015; n = 750 item-model summaries; Fig. 4 and Table 2). Diffuse items showed stronger secondary compression, 1.507379 bits (95% CI, 1.452200-1.562768; n = 500). High-consensus items also showed positive compression, 0.563708 bits (95% CI, 0.495005-0.633547; n = 350). The low-consensus-minus-high-consensus contrast was 0.700930 bits (95% CI, 0.618287-0.783543).

Under the study's repeated forced-choice protocol, outputs across fresh calls were more concentrated than source-community votes, with larger compression in the low-consensus primary subset than in the high-consensus reference condition. This endpoint extends the finding beyond stated agreement: concentration appears in label choices as well. Repeated forced-choice outputs under this protocol measure label diversity across fresh calls rather than stochastic sampling from an internal model distribution.

### Pattern across models and output validity

All five evaluated models showed positive low-consensus agreement surplus, positive low-consensus distribution-agreement gap and positive low-consensus sampling compression. Model-level low-consensus agreement surplus ranged from 0.326454 to 0.445325. Low-consensus distribution-agreement gaps ranged from 0.215187 to 0.271943. Low-consensus sampling compression ranged from 0.920001 to 1.408416. Leave-one-model-out summaries preserved the direction of the aggregate pattern for all three endpoints. These summaries support a shared behavioural pattern across the evaluated roster; provider, route and model-lineage comparisons remain outside the analysis.

Output validity was also high across the audit. Of 47,500 outputs, 47,432 were primary-valid (validity rate = 0.998568), comprising 38,790 strict-schema outputs and 8,642 extracted-JSON outputs. The minimum model/mode primary-valid rate was 0.969. Invalid statuses were 52 probability-out-of-bounds outputs, 10 probability-sum errors, 4 invalid-JSON outputs and 2 empty responses. Refusals and off-schema labels were both zero. Repair fields were tracked; `repair_attempted` and `repair_successful` were both zero, so no repaired outputs entered the final analysis. Validity by model and prompt mode is summarized in Extended Data Fig. 3 and Extended Data Table 1.

### Robustness and diagnostics

The directional pattern of the three low-consensus endpoint results was preserved across robustness checks that recomputed the endpoints under alternative validity, reference-distribution and item-composition choices.

A strict-valid-only analysis restricted the data to outputs satisfying the strict schema. The direction of all three low-consensus endpoints was preserved: agreement surplus 0.376030, distribution-agreement gap 0.223867 and sampling compression 1.268188.

The source-community reference distribution was checked against alternative constructions from SCRUPLES vote counts. Low-consensus endpoint effects were recomputed using raw proportions, Jeffreys smoothing and Laplace smoothing, and positive effects were preserved across all three. These checks addressed reference-distribution construction, not the calibration of distribution-mode outputs to those distributions.

Item-composition checks asked whether the pattern depended on annotation density or on the `info` label. The directional endpoint pattern was preserved in high-annotation-only analyses, after excluding `info`-majority items and after excluding high-`info` items.

Distribution-mode diagnostics confirmed that model outputs varied by item and disagreement bin. Source entropy was higher in diffuse items (mean 1.955481 bits) than in high-consensus items (0.823596 bits). Model distribution entropy also varied by bin, with higher entropy in diffuse (1.515785 bits) and low-consensus items (1.476755 bits) than in high-consensus items (1.200675 bits). These analyses, summarized in Extended Data Fig. 1, are diagnostic rather than distribution-prediction or perfect-calibration tests.

The paraphrase audit provided aggregate surface-form evidence in paraphrased items (Extended Data Fig. 2), with 2,500 target calls and 2,495 valid outputs. In paraphrased low-consensus items, agreement surplus was 0.366821 (95% CI, 0.334632-0.397075) and the distribution-agreement gap was 0.212124 (95% CI, 0.192023-0.231651). In paraphrased diffuse items, the corresponding estimates were 0.418159 (95% CI, 0.396906-0.443057) and 0.200502 (95% CI, 0.174963-0.225410).

Within the limited matched original-vs-paraphrase overlap, chosen-label stability was 0.655 in low-consensus rows and 0.467 in diffuse rows. With 29 matched low-consensus rows and 15 matched diffuse rows, this component provides aggregate surface-form evidence rather than a definitive paired original-vs-paraphrase test.


## Discussion

Under the tested prompt formats and evaluated models, verdict-style answers made divided cases appear more settled than either the source-community votes or the same model's own distributional answer would indicate. The clearest evidence is the distribution-agreement gap: for the same model, item and chosen label, verdict-mode agreement estimates exceeded the model's own distribution-mode probability for that label — a within-model comparison that holds model, item and label constant. This gap, together with positive agreement surplus and sampling compression in the same low-consensus setting, shows that the apparent level of source-community agreement a model communicates can depend on the elicitation format.

The finding has implications for how LLM reliability is evaluated. Majority-label accuracy can reward a model for selecting the most common label without indicating how that model estimates source-community agreement in verdict mode. Distribution-mode uncertainty tests are similarly incomplete on their own: a model can produce non-degenerate distributional outputs while also reporting higher apparent source-community agreement in verdict mode for the same item and label. Prior work shows that benchmark conclusions can depend on prompt formatting [8]; the present results extend that concern to whether agreement estimates remain consistent when the interface changes from distributional to verdict-style.

The findings also bear on interface design. When a model is prompted for a verdict on a divided case, the accompanying agreement estimate can substantially exceed what the source-community votes and the model's own distributional answer would support for that label. The design implication is that verdict-mode agreement estimates are not interchangeable with distributional probability estimates for the same case and label. Whether interface changes would reduce that gap is a question outside this study.

The findings are bounded by one source-community dataset, five evaluated models, a finite set of prompt templates and a source community that is not a universal or representative population sample.

The paraphrase audit provides aggregate surface-form evidence; it did not test training-set membership; contamination was not directly measured; and the small matched original-vs-paraphrase overlap limits paired interpretation. Item familiarity could affect absolute label probabilities, though the distribution-agreement gap compares the same model's outputs across formats for the same item rather than against an external calibration target. The study leaves user effects -- including effects on perceived social consensus, confidence and decision-making -- as an open empirical question.

The implication for model-output reliability is direct. Testing models only in distribution mode can miss over-resolution in verdict mode: a model can produce non-degenerate distributional outputs while reporting higher apparent source-community agreement in verdict mode for the same case and label. Reliability evaluations that compare verdict-mode agreement estimates against the same model's distributional outputs for matched items can identify that discrepancy. An evaluation limited to one format can make distributional uncertainty appear adequate in that format while missing how the same model behaves when asked for a verdict.

## Methods

### Preregistration and analysis scope

The study was preregistered on OSF as a target-scoped computational audit. It used existing SCRUPLES source-community judgments and newly collected LLM API outputs; no new human participants were recruited. The analysis uses the frozen 50k target-scoped exports from `post_run/analysis_exports/50k/`.

Operational milestones tracked monitoring and release discipline. Primary endpoint definitions and the low-consensus confirmatory subset remained fixed after inspection of the final 50k results; subsequent presentation changes did not alter the frozen numerical outputs.

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

Robustness checks used raw proportions and Laplace smoothing with alpha = 1.0.

Items were stratified by top-label support:

```text
high consensus:             top-label support >= 0.80
moderate consensus:         top-label support >= 0.65 and < 0.80
low consensus:              top-label support >= 0.50 and < 0.65
diffuse/no-clear-consensus: top-label support < 0.50
```

Item selection and label-order assignment used the recorded milestone seed `20260615`. Within each disagreement bin, eligible items were selected according to the frozen allocation plan and component-specific target counts; the released target manifests record the resulting item IDs. Beyond the eligibility rules above, target-list membership was determined by the frozen allocation plan and recorded seed rather than by inspection of model outputs.

Low-consensus items were the primary confirmatory subset, diffuse/no-clear-consensus items remained secondary, and high-consensus items served as the reference condition.

The core cross-format component used 350 high-consensus, 400 moderate-consensus, 750 low-consensus and 500 diffuse/no-clear-consensus items. The repeated-sampling, paraphrase-audit and normative-certainty components used component-specific target sets. The paraphrase audit used a stratified subset for aggregate surface-form checks.

### Model roster and collection

The amended frozen roster contained five models: `claude-sonnet-4-6`, `deepseek/deepseek-v3.2`, `gpt-5.5`, `grok-4.3` and `qwen/qwen3.7-max`. Each model had 9,500 target calls. API routes and call windows are reported in Table 1a.

Temperature was 0.0 for all exported rows. Top-p was blank/null in the final model roster. Provider and route fields record access provenance and are not analysed as cross-provider group effects. Exact model snapshot dates were not available in the local final roster and are not inferred beyond the recorded first and last call timestamps.

Full API-parameter fields, structured-output settings where applicable, maximum-token settings, retry-policy fields, reasoning-effort fields when present and collection timestamps are reported in the Supplementary Information and exported roster. The Supplementary Information and run manifests document the roster amendment and final completion/analysis provenance. The final analysis uses only the amended frozen five-model roster.

### Prompt modes and request construction

Distribution mode asked each model to estimate the source-community probability distribution over the five labels. Descriptive verdict/agreement mode asked the model to choose one label and estimate source-community agreement for that choice. Repeated-sampling mode elicited ten single-label forced-choice outputs for each repeated-sampling item-model pair. Normative-certainty prompts elicited a separate moral-certainty construct for secondary descriptive analysis.

Requests were fresh and stateless across prompt modes. The verdict/agreement prompt did not include the model's own distribution-mode answer. Prompt templates, schemas, label order, rendered prompt hashes, model IDs, API route, timestamps and decoding parameters were recorded in run records. Prompts requested structured final outputs and did not request chain-of-thought.

For repeated sampling, the ten outputs for each item-model pair were ten separate fresh calls under the sampling prompt at temperature 0.0. Label order was assigned separately for each prompt assignment using the recorded seed procedure; `sample_id` was part of the local label-order seed. Invalid outputs were handled under the same parsing and validity rules as other components before entropy summaries were computed. The sampling-compression endpoint measures diversity across repeated forced-choice outputs under the recorded prompt and label-order randomization protocol rather than stochastic sampling from an internal model distribution.

For paraphrase analyses, paraphrased versions of a stratified item subset were generated with the study's paraphrase-generation prompt mode. The paraphrased items were then evaluated with the paraphrased distribution and paraphrased descriptive verdict/agreement modes, using the same response schemas and parsing/validity rules as corresponding original-item prompts. Because matched original-vs-paraphrase coverage was limited, the paraphrase component provides aggregate surface-form evidence rather than a definitive paired original-vs-paraphrase test. This component did not test training-set membership, and contamination was not directly measured.

Rendered prompt hashes were computed after inserting item text and randomized label order. Public materials describe prompt structure and release-safe templates while excluding rendered prompts containing source anecdotes.

### Parsing, validity and exclusions

Strict JSON schema enforcement was used where supported. Otherwise, JSON was extracted from model responses and validated against the required fields and ranges. Outputs were excluded from primary analyses if the response was empty, invalid JSON, out of range, outside the validation tolerance for five-label probability sums, missing required fields, a refusal, an off-schema label or a terminal/API failure without a valid response.

For distribution-mode outputs, all five label probabilities had to be castable to floats and within the closed interval [0, 1]. Values outside that interval were marked as `probability_out_of_bounds`.

Probability vectors were accepted when their total fell within the inclusive interval [0.99, 1.01]. Accepted vectors whose totals differed from 1.0 by more than 1e-12 were renormalized to sum to one before downstream use. The 1e-12 threshold was only the renormalization threshold, not the exclusion tolerance. Vectors with totals below 0.99 or above 1.01 were marked as `probability_sum_error` and excluded from primary analyses. These statuses were assigned by the collection-time parser; the final 50k exporter inherited stored parser validity statuses rather than revalidating probability sums or applying a second tolerance.

The frozen analysis included 47,500 planned, attempted and completed target calls. Run provenance recorded 0 API errors, 0 terminal failures, retry rate 0.0, executor status passed and database integrity ok.

Primary-valid outputs were 47,432 of 47,500: 38,790 strict-schema outputs and 8,642 extracted-JSON outputs. Invalid status counts were 52 `probability_out_of_bounds` outputs, 10 `probability_sum_error` outputs, 4 invalid-JSON outputs and 2 empty responses. Refusals and off-schema labels were zero. Repair fields were tracked, but `repair_attempted=0` and `repair_successful=0`; the final 50k analysis contained no repaired outputs. Validity by model and prompt mode is reported in Extended Data Table 1.

Strict-schema support varied across access routes. The robustness analyses included a strict-valid-only subset, which preserved the direction of all three low-consensus endpoints and is reported in Results and the Supplementary Information.

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

Primary inference used item-cluster bootstrap confidence intervals with 2,000 bootstrap iterations and seed `20260621`. For bin-specific estimates, each bootstrap replicate resampled item IDs with replacement within the bin and retained all relevant model/prompt rows associated with the resampled items.

For contrasts, each bootstrap replicate recomputed the relevant bin means and subtracted the high-consensus reference estimate. This item-level clustering avoids treating item-model rows as fully independent observations.

The three low-consensus primary endpoints were tested using one-sided positive-effect bootstrap P values, Holm-adjusted across the three endpoints. Because 2,000 bootstrap iterations impose a finite floor, adjusted P values are reported as Holm-adjusted P = 0.0015.

Contrasts comparing low-consensus or diffuse items with high-consensus items used the same bootstrap framework. Mixed-effects model-ready rows are provided as transparency files; mixed-effects model results are outside the reported analyses.

### Robustness and secondary analyses

Robustness analyses covered five areas: parsing and schema validity, source-community distribution construction, annotation and `info` sensitivity, distribution-mode non-degeneracy, and prompt surface form. Checks included strict-valid-only subsets; raw, Jeffreys-smoothed and Laplace-smoothed source-community distributions; high-annotation-only subsets; exclusion of `info`-majority and high-`info` items; distribution-quality diagnostics with non-API baselines; and aggregate paraphrase analyses.

Distribution-quality diagnostics included Jensen-Shannon divergence, total variation distance, entropy and Brier summaries, with uniform, global-base-rate and source-majority-oracle baselines. These diagnostics assessed non-degeneracy and item sensitivity rather than perfect distribution calibration.

Normative certainty was analysed as a secondary descriptive construct distinct from estimated source-community agreement. No formal recognition audit was run for the final 50k analysis, and contamination was not directly measured.

## Data availability

Derived analysis files and reproducibility records are available through the OSF project (`https://osf.io/rwhax/overview`), OSF registration home (`https://osf.io/rwhax/registrations`), GitHub repository (`https://github.com/pbriggs/format-induced-moral-overresolution`), the post-50k execution/completion archive (`https://doi.org/10.5281/zenodo.20786461`) and the paper-analysis archive (`https://doi.org/10.5281/zenodo.20789625`). The corresponding release tags are `post-50k-completion-v1` and `paper-analysis-50k-v1`.

Release-safe materials include frozen target lists and run manifests with sensitive details removed where needed; prompt templates and schemas; derived endpoint, robustness, paraphrase, baseline, secondary normative-certainty and distribution-quality summaries; bootstrap intervals, adjusted tests and validity/exclusion summaries; manuscript-table CSVs, figure-ready CSVs and rendered figures. The Supplementary Information and repository documentation list the main source-data and analysis files, and analysis code is described below. The repository license is CC0 1.0 Universal unless superseded by OSF project settings.

Raw SCRUPLES anecdotes, rendered prompts containing anecdote text, newly collected raw model/provider responses, full call ledgers and full run stores containing restricted or mixed material are not redistributed in unrestricted form where doing so could conflict with SCRUPLES/AllenAI terms, model-provider terms, privacy/sensitivity considerations or institutional review requirements. The source SCRUPLES data should be accessed through the original dataset source subject to its terms [4]. Restricted verification materials can be provided to editors or reviewers upon reasonable request under appropriate non-redistribution conditions and applicable third-party terms.

## Code availability

Analysis and figure-generation code are available at `https://github.com/pbriggs/format-induced-moral-overresolution` and archived under release tag `paper-analysis-50k-v1` with DOI `https://doi.org/10.5281/zenodo.20789625`. The repository includes preprocessing, prompt/schema, parsing/validation, bootstrap-analysis, manuscript-table and figure-rendering code. API credentials and provider-specific secrets are not included.

Local setup and regeneration instructions are provided in `README.md`, `.env.example` and `docs/DATA_SETUP.md`. Offline regeneration uses completed-run data in an authorized local or reviewer environment and does not make new provider calls. Optional provider-call reruns require the rerunning researcher’s own provider credentials and may produce new model outputs rather than exactly reproducing the frozen 50k collection.

## AI assistance disclosure

The author used AI tools for editorial drafting support, code and checklist support, manuscript organization and revision planning. The author reviewed, verified and takes responsibility for all analyses, claims, interpretations and final manuscript text. No AI tool is listed as an author.

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
8. Sclar, M., Choi, Y., Tsvetkov, Y. & Suhr, A. Quantifying language models' sensitivity to spurious features in prompt design or: How I learned to start worrying about prompt formatting. *International Conference on Learning Representations* (2024). https://openreview.net/forum?id=RIu5lyNXjT

## Main display items

**Fig. 1 | Study design for testing cross-format agreement consistency.** SCRUPLES source-community vote distributions were grouped by source-community disagreement bin and evaluated in matched item-model comparisons across prompt formats. Distribution mode elicited five-label source-community probability estimates; descriptive verdict/agreement mode elicited one label and an estimated source-community agreement value; repeated-sampling mode elicited repeated forced-choice outputs for the same item-model pair. The three primary endpoints are agreement surplus, distribution-agreement gap and sampling compression. Together, they compare source-community support, distribution-mode probabilities, verdict/agreement estimates and repeated-output entropy. Paraphrase-audit results provide supporting aggregate surface-form evidence, and normative-certainty results are secondary descriptive evidence; neither component is a primary endpoint. This schematic is a design overview; quantitative endpoint results are reported in Figs. 2–4 and Table 2.

**Fig. 2 | Verdict prompts inflate apparent source-community agreement.** Agreement surplus by source-community disagreement bin and model. Bars show aggregate means across the evaluated models; overlaid points show model-level means. Positive values mean that the verdict-mode estimated source-community agreement exceeds source-community support for the model's chosen label. In the low-consensus primary subset, mean agreement surplus was 0.370931 (95% item-cluster bootstrap CI, 0.361206-0.381114; n = 3,749 item-model rows; Holm-adjusted P = 0.0015).

**Fig. 3 | Verdict prompts overstate agreement relative to the same model's distribution-mode estimate.** Distribution-agreement gap by source-community disagreement bin and model. Bars show aggregate means across the evaluated models; overlaid points show model-level means. Positive values mean that the verdict-mode agreement estimate exceeds the same model's distribution-mode probability for the same item and verdict-selected label. This endpoint is the most direct cross-format coherence test because the model, item and selected label are fixed while the elicitation format changes; it does not require perfect calibration of distribution-mode estimates to the SCRUPLES source-community distribution. In the low-consensus primary subset, mean distribution-agreement gap was 0.232687 (95% item-cluster bootstrap CI, 0.224387-0.241341; n = 3,736 item-model rows; Holm-adjusted P = 0.0015).

**Fig. 4 | Repeated forced-choice outputs compress source-community disagreement.** Sampling compression by source-community disagreement bin and model. Bars show aggregate means across the evaluated models; overlaid points show model-level means for source-community entropy minus entropy of repeated forced-choice outputs on the five-label scale in bits. Positive values mean that repeated forced-choice outputs are more concentrated than source-community judgments under the study protocol. In the low-consensus primary subset, mean sampling compression was 1.264638 bits (95% item-cluster bootstrap CI, 1.218425-1.309054; n = 750 item-model summaries; Holm-adjusted P = 0.0015).

**Table 1 | Model roster and target allocation.** The roster reports the evaluated model IDs, access routes, collection windows and target calls. Provider/route fields record provenance only; provider-family, route and model-family comparisons are outside the analysis. The allocation table reports the frozen study components used for the 50k analysis.

**Table 1a | Model roster and collection windows.**

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
