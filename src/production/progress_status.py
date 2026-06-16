from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
import sys
from typing import Any


def _json_loads(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _count_shards(out_dir: Path, run_id: str, milestone: str) -> dict[str, int]:
    shard_dir = out_dir / run_id / "execution_shards" / milestone
    states = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(shard_dir.glob("*.state.json"))
        if path.exists()
    ]
    active = [state for state in states if int(state.get("planned_calls") or 0) > 0]
    pending = [state for state in active if state.get("status") != "passed"]
    return {
        "passed": len(active) - len(pending),
        "pending_or_failed": len(pending),
        "active": len(active),
        "total": len(states),
    }


def _db_progress(db_path: Path, run_id: str, milestone: str) -> dict[str, int | str]:
    if not db_path.exists():
        return {
            "planned": 0,
            "completed_successful": 0,
            "api_errors": 0,
            "terminal_failures": 0,
            "left_total": 0,
            "provider_executable_left": 0,
            "prework_blocked_left": 0,
            "integrity": "missing_db",
        }
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        integrity = str(connection.execute("PRAGMA integrity_check").fetchone()[0])
        raw_rows = connection.execute(
            """
            SELECT api_call_id, api_error_flag, terminal_failure_flag
            FROM api_calls_raw
            WHERE run_id = ? AND milestone = ?
            """,
            (run_id, milestone),
        ).fetchall()
        successful = {str(row["api_call_id"]) for row in raw_rows if not row["api_error_flag"]}
        terminal = {str(row["api_call_id"]) for row in raw_rows if row["terminal_failure_flag"]}
        api_errors = {str(row["api_call_id"]) for row in raw_rows if row["api_error_flag"]}
        planned_rows = connection.execute(
            """
            SELECT api_call_id, request_json
            FROM planned_api_calls
            WHERE run_id = ? AND milestone = ?
            """,
            (run_id, milestone),
        ).fetchall()
        pending_rows = [
            row
            for row in planned_rows
            if str(row["api_call_id"]) not in successful and str(row["api_call_id"]) not in terminal
        ]
        prework_blocked = sum(1 for row in pending_rows if _json_loads(row["request_json"]).get("prework_required"))
        return {
            "planned": len(planned_rows),
            "completed_successful": len(successful),
            "api_errors": len(api_errors),
            "terminal_failures": len(terminal),
            "left_total": len(pending_rows),
            "provider_executable_left": len(pending_rows) - prework_blocked,
            "prework_blocked_left": prework_blocked,
            "integrity": integrity,
        }
    finally:
        connection.close()


def print_progress(out_dir: Path, run_id: str, milestone: str) -> int:
    run_dir = out_dir / run_id
    db_path = run_dir / "study.sqlite"
    db_progress = _db_progress(db_path, run_id, milestone)
    shard_progress = _count_shards(out_dir, run_id, milestone)
    print(
        "full milestone progress: "
        f"completed={db_progress['completed_successful']}/{db_progress['planned']} "
        f"left_total={db_progress['left_total']} "
        f"provider_executable_left={db_progress['provider_executable_left']} "
        f"prework_blocked_left={db_progress['prework_blocked_left']} "
        f"api_errors={db_progress['api_errors']} "
        f"terminal_failures={db_progress['terminal_failures']} "
        f"db_integrity={db_progress['integrity']}",
        flush=True,
    )
    print(
        "shard status: "
        f"passed={shard_progress['passed']} "
        f"pending_or_failed={shard_progress['pending_or_failed']} "
        f"active={shard_progress['active']} "
        f"total={shard_progress['total']}",
        flush=True,
    )
    return 30 if shard_progress["pending_or_failed"] == 0 else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print milestone and shard progress.")
    parser.add_argument("--out-dir", default="runs")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--milestone", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    raise SystemExit(print_progress(Path(args.out_dir), args.run_id, args.milestone))


if __name__ == "__main__":
    main()
