from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def json_dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json_dumps(record) + "\n")


def write_json(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_shard_plan(shard_dir: Path, pending: list[dict[str, Any]], shard_count: int) -> list[Path]:
    shard_dir.mkdir(parents=True, exist_ok=True)
    shard_count = max(1, shard_count)
    shard_paths: list[Path] = []
    buckets: list[list[dict[str, Any]]] = [[] for _ in range(shard_count)]
    for index, request in enumerate(pending):
        buckets[index % shard_count].append(request)
    for index, bucket in enumerate(buckets):
        path = shard_dir / f"shard_{index:04d}.jsonl"
        state_path = shard_state_path(path)
        state = read_json(state_path) or {}
        existing_call_ids = [record.get("api_call_id") for record in iter_jsonl(path)] if path.exists() else None
        bucket_call_ids = [record.get("api_call_id") for record in bucket]
        stale_plan = existing_call_ids != bucket_call_ids
        should_write = not path.exists() or (state.get("status") != "running" and stale_plan)
        if should_write:
            with path.open("w", encoding="utf-8", newline="\n") as handle:
                for record in bucket:
                    handle.write(json_dumps(record) + "\n")
        if not state_path.exists() or should_write:
            planned_calls = len(bucket)
            write_json(
                state_path,
                {
                    "shard": path.name,
                    "status": "pending" if planned_calls else "passed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "planned_calls": planned_calls,
                    "completed_calls": 0,
                    "failed_calls": 0,
                },
            )
        shard_paths.append(path)
    active_path_names = {path.name for path in shard_paths}
    for stale_path in sorted(shard_dir.glob("shard_*.jsonl")):
        if stale_path.name in active_path_names:
            continue
        state_path = shard_state_path(stale_path)
        state = read_json(state_path) or {}
        if state.get("status") == "running":
            continue
        stale_path.write_text("", encoding="utf-8")
        write_json(
            state_path,
            {
                "shard": stale_path.name,
                "status": "passed",
                "created_at": state.get("created_at") or utc_now(),
                "updated_at": utc_now(),
                "planned_calls": 0,
                "completed_calls": 0,
                "failed_calls": 0,
            },
        )
    return shard_paths


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.exists():
        return ()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def shard_state_path(shard_path: Path) -> Path:
    return shard_path.with_suffix(".state.json")


def first_incomplete_shard(shard_paths: Iterable[Path]) -> Path | None:
    for shard_path in sorted(shard_paths):
        state = read_json(shard_state_path(shard_path)) or {}
        if state.get("status") != "passed" and state.get("planned_calls", 1) > 0:
            return shard_path
    return None


def update_shard_state(shard_path: Path, **updates: Any) -> None:
    path = shard_state_path(shard_path)
    state = read_json(path) or {"shard": shard_path.name, "created_at": utc_now()}
    state.update(updates)
    state["updated_at"] = utc_now()
    write_json(path, state)
