# Workspace Completion Audit: 50k NMI Manuscript — gap-fixed review

Date: 2026-06-25  
Revision: v2 gap-fixed review based on `workspace_completion_audit_50k.md`

Scope: audit-only review of the `format-induced-moral-overresolution` manuscript workspace and the next packaging path. This revision does not move, rename, delete, regenerate or validate repository assets. It closes planning gaps in the original audit by separating scientific readiness from LaTeX/package readiness, adding LaTeX QA gates, adding Windows/VSCode tooling recommendations, tightening bibliography/package risks and clarifying what still requires manual inspection.

## 1. Concise verdict

**Ready to begin LaTeX packaging; not yet ready as a final LaTeX submission package.**

The manuscript package is scientifically and structurally far enough along to start a clean LaTeX conversion. The current main manuscript and Supplementary Information are present, the figure package is rendered in SVG/PNG/PDF, source-data mappings are documented, and the reported numerical results are traceable to the frozen 50k exports.

The remaining blockers are packaging and verification blockers rather than analysis blockers:

- no `references.bib` exists;
- no LaTeX workspace, template/class file, `main.tex`, `.bbl`, `latexmkrc` or build script exists;
- no compiled PDF has been built and visually inspected;
- the current manuscript references are embedded as numbered Markdown references rather than citation keys or a controlled LaTeX bibliography;
- the proposed `paper/` directory is currently ignored by `.gitignore`, so `submission/` is the safer package root unless the ignore rule is intentionally changed;
- Fig. 1 still needs manual visual review despite automated layout QA;
- no LaTeX log, reference/citation, overfull-box, font-embedding or hyperlink QA has been performed because no LaTeX build exists yet.

Live NMI pages checked in the original audit:

- `https://www.nature.com/natmachintell/content`
- `https://www.nature.com/natmachintell/submission-guidelines/initial-formatting`

Current NMI interpretation for this package:

- Initial submission can be PDF, Word or TeX/LaTeX, and TeX/LaTeX should include compiled PDFs.
- Article format is consistent with the current main display count and abstract length target, but final submission quality still requires a compiled PDF and manual inspection.

## 2. Current canonical manuscript and SI files

Current main manuscript:

- `article/nmi_moral_overresolution_draft_50k_v5.md`
- Size reported in original audit: 48,191 bytes
- Modified reported in original audit: 2026-06-25 11:57:10
- Abstract word count reported in original audit: 149 words

Current Supplementary Information:

- `article/nmi_supplementary_information_50k_v2.md`
- Size reported in original audit: 22,880 bytes
- Modified reported in original audit: 2026-06-24 17:43:47

Recommended canonical package filenames:

- `submission/manuscript.md`
- `submission/supplementary_information.md`
- `submission/references.bib`
- `submission/latex/main.tex`

Gap fixed:

- The original audit correctly identified the `article/` files as canonical, but the next task should copy them into a clean package root rather than editing them in place.
- Before creating `submission/`, check whether it is ignored:

```bash
git check-ignore -v submission/ || true
```

If `submission/` is not ignored, use it. If it is ignored in a local/global ignore, either change the ignore rule intentionally or use a different package root and document the choice.

## 3. Current repo and workspace state

Original audit findings:

- Branch: `main...origin/main`
- Before the audit memo update, the tracked tree was clean.
- After the memo update, the only tracked modification was `post_run/analysis_exports/50k/workspace_completion_audit_50k.md`.
- `git status --short --branch --ignored` also reported ignored/local-only directories.
- Warning observed: `could not open directory '.tmp_pytest/': Permission denied`.

Ignored/local-only material:

- `drafts/`: ignored; 50 files, about 1.4 MB.
- `runs/`: ignored; 2,967 files, about 4.78 GB.
- `data/scruples/`: ignored; three SCRUPLES JSONL files, about 74.96 MB.
- `__pycache__/` and `.tmp_pytest/`: runtime/cache only.
- `paper/`: ignored by `.gitignore`.

Gap fixed:

- The next packaging task should not rely only on `git status`; it should explicitly check ignore behavior for the new package root and for copied figures/source data.
- Add a small package manifest under `submission/package_manifest.md` so the curated package can be audited without re-reading the whole repository.
- Do not copy `runs/`, `data/scruples/`, raw provider responses, rendered prompts containing anecdote text, local style-reference images or full run stores into `submission/`.

Recommended package-status commands after the package root exists:

```bash
git status --short --branch --ignored
git check-ignore -v submission/ || true
find submission -maxdepth 3 -type f | sort > submission/package_file_list.txt
```

## 4. Current figure package status

Final rendered figure directory:

- `post_run/analysis_exports/50k/rendered_figures/`

Rendering script:

- `src/analysis/render_final_figures.py`

Figure source inventory:

- `post_run/analysis_exports/50k/figure_source_inventory_50k.md`

Final export checklist:

- `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`

All expected rendered figures exist in SVG, PNG and PDF:

| Role | Rendered assets | Source CSV | Script |
|---|---|---|---|
| Fig. 1 study design | `figure_study_design_50k.{svg,png,pdf}` | not applicable | `src/analysis/render_final_figures.py` |
| Fig. 2 agreement surplus | `figure_agreement_surplus_by_bin_model_50k.{svg,png,pdf}` | `figure_ready/figure_agreement_surplus_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Fig. 3 distribution-agreement gap | `figure_distribution_gap_by_bin_model_50k.{svg,png,pdf}` | `figure_ready/figure_distribution_gap_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Fig. 4 sampling compression | `figure_sampling_compression_by_bin_model_50k.{svg,png,pdf}` | `figure_ready/figure_sampling_compression_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Extended Data Fig. 1 distribution quality | `figure_distribution_quality_distances_50k.{svg,png,pdf}` | `figure_ready/figure_distribution_quality_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Extended Data Fig. 2 paraphrase audit | `figure_paraphrase_audit_effects_50k.{svg,png,pdf}` | `figure_ready/figure_paraphrase_effects_by_bin_model_50k.csv` | `src/analysis/render_final_figures.py` |
| Extended Data Fig. 3 validity | `figure_validity_rate_by_model_50k.{svg,png,pdf}` | `figure_ready/figure_validity_by_model_mode_50k.csv` | `src/analysis/render_final_figures.py` |

Original audit checks that remain valid:

- All SVG, PNG and PDF files are non-empty.
- All PDFs have `%PDF-` headers.
- Search found no `<image>`, `base64` or `data:image` references in rendered SVGs, so the SVGs appear vector/editable rather than raster-embedded.
- `quantitative_figure_numerical_validation_50k.txt` records PNG dimensions/DPI, SVG raster checks and PDF header checks.
- `figure_study_design_50k_layout_qa.txt` reports 0 text overlaps, 0 text-box border collisions and 0 sampled arrow-text collisions; it still requires manual visual review.

Gap fixed:

- Automated layout QA is not enough. A manual figure pass should be explicit before submission.
- The LaTeX build should include final PDFs for figures by default. Keep SVGs as editable/source-adjacent assets and PNGs as preview/fallback assets.
- After LaTeX conversion, inspect whether figure scaling changes text size, line weights, label readability, panel alignment or caption/callout accuracy.
- If final journal upload later requires separate artwork formats, re-check the journal’s current artwork instructions at that time. For now, the package should preserve PDF, SVG and PNG so format conversion remains possible.

Manual figure QA checklist:

- Open each main and Extended Data PDF at 100%, page width and print-like size.
- Confirm all labels are readable after LaTeX scaling.
- Confirm Fig. 3 says `Distribution-agreement gap`, not the shorter older label.
- Confirm Fig. 4 unit is `bits`.
- Confirm no cropped text, clipped markers, low-contrast points or overlapping labels.
- Confirm Fig. 1 arrows, boxes and labels are legible and visually balanced.
- Confirm captions in LaTeX match the final figure files and do not cite older pre-polish notes.

## 5. Source-data and numerical traceability status

Main Figs. 2–4:

- Fig. 2 source CSV: `post_run/analysis_exports/50k/figure_ready/figure_agreement_surplus_by_bin_model_50k.csv`
- Fig. 3 source CSV: `post_run/analysis_exports/50k/figure_ready/figure_distribution_gap_by_bin_model_50k.csv`
- Fig. 4 source CSV: `post_run/analysis_exports/50k/figure_ready/figure_sampling_compression_by_bin_model_50k.csv`
- CI table: `post_run/analysis_exports/50k/manuscript_tables/table_primary_results_with_ci_50k.csv`
- Contrast table: `post_run/analysis_exports/50k/manuscript_tables/table_primary_contrasts_with_ci_50k.csv`

Traceability findings from original audit:

- All all-model means in Figs. 2–4 match the corresponding figure-ready CSV rows.
- All all-model means also match `table_primary_results_with_ci_50k.csv`.
- CIs are read from `table_primary_results_with_ci_50k.csv`; no new CIs were computed for figure polish.
- Moderate-consensus rows have means but no CI bounds in the table, and the figure/checklist correctly state that no invented CIs were added.
- Figure-ready CSVs and manuscript tables have 2026-06-21 timestamps, while polished rendered figures and validation notes have 2026-06-24 timestamps, consistent with figure polish not changing source CSVs or manuscript tables.

Gap fixed:

- The submission package should copy only the source-data files actually needed to support the manuscript figures/tables, plus an inventory explaining why each file is included.
- Do not copy raw SCRUPLES anecdotes or raw provider responses into source data.
- Add checksums for copied package artifacts so the curated package can be compared with the repo source.

Recommended checksum command after copying:

```bash
python - <<'PY'
from pathlib import Path
import hashlib
root = Path("submission")
for p in sorted(root.rglob("*")):
    if p.is_file():
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        print(f"{h}  {p.as_posix()}")
PY
```

Save the output as `submission/package_checksums_sha256.txt`.

## 6. Caption and cross-reference status

Main manuscript captions/callouts are present for:

- Fig. 1
- Fig. 2
- Fig. 3
- Fig. 4
- Table 1
- Table 2
- Extended Data Fig. 1
- Extended Data Fig. 2
- Extended Data Fig. 3
- Extended Data Table 1

Alignment checks from original audit:

- Fig. 3 is described as the same model, same item and same selected/verdict label.
- Fig. 4 is described in bits.
- Low-consensus is described as primary.
- Diffuse/no-clear-consensus is described as secondary and separate.
- High-consensus is described as a positive reference condition, not a null or unaffected condition.
- Distribution diagnostics are described as support/diagnostics, not proof of perfect calibration.
- Paraphrase is described as aggregate surface-form evidence with limited matched coverage, not as contamination exclusion or strong paired robustness.
- Validity is described as supporting transparency/exclusions, not a primary endpoint.

Gap fixed:

- Markdown callouts still need conversion into LaTeX labels and references. During conversion, each callout should become a stable `\label{}`/`\ref{}` or controlled textual citation.
- Table 1 has subparts (`Table 1a`, `Table 1b`) that may need careful LaTeX handling so the rendered PDF does not confuse them with separate main display items.
- Extended Data references should remain Extended Data references and should not be counted as main display items.
- The LaTeX PDF should be searched for unresolved references and citations.

Suggested label scheme:

```text
fig:study-design
fig:agreement-surplus
fig:distribution-agreement-gap
fig:sampling-compression
tab:model-roster-allocation
tab:primary-endpoints
edfig:distribution-quality
edfig:paraphrase-audit
edfig:validity
edtab:validity-exclusions
```

## 7. Claim-discipline guardrails

Original audit conclusion remains sound: current manuscript/SI wording does not appear to claim moral truth, universal representativeness, contamination exclusion, strong paired paraphrase robustness, provider-family effects, model-family effects, normative certainty as a primary endpoint, high-consensus as null/unaffected, distribution-mode perfect recovery or repeated temperature-0 calls as latent model-distribution sampling.

Gap fixed:

- Add one more conversion-specific guardrail: LaTeX conversion must be treated as format conversion, not prose revision. The converter should not “improve” scientific claims, rewrite captions, shorten limitations, change endpoint definitions or rephrase caveats unless a separate manuscript revision task explicitly asks for it.
- After conversion, run a text diff between `submission/manuscript.md` and the extracted/converted `main.tex` prose where feasible, focusing on numbers, endpoint definitions and caveats.

Numbers that should not change:

- target calls: 47,500;
- primary-valid outputs: 47,432;
- agreement surplus low-consensus mean: 0.370931;
- distribution-agreement gap low-consensus mean: 0.232687;
- sampling compression low-consensus mean: 1.264638 bits;
- adjusted primary P values: 0.0015;
- paraphrase valid outputs: 2,495 of 2,500;
- no repaired outputs entered the final analysis;
- contamination was not directly measured.

## 8. Bibliography and references readiness

Findings:

- No `.bib` file found.
- No `.bbl` file found.
- No `main.tex`, `sn-jnl.cls`, `.bst`, `.csl` or LaTeX folder found.
- References are embedded in `article/nmi_moral_overresolution_draft_50k_v5.md` as numbered Markdown references `[1-8]`.
- No Pandoc citation keys such as `[@key]` were found in the current manuscript or SI.
- No obvious `TODO`, `TBD`, `PLACEHOLDER`, `CITE` or `citation needed` markers were found in the current manuscript or SI.

Gap fixed:

- Creating `references.bib` is the first required packaging task, not a cosmetic task.
- Decide before conversion whether to use BibTeX/BibLaTeX citation keys or a controlled manual `thebibliography`. BibTeX is preferable for maintainability; manual bibliography is simpler but more fragile if references are reordered.
- Verify all eight references against DOI/publisher pages before freezing BibTeX. Do not invent missing metadata, provider/model citations or model snapshot citations.
- Create a citation mapping table before touching the manuscript:

| Current number | Proposed key | Reference |
|---:|---|---|
| 1 | `jiang2025delphi` | Jiang et al., Delphi experiment |
| 2 | `steyvers2025whatllmsknow` | Steyvers et al., what LLMs know |
| 3 | `kumaran2026competingbiases` | Kumaran et al., overconfidence/underconfidence |
| 4 | `lourie2021scruples` | SCRUPLES |
| 5 | `abdulhai2023moralfoundations` | Moral foundations of LLMs |
| 6 | `takemoto2024moralmachine` | Moral machine experiment on LLMs |
| 7 | `zaimtakemoto2025largescale` | Large-scale moral machine experiment |
| 8 | `sclar2024promptformatting` | Prompt formatting sensitivity |

Potential citation conversion approaches:

1. Convert inline citations such as `[1-7]` to `\citep{jiang2025delphi,steyvers2025whatllmsknow,kumaran2026competingbiases,lourie2021scruples,abdulhai2023moralfoundations,takemoto2024moralmachine,zaimtakemoto2025largescale}`.
2. Convert to journal-template-native citation macros after the selected template is installed.
3. Use a manual numbered bibliography only if the template or submission route makes BibTeX unnecessary.

## 9. LaTeX readiness status

Findings:

- No LaTeX workspace exists.
- No `main.tex` exists.
- No Nature/Springer class file such as `sn-jnl.cls` exists.
- No compiled manuscript PDF exists.
- No Pandoc conversion script exists.
- No bibliography build outputs exist.

Gap fixed:

- The next step should build a minimal reproducible LaTeX workspace before extensive manual polishing.
- Add a build script and build log capture so LaTeX issues are repeatable.

Recommended LaTeX workspace:

```text
submission/
  manuscript.md
  supplementary_information.md
  references.bib
  package_manifest.md
  package_file_list.txt
  package_checksums_sha256.txt
  figures/
    editable/
    final/
    preview/
  source_data/
  latex/
    main.tex
    supplementary_information.tex
    references.bib
    latexmkrc
    Makefile or build.ps1
    build_logs/
```

Recommended initial build command:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Recommended Windows PowerShell wrapper:

```powershell
$ErrorActionPreference = "Stop"
Set-Location submission/latex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex 2>&1 | Tee-Object -FilePath build_logs/build_latest.log
```

Recommended cleanup command:

```bash
latexmk -c
```

If using MiKTeX on Windows, install/update packages through MiKTeX Console or allow missing packages to install automatically. If using TeX Live, install a full distribution or document any packages needed by the Springer/Nature template.

## 10. Recommended Windows/VSCode LaTeX review setup

Best default setup:

- **TeX distribution:** MiKTeX or TeX Live. On Windows, MiKTeX is convenient because it can install missing packages automatically.
- **VSCode extension:** LaTeX Workshop for editing, building and PDF preview.
- **LaTeX linter:** ChkTeX for common LaTeX/typographic issues that a normal compile may not catch.
- **Language/style checker:** LTeX+ or another LanguageTool-based extension for prose issues, with scientific terms added to the dictionary to avoid noise.
- **Formatter:** `latexindent` for controlled indentation of `.tex` files, but do not run it blindly on tables until the build is stable.
- **Desktop app fallback:** TeXstudio. It is useful for side-by-side source/PDF inspection, syntax highlighting, live reference/citation checking and an integrated PDF viewer.

Recommendation:

- Use VSCode + LaTeX Workshop as the primary workflow because the repo already uses code and generated assets.
- Install TeXstudio as a secondary reviewer because it catches some reference/citation/navigation issues visually and is often easier for manual PDF-source inspection.
- Do not rely on any single tool. The minimum reliable QA loop is compile + log review + ChkTeX + manual PDF inspection.

## 11. LaTeX QA gates before calling the package “ready”

A compiled PDF is necessary but not sufficient. The package should pass these gates.

Compile gate:

- `latexmk` completes without fatal errors.
- No unresolved references.
- No unresolved citations.
- No “rerun to get cross-references right” warnings remain after `latexmk`.
- Bibliography is generated correctly and appears in the intended style.

Log gate:

Search the `.log` and captured build output for:

```text
Undefined control sequence
LaTeX Error
Package Error
Citation
Reference
undefined
multiply defined
Overfull \hbox
Underfull \hbox
Float too large
Rerun
Missing character
Font shape
```

Manual PDF gate:

- Page order is correct.
- Title/author/affiliation/ORCID/corresponding author fields render correctly.
- Abstract remains within NMI’s 150-word limit by the chosen counting method.
- Introduction appears without a visible “Introduction” heading if following NMI Article style.
- Results and Methods have subheadings; Discussion has no subheadings.
- Main display count remains six: Figs. 1–4 and Tables 1–2.
- Tables are readable and not overflowing.
- Figure captions are paired with the correct figures.
- Extended Data and Supplementary Information are clearly separated from the main article.
- Hyperlinks, DOIs and cross-references work.
- No restricted raw anecdote text or raw provider responses appear in public package files.

Optional automated QA:

```bash
chktex -q main.tex
```

Use ChkTeX warnings as prompts for review, not as mandatory edits. Some warnings will be false positives for scientific notation, URLs, tables or template macros.

## 12. Recommended folder/package structure

Use `submission/`, not `paper/`, for the clean package unless `.gitignore` is intentionally changed.

Recommended structure:

```text
submission/
  manuscript.md
  supplementary_information.md
  references.bib
  package_manifest.md
  figures/
    src/
      render_final_figures.py
    editable/
      fig1_study_design.svg
      fig2_agreement_surplus.svg
      fig3_distribution_agreement_gap.svg
      fig4_sampling_compression.svg
      edfig1_distribution_quality.svg
      edfig2_paraphrase_audit.svg
      edfig3_validity.svg
    final/
      fig1_study_design.pdf
      fig1_study_design.svg
      fig2_agreement_surplus.pdf
      fig2_agreement_surplus.svg
      fig3_distribution_agreement_gap.pdf
      fig3_distribution_agreement_gap.svg
      fig4_sampling_compression.pdf
      fig4_sampling_compression.svg
      edfig1_distribution_quality.pdf
      edfig1_distribution_quality.svg
      edfig2_paraphrase_audit.pdf
      edfig2_paraphrase_audit.svg
      edfig3_validity.pdf
      edfig3_validity.svg
    preview/
      fig1_study_design.png
      fig2_agreement_surplus.png
      fig3_distribution_agreement_gap.png
      fig4_sampling_compression.png
      edfig1_distribution_quality.png
      edfig2_paraphrase_audit.png
      edfig3_validity.png
  latex/
    main.tex
    supplementary_information.tex
    references.bib
    latexmkrc
    build.ps1
    build_logs/
  source_data/
    figure_source_inventory_50k.md
    final_figure_export_checklist_50k.md
    quantitative_figure_numerical_validation_50k.txt
    figure_ready/
    manuscript_tables/
```

Notes:

- Include both SVG and PDF for main and Extended Data final figures.
- Keep PNGs available for preview only.
- Do not copy local style-reference images into `submission/`.
- Do not copy restricted materials into `submission/`.
- Include source-data CSVs only if they are release-safe derived files.

## 13. Done

Items that appear complete and should be frozen unless explicitly reopened:

- Current main manuscript in `article/nmi_moral_overresolution_draft_50k_v5.md`.
- Current SI in `article/nmi_supplementary_information_50k_v2.md`.
- Final rendered figure package in `post_run/analysis_exports/50k/rendered_figures/`.
- Figure source inventory in `post_run/analysis_exports/50k/figure_source_inventory_50k.md`.
- Final figure export checklist in `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`.
- Quantitative figure numerical validation in `post_run/analysis_exports/50k/quantitative_figure_numerical_validation_50k.txt`.
- Figure-ready CSVs in `post_run/analysis_exports/50k/figure_ready/`.
- Manuscript tables in `post_run/analysis_exports/50k/manuscript_tables/`.
- 50k analysis manifest and derived analysis exports.
- Figure rendering source in `src/analysis/render_final_figures.py`.

## 14. Needs small fix before LaTeX

- Create `references.bib`.
- Choose stable citation keys and convert numbered Markdown citations safely.
- Create `submission/` as the clean package root and verify it is not ignored.
- Copy canonical manuscript/SI into `submission/` under stable filenames.
- Copy final figure assets and release-safe source-data assets into `submission/`.
- Create a package manifest and checksums.
- Confirm older pre-polish audit notes will not be treated as controlling over the final figure checklist.
- Do one final manual visual review of all rendered PDFs/SVGs, especially Fig. 1.

## 15. Needs LaTeX setup

- Create `submission/latex/`.
- Add `main.tex`.
- Add `supplementary_information.tex` or a separate SI PDF workflow.
- Add selected Springer Nature/NMI-compatible template/class files if needed and if redistribution is permitted.
- Add `references.bib`.
- Add `latexmkrc`.
- Add `build.ps1` or `Makefile`.
- Convert numbered Markdown references to citation keys or a controlled manual bibliography.
- Add figure inclusion paths for final PDFs.
- Build and inspect compiled PDF.
- Save build logs.

## 16. Needs submission package later

- Cover letter, currently only as ignored/local draft: `drafts/nmi_cover_letter_50k.md`.
- Submission checklist, currently ignored/local: `drafts/nmi_submission_checklist_custom.md`.
- Journal upload manifest.
- Final source-data package mapping.
- Final data/code availability text matched to uploaded archive/release.
- Any required author forms, reporting summaries or editorial declarations.
- Word/PDF version if the author chooses an initial-submission format outside LaTeX.

## 17. Do not touch

Unless explicitly instructed later, do not modify:

- `data/scruples/`
- `runs/`
- `drafts/style_reference/`
- `drafts/` historical review/planning files
- raw provider responses, full run stores or restricted materials
- figure-ready CSVs
- manuscript-table CSVs
- final rendered figure assets
- current canonical manuscript/SI text
- source analysis code

## 18. Files that should be committed

Tracked package files that should remain committed:

- `article/nmi_moral_overresolution_draft_50k_v5.md`
- `article/nmi_supplementary_information_50k_v2.md`
- `src/analysis/render_final_figures.py`
- `src/analysis/final_50k_exports.py`
- `post_run/analysis_exports/50k/figure_ready/*.csv`
- `post_run/analysis_exports/50k/manuscript_tables/*.csv`
- `post_run/analysis_exports/50k/rendered_figures/*.{svg,png,pdf}`
- `post_run/analysis_exports/50k/figure_source_inventory_50k.md`
- `post_run/analysis_exports/50k/final_figure_export_checklist_50k.md`
- `post_run/analysis_exports/50k/quantitative_figure_numerical_validation_50k.txt`
- `post_run/analysis_exports/50k/quantitative_figure_polish_implementation_50k.md`
- `post_run/analysis_exports/50k/analysis_export_manifest_50k.json`
- `post_run/analysis_exports/50k/workspace_completion_audit_50k.md`

Future files to commit after explicit creation:

- `submission/manuscript.md`
- `submission/supplementary_information.md`
- `submission/package_manifest.md`
- `submission/package_file_list.txt`
- `submission/package_checksums_sha256.txt`
- `submission/references.bib`
- `submission/latex/main.tex`
- `submission/latex/supplementary_information.tex`
- `submission/latex/latexmkrc`
- `submission/latex/build.ps1` or `submission/latex/Makefile`
- selected LaTeX template/class files if redistribution is permitted
- curated submission figures and source-data copies

## 19. Files that should stay untracked/ignored

- `drafts/style_reference/nmi_figures/*.webp`
- other files under `drafts/` unless explicitly promoted
- `runs/`
- `data/scruples/`
- `.tmp_pytest/`
- `__pycache__/`
- `.env` and `.env.*` except `.env.example`
- raw provider responses, full call ledgers, full run stores and restricted/mixed materials
- LaTeX auxiliary files such as `.aux`, `.log`, `.out`, `.toc`, `.lof`, `.lot`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, `.blg` and temporary build artifacts, except saved audit logs intentionally placed in `build_logs/`

## 20. Files not to modify

Do not modify these in the next packaging step unless the task explicitly asks for it:

- `article/nmi_moral_overresolution_draft_50k_v5.md`
- `article/nmi_supplementary_information_50k_v2.md`
- `post_run/analysis_exports/50k/figure_ready/*.csv`
- `post_run/analysis_exports/50k/manuscript_tables/*.csv`
- `post_run/analysis_exports/50k/rendered_figures/*`
- `src/analysis/render_final_figures.py`
- `src/analysis/final_50k_exports.py`
- `data/scruples/*`
- `runs/*`
- `drafts/style_reference/*`

## 21. Prioritized next steps

1. Create `references.bib` from the eight embedded Markdown references and choose stable citation keys.
2. Create `submission/` as the clean package root, not `paper/`, unless `.gitignore` is intentionally changed.
3. Copy current canonical manuscript/SI, final figures, figure inventory and relevant source-data tables into `submission/`.
4. Add `submission/package_manifest.md`, `submission/package_file_list.txt` and `submission/package_checksums_sha256.txt`.
5. Convert the manuscript and SI to LaTeX in `submission/latex/`.
6. Add `latexmkrc` and a Windows-friendly build script.
7. Build and inspect a compiled PDF.
8. Run LaTeX log/reference/citation/overfull-box QA.
9. Run ChkTeX as advisory linting.
10. Prepare cover letter and final submission checklist after the LaTeX/PDF build works.

## 22. Clear recommendation for the next Codex task

Next Codex task:

> Create `submission/` as a clean package root, verify it is not ignored, copy the canonical manuscript/SI and final release-safe figure/source-data assets into it, create `references.bib` from the eight numbered references, and add a package manifest plus checksums. Then start LaTeX conversion in `submission/latex/` with `main.tex`, `supplementary_information.tex`, `latexmkrc` and a Windows-friendly build script. Build the PDF, save the build log, and report unresolved references, unresolved citations, overfull boxes and any visual issues.

Rationale:

- The science, figures and source-data mappings are ready enough to freeze.
- The biggest blockers are bibliography structure, clean package layout, LaTeX build infrastructure and manual visual/log QA.
- This should be treated as package construction, not scientific manuscript revision.
