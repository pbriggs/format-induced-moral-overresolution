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
if "%MAX_SHARD_RUNS%"=="" set "MAX_SHARD_RUNS=999"

set "PYTHONPATH=src"
set "PYTHONDONTWRITEBYTECODE=1"

set /a RUN_COUNT=0

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

python -c "import json, pathlib, sys; out=pathlib.Path(r'%OUT_DIR%') / r'%RUN_ID%'; summary_path=out / 'execution_summary_%MILESTONE%.json'; summary=json.loads(summary_path.read_text(encoding='utf-8')) if summary_path.exists() else {}; status=summary.get('status'); print('last executor status:', status); sys.exit(20 if status in {'failed','aborted'} else 0)"
if errorlevel 20 (
  echo Stopping because the last shard did not pass.
  exit /b 20
)
if errorlevel 1 exit /b %errorlevel%

python -c "import json, pathlib, sys; shard_dir=pathlib.Path(r'%OUT_DIR%') / r'%RUN_ID%' / 'execution_shards' / r'%MILESTONE%'; states=[json.loads(path.read_text(encoding='utf-8')) for path in sorted(shard_dir.glob('*.state.json'))]; active=[state for state in states if state.get('planned_calls',0)>0]; pending=[state for state in active if state.get('status')!='passed']; print(f'shard status: passed={len(active)-len(pending)} pending_or_failed={len(pending)} active={len(active)} total={len(states)}'); sys.exit(0 if pending else 30)"
if errorlevel 30 (
  echo All executable shards for %MILESTONE% are passed.
  exit /b 0
)
if errorlevel 1 exit /b %errorlevel%

goto loop
