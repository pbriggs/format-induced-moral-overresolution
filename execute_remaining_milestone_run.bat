@echo off
setlocal EnableDelayedExpansion

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
if "%MAX_SHARD_RUNS%"=="" set "MAX_SHARD_RUNS=999"
if "%MAX_RETRYABLE_FAILURE_PASSES%"=="" set "MAX_RETRYABLE_FAILURE_PASSES=10"
if "%RETRYABLE_FAILURE_PAUSE_SECONDS%"=="" set "RETRYABLE_FAILURE_PAUSE_SECONDS=120"

set "PYTHONPATH=src"
set "PYTHONDONTWRITEBYTECODE=1"

set /a RUN_COUNT=0
set /a RETRYABLE_FAILURE_COUNT=0

:loop
set /a RUN_COUNT+=1
if %RUN_COUNT% GTR %MAX_SHARD_RUNS% (
  echo Reached MAX_SHARD_RUNS=%MAX_SHARD_RUNS%; stopping.
  exit /b 4
)

echo.
echo ===== Executing %MILESTONE% shard pass %RUN_COUNT% =====
call "%~dp0execute_milestone_run.bat" "%MILESTONE%"
if errorlevel 1 exit /b %errorlevel%

python -c "import json, pathlib, sys; out=pathlib.Path(r'%OUT_DIR%') / r'%RUN_ID%'; summary_path=out / 'execution_summary_%MILESTONE%.json'; summary=json.loads(summary_path.read_text(encoding='utf-8')) if summary_path.exists() else {}; status=summary.get('status'); print('last executor status:', status); sys.exit({'aborted':20,'failed':21}.get(status,0))"
if errorlevel 21 (
  python -m production.progress_status --out-dir "%OUT_DIR%" --run-id "%RUN_ID%" --milestone "%MILESTONE%"
  python -c "import pathlib, sqlite3, sys; db=pathlib.Path(r'%OUT_DIR%') / r'%RUN_ID%' / 'study.sqlite'; con=sqlite3.connect(db); row=con.execute('select count(distinct api_call_id) from api_calls_raw where run_id=? and milestone=? and api_error_flag=1 and terminal_failure_flag=1', (r'%RUN_ID%', r'%MILESTONE%')).fetchone(); con.close(); sys.exit(31 if row[0] == 0 else 20)"
  if errorlevel 31 (
    set /a RETRYABLE_FAILURE_COUNT+=1
    if !RETRYABLE_FAILURE_COUNT! GTR %MAX_RETRYABLE_FAILURE_PASSES% (
      echo Reached MAX_RETRYABLE_FAILURE_PASSES=%MAX_RETRYABLE_FAILURE_PASSES%; stopping.
      exit /b 31
    )
    echo Last shard failed only with retryable non-terminal API errors. Waiting %RETRYABLE_FAILURE_PAUSE_SECONDS% seconds, then retrying.
    timeout /t %RETRYABLE_FAILURE_PAUSE_SECONDS% /nobreak
    goto loop
  )
  echo Stopping because the failed shard included terminal API failures.
  exit /b 20
)
if errorlevel 20 (
  python -m production.progress_status --out-dir "%OUT_DIR%" --run-id "%RUN_ID%" --milestone "%MILESTONE%"
  echo Stopping because the last shard aborted.
  exit /b 20
)
if errorlevel 1 exit /b %errorlevel%

set /a RETRYABLE_FAILURE_COUNT=0

python -m production.progress_status --out-dir "%OUT_DIR%" --run-id "%RUN_ID%" --milestone "%MILESTONE%"
if errorlevel 30 (
  echo All executable shards for %MILESTONE% are passed.
  exit /b 0
)
if errorlevel 1 exit /b %errorlevel%

goto loop
