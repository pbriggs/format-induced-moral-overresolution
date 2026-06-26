param([ValidateSet('main','si','all')] [string]$Target='all')
if ($Target -eq 'main' -or $Target -eq 'all') { latexmk -xelatex main.tex }
if ($Target -eq 'si' -or $Target -eq 'all') { latexmk -xelatex supplementary_information.tex }
