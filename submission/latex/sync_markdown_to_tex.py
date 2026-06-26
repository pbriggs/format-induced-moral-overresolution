from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "article" / "nmi_moral_overresolution_draft_50k_v5.md"
OUT = Path(__file__).resolve().parent / "main.tex"

def esc(s: str) -> str:
    s = html.unescape(s)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    s = s.replace("—", "---").replace("–", "--")
    s = s.replace("“", "``").replace("”", "''").replace("’", "'")
    return s

def inline_md(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*(.+?)\*", r"\\emph{\1}", s)
    s = re.sub(r"`(.+?)`", r"\\texttt{\1}", s)
    return s

def front_matter_value(line: str):
    match = re.match(r"^\*\*(.+?):\*\*\s*(.*?)\s*$", line.strip())
    if not match:
        return None
    key = match.group(1).strip().lower()
    value = match.group(2).strip()
    return key, value

def table_to_latex(lines):
    rows = []
    for line in lines:
        cells = [inline_md(c.strip()) for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return ""
    colspec = "p{0.22\\linewidth}" + "p{0.14\\linewidth}" * (len(rows[0]) - 1)
    out = [r"\begin{landscape}", r"\small", rf"\begin{{longtable}}{{{colspec}}}"]
    out.append(r" \toprule")
    out.append(" & ".join(rows[0]) + r" \\")
    out.append(r" \midrule")
    for r in rows[1:]:
        out.append(" & ".join(r) + r" \\")
    out.append(r" \bottomrule")
    out.append(r"\end{longtable}")
    out.append(r"\normalsize")
    out.append(r"\end{landscape}")
    return "\n".join(out)

def convert(md: str) -> str:
    md = md.lstrip("\ufeff")
    lines = md.splitlines()
    body = []
    in_code = False
    code = []
    i = 0

    title = esc(lines[0].lstrip("# ").strip()) if lines and lines[0].startswith("# ") else "Manuscript"
    metadata = {}
    metadata_end = 1 if lines and lines[0].startswith("# ") else 0

    while metadata_end < len(lines) and not lines[metadata_end].strip():
        metadata_end += 1

    while metadata_end < len(lines):
        item = front_matter_value(lines[metadata_end])
        if not item:
            break
        key, value = item
        metadata[key] = value
        metadata_end += 1

    while metadata_end < len(lines) and not lines[metadata_end].strip():
        metadata_end += 1

    author_lines = [
        esc(metadata.get("author", "Paul Briggs")),
        esc(metadata.get("affiliation", "Independent researcher, Los Angeles, CA, USA")),
    ]
    if metadata.get("corresponding author"):
        author_lines.append("Corresponding author: " + esc(metadata["corresponding author"]))
    if metadata.get("orcid"):
        author_lines.append(r"ORCID: \url{" + metadata["orcid"].strip() + "}")
    author_block = r"\\".join(author_lines)

    preamble = rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{hyperref}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{array}}
\usepackage{{pdflscape}}
\usepackage{{graphicx}}
\usepackage{{caption}}
\usepackage{{float}}
\usepackage{{xurl}}
\hypersetup{{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue}}
\title{{{title}}}
\author{{{author_block}}}
\date{{}}
\begin{{document}}
\maketitle
"""

    while i < len(lines):
        line = lines[i]

        if i < metadata_end:
            i += 1
            continue

        if line.startswith("# "):
            i += 1
            continue

        if line.startswith("```"):
            if not in_code:
                in_code = True
                code = []
            else:
                body.append(r"\begin{verbatim}")
                body.extend(code)
                body.append(r"\end{verbatim}")
                in_code = False
            i += 1
            continue

        if in_code:
            code.append(line)
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and lines[i + 1].startswith("|"):
            table_lines = [line]
            i += 2  # skip separator
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            body.append(table_to_latex(table_lines))
            continue

        if line.startswith("## Abstract"):
            body.append(r"\begin{abstract}")
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                if lines[i].strip():
                    body.append(inline_md(lines[i].strip()))
                    body.append("")
                i += 1
            body.append(r"\end{abstract}")
            continue

        if line.startswith("## Main"):
            i += 1
            continue

        if line.startswith("## "):
            body.append(r"\section{" + inline_md(line[3:].strip()) + "}")
        elif line.startswith("### "):
            body.append(r"\subsection{" + inline_md(line[4:].strip()) + "}")
        elif line.strip() == "":
            body.append("")
        else:
            body.append(inline_md(line.strip()))

        i += 1

    return preamble + "\n".join(body) + "\n\\end{document}\n"

if not SRC.exists():
    raise SystemExit(f"Missing source markdown: {SRC}")

tex = convert(SRC.read_text(encoding="utf-8-sig"))
OUT.write_text(tex, encoding="utf-8")
print(f"Wrote {OUT}")
