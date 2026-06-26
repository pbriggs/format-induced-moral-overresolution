@echo off
setlocal EnableExtensions

cd /d "%~dp0"

echo.
echo === Syncing Markdown to LaTeX ===
python sync_markdown_to_tex.py
if errorlevel 1 goto fail

echo.
echo === Cleaning stale main build files ===
latexmk -c main.tex

echo.
echo === Building main manuscript ===
powershell -NoProfile -ExecutionPolicy Bypass -Command "latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex"
if errorlevel 1 goto fail

if exist "supplementary_information.tex" (
  echo.
  echo === Building supplementary information ===
  powershell -NoProfile -ExecutionPolicy Bypass -Command "latexmk -xelatex -interaction=nonstopmode -halt-on-error supplementary_information.tex"
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
