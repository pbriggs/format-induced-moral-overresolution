@echo off
setlocal

cd /d "%~dp0"

if "%~1"=="" (
  set "MILESTONE=3k"
) else (
  set "MILESTONE=%~1"
)

if "%RUN_ID%"=="" (
  if "%MOCK_PROVIDER%"=="1" (
    set "RUN_ID=mock_smoke_v1"
  ) else if "%MILESTONE%"=="1" (
    set "RUN_ID=engineering_shakedown_v1"
  ) else if "%MILESTONE%"=="10" (
    set "RUN_ID=engineering_shakedown_v1"
  ) else if "%MILESTONE%"=="50" (
    set "RUN_ID=engineering_shakedown_v1"
  ) else (
    set "RUN_ID=production_milestones_cumulative_v1"
  )
)
if "%OUT_DIR%"=="" set "OUT_DIR=runs"
if "%SUBSET_SEED%"=="" set "SUBSET_SEED=20260615"
if "%SCRUPLES_SPLITS%"=="" set "SCRUPLES_SPLITS=train,dev,test"
if "%SHARD_COUNT%"=="" set "SHARD_COUNT=20"

for %%S in (%SCRUPLES_SPLITS:,= %) do (
  if not exist "data\scruples\anecdotes\%%S.scruples-anecdotes.jsonl" (
    echo Missing SCRUPLES split file: data\scruples\anecdotes\%%S.scruples-anecdotes.jsonl
    echo See docs\DATA_SETUP.md. Run this script from the repository root after placing the local SCRUPLES files.
    exit /b 3
  )
)

if "%STUDY_MODEL_IDS%"=="" (
  echo STUDY_MODEL_IDS must be set to exactly five comma-separated frozen model IDs.
  exit /b 2
)

set "PYTHONPATH=src"
set "PYTHONDONTWRITEBYTECODE=1"

set "MOCK_FLAG="
if "%MOCK_PROVIDER%"=="1" set "MOCK_FLAG=--mock-provider"

set "SKIP_MODEL_FLAG="
if not "%SKIP_MODEL_IDS%"=="" set "SKIP_MODEL_FLAG=--skip-model-ids %SKIP_MODEL_IDS%"

python -m production.execute_milestone ^
  --milestone "%MILESTONE%" ^
  --run-id "%RUN_ID%" ^
  --out-dir "%OUT_DIR%" ^
  --splits "%SCRUPLES_SPLITS%" ^
  --seed "%SUBSET_SEED%" ^
  --models "%STUDY_MODEL_IDS%" ^
  --shard-count "%SHARD_COUNT%" ^
  %SKIP_MODEL_FLAG% ^
  %MOCK_FLAG%

endlocal
