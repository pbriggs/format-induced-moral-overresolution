@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "MIKTEX_BIN=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64"
if exist "%MIKTEX_BIN%\pdflatex.exe" set "PATH=%MIKTEX_BIN%;%PATH%"

echo.
echo === Syncing Markdown to LaTeX ===
python sync_markdown_to_tex.py
if errorlevel 1 goto fail

echo.
echo === Checking LaTeX engines ===
where pdflatex >nul 2>nul
if errorlevel 1 goto fail
where xelatex >nul 2>nul
if errorlevel 1 goto fail

echo.
echo === Building main manuscript ===
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if errorlevel 1 goto fail
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if errorlevel 1 goto fail

if exist "supplementary_information.tex" (
  echo.
  echo === Building supplementary information ===
  xelatex -interaction=nonstopmode -halt-on-error supplementary_information.tex
  if errorlevel 1 goto fail
  xelatex -interaction=nonstopmode -halt-on-error supplementary_information.tex
  if errorlevel 1 goto fail
)

echo.
echo === Opening PDFs ===
if exist "main.pdf" start "" "%CD%\main.pdf"
if exist "supplementary_information.pdf" start "" "%CD%\supplementary_information.pdf"

echo Done.
exit /b 0

:fail
echo.
echo Build failed. Check main.log.
pause
exit /b 1
