# Build notes

This package was generated from the latest uploaded manuscript markdown.

From `submission/latex/`, build with:

```powershell
latexmk -xelatex main.tex
latexmk -xelatex supplementary_information.tex
```

or:

```powershell
.\build.ps1 -Target all
```

This is a simple article-style PDF build for review/local inspection, not a final Nature/Springer production template. Figure files and release-safe source-data files must be copied from the repository before final submission packaging.
