@echo off
setlocal

cd /d "%~dp0"

if "%~1"=="" (
  set "MILESTONE=3k"
) else (
  set "MILESTONE=%~1"
)

if "%RUN_ID%"=="" set "RUN_ID=production_milestones_cumulative_v1"
if "%OUT_DIR%"=="" set "OUT_DIR=runs"

if "%STUDY_MODEL_IDS%"=="" (
  echo STUDY_MODEL_IDS must be set to exactly five comma-separated model IDs.
  exit /b 2
)

set "PYTHONPATH=src"
set "PYTHONDONTWRITEBYTECODE=1"

set "MOCK_FLAG="
if "%MOCK_PROVIDER%"=="1" set "MOCK_FLAG=--mock-provider"

set "HELPER_MODEL_FLAG="
if not "%PARAPHRASE_HELPER_MODEL_ID%"=="" set "HELPER_MODEL_FLAG=--helper-model %PARAPHRASE_HELPER_MODEL_ID%"

set "MAX_ITEMS_FLAG="
if not "%PARAPHRASE_MAX_ITEMS%"=="" set "MAX_ITEMS_FLAG=--max-items %PARAPHRASE_MAX_ITEMS%"

python -m production.materialize_paraphrases ^
  --milestone "%MILESTONE%" ^
  --run-id "%RUN_ID%" ^
  --out-dir "%OUT_DIR%" ^
  --models "%STUDY_MODEL_IDS%" ^
  %HELPER_MODEL_FLAG% ^
  %MAX_ITEMS_FLAG% ^
  %MOCK_FLAG%

endlocal
