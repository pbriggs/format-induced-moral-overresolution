@echo off
setlocal

cd /d "%~dp0"

echo Building main manuscript...
powershell -NoProfile -ExecutionPolicy Bypass -Command "latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex"
if errorlevel 1 goto fail

echo Building supplementary information...
powershell -NoProfile -ExecutionPolicy Bypass -Command "latexmk -xelatex -interaction=nonstopmode -halt-on-error supplementary_information.tex"
if errorlevel 1 goto fail

echo Opening PDFs...
start "" "%CD%\main.pdf"
start "" "%CD%\supplementary_information.pdf"

echo Done.
exit /b 0

:fail
echo.
echo Build failed. Check main.log or supplementary_information.log.
pause
exit /b 1