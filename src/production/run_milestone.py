from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

from data.scruples_loader import ScruplesAnalysisRow, load_scruples_anecdotes, analysis_rows
from prompts.prompt_hashing import prompt_hash
from prompts.prompt_templates import render_prompt
from protocol.call_milestones import (
    CALL_MILESTONE_BY_NAME,
    CALL_MILESTONES,
    BinAllocation,
    CallMilestone,
    MilestoneComponent,
    MilestoneComponentType,
    get_call_milestone,
)
from protocol.label_schema import CANONICAL_SCHEMA
from protocol.label_schema import LABELS
from randomization.assignment import make_assignment
from production.reporting import write_api_call_ledger, write_milestone_report
from storage.db import connect, migrate
from storage.manifests import create_manifest
from utils.hashing import stable_hash


DEFAULT_MODELS: tuple[str, ...] = (
    "model_slot_1_replace_before_api_execution",
    "model_slot_2_replace_before_api_execution",
    "model_slot_3_replace_before_api_execution",
    "model_slot_4_replace_before_api_execution",
    "model_slot_5_replace_before_api_execution",
)

MILESTONE_RANK = {milestone.name: index for index, milestone in enumerate(CALL_MILESTONES)}


def parse_model_ids(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return DEFAULT_MODELS
    models = tuple(model.strip() for model in raw.split(",") if model.strip())
    if len(models) != 5:
        raise ValueError(f"expected exactly 5 comma-separated model IDs, got {len(models)}")
    return models


def load_source_rows(splits: Sequence[str], alpha: float) -> list[ScruplesAnalysisRow]:
    return list(analysis_rows(load_scruples_anecdotes(splits=splits), alpha=alpha))


def stable_row_order(rows: Iterable[ScruplesAnalysisRow], seed: int, namespace: str) -> list[ScruplesAnalysisRow]:
    return sorted(rows, key=lambda row: stable_hash([seed, namespace, row.item_id]))


def select_allocated_rows(
    rows: Sequence[ScruplesAnalysisRow],
    allocation: BinAllocation,
    seed: int,
    namespace: str,
) -> list[ScruplesAnalysisRow]:
    by_bin: dict[str, list[ScruplesAnalysisRow]] = {}
    for row in rows:
        by_bin.setdefault(row.disagreement_bin, []).append(row)

    selected: list[ScruplesAnalysisRow] = []
    for bin_name, count in allocation.to_dict().items():
        candidates = stable_row_order(by_bin.get(bin_name, []), seed, f"{namespace}:{bin_name}")
        if len(candidates) < count:
            raise ValueError(f"not enough SCRUPLES rows in {bin_name!r}: need {count}, found {len(candidates)}")
        selected.extend(candidates[:count])
    return stable_row_order(selected, seed, f"{namespace}:combined")


def select_unallocated_rows(
    rows: Sequence[ScruplesAnalysisRow],
    item_count: int,
    seed: int,
    namespace: str,
) -> list[ScruplesAnalysisRow]:
    candidates = stable_row_order(rows, seed, namespace)
    if len(candidates) < item_count:
        raise ValueError(f"not enough SCRUPLES rows: need {item_count}, found {len(candidates)}")
    return candidates[:item_count]


def select_component_rows(
    rows: Sequence[ScruplesAnalysisRow],
    component: MilestoneComponent,
    seed: int,
    milestone_name: str,
) -> list[ScruplesAnalysisRow]:
    namespace = component.component_type.value
    if component.bin_allocation is None:
        return select_unallocated_rows(rows, component.item_count, seed, namespace)
    selected = select_allocated_rows(rows, component.bin_allocation, seed, namespace)
    if len(selected) != component.item_count:
        raise ValueError(f"{component.name} selected {len(selected)} rows, expected {component.item_count}")
    return selected


def json_dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def insert_source_row(connection: sqlite3.Connection, row: ScruplesAnalysisRow) -> None:
    connection.execute(
        """
        INSERT OR IGNORE INTO items (
          item_id, dataset_id, source_item_id, item_text, canonical_label_schema_version,
          split, item_length_chars, raw_metadata_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row.item_id,
            row.dataset_id,
            row.source_item_id,
            row.item_text,
            row.canonical_label_schema_version,
            row.split,
            row.item_length_chars,
            json_dumps({"post_id": row.post_id}),
        ),
    )
    connection.execute(
        """
        INSERT OR IGNORE INTO source_distributions (
          item_id, dataset_id, source_distribution_version, smoothing_method, alpha,
          p_author, p_other, p_everybody, p_nobody, p_info, majority_label,
          majority_support, majority_margin, entropy, entropy_normalized,
          disagreement_bin, posterior_draw_id_or_null
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row.item_id,
            row.dataset_id,
            row.source_distribution_version,
            "dirichlet",
            0.5,
            row.source_p_author,
            row.source_p_other,
            row.source_p_everybody,
            row.source_p_nobody,
            row.source_p_info,
            row.source_majority_label,
            row.source_majority_support,
            row.source_majority_margin,
            row.source_entropy,
            row.source_entropy_normalized,
            row.disagreement_bin,
            None,
        ),
    )
    # SCRUPLES stores raw label counts in the source JSON. The smoothed analysis
    # row has annotation_count but not per-label counts, so reconstruct the
    # canonical source-vote row from the local dataset when available.
    raw_votes = _source_vote_counts_for_item(row.item_id)
    if raw_votes is not None:
        connection.execute(
            """
            INSERT OR IGNORE INTO source_votes (
              item_id, dataset_id, count_author, count_other, count_everybody,
              count_nobody, count_info, annotation_count, source_vote_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row.item_id,
                row.dataset_id,
                raw_votes["author"],
                raw_votes["other"],
                raw_votes["everybody"],
                raw_votes["nobody"],
                raw_votes["info"],
                sum(raw_votes.values()),
                "scruples_anecdotes_v1_raw_counts",
            ),
        )


_SOURCE_VOTE_CACHE: dict[str, dict[str, int]] | None = None


def _source_vote_counts_for_item(item_id: str) -> dict[str, int] | None:
    global _SOURCE_VOTE_CACHE
    if _SOURCE_VOTE_CACHE is None:
        cache: dict[str, dict[str, int]] = {}
        try:
            anecdotes = load_scruples_anecdotes(splits=("train", "dev", "test"))
        except FileNotFoundError:
            anecdotes = []
        for anecdote in anecdotes:
            cache[anecdote.item_id] = {label: int(anecdote.label_scores.get(label, 0)) for label in LABELS}
        _SOURCE_VOTE_CACHE = cache
    return _SOURCE_VOTE_CACHE.get(item_id)


def planned_call_id(run_id: str, component: MilestoneComponent, row: ScruplesAnalysisRow, model_id: str, prompt_mode: str, sample_id: int | None) -> str:
    return stable_hash(
        {
            "run_id": run_id,
            "component_type": component.component_type.value,
            "item_id": row.item_id,
            "model_id": model_id,
            "prompt_mode": prompt_mode,
            "sample_id": sample_id,
        }
    )


def insert_planned_calls(
    connection: sqlite3.Connection,
    milestone: CallMilestone,
    component: MilestoneComponent,
    rows: Sequence[ScruplesAnalysisRow],
    model_ids: Sequence[str],
    seed: int,
    run_id: str,
    target_api_call_ids: set[str] | None = None,
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    inserted = 0
    for row in rows:
        insert_source_row(connection, row)
        for model_id in model_ids[: component.model_count]:
            for prompt_mode in component.prompt_modes:
                sample_ids = range(component.samples_per_item) if component.samples_per_item > 1 else (None,)
                for sample_id in sample_ids:
                    api_call_id = planned_call_id(run_id, component, row, model_id, prompt_mode.value, sample_id)
                    if target_api_call_ids is not None:
                        target_api_call_ids.add(api_call_id)
                    assignment = make_assignment(row.item_id, model_id, prompt_mode, seed=seed, sample_id=sample_id)
                    rendered_prompt = render_prompt(prompt_mode, row.item_text, assignment.label_order)
                    rendered_prompt_hash = prompt_hash(rendered_prompt)
                    request = {
                        "api_call_id": api_call_id,
                        "run_id": run_id,
                        "introduced_milestone": milestone.name,
                        "target_milestone": milestone.name,
                        "call_type": component.component_type.value,
                        "is_pilot": not milestone.use_as_confirmatory,
                        "is_confirmatory": milestone.use_as_confirmatory,
                        "component_type": component.component_type.value,
                        "component_name": component.name,
                        "item_id": row.item_id,
                        "dataset_id": row.dataset_id,
                        "model_id": model_id,
                        "prompt_mode": prompt_mode.value,
                        "sample_id": sample_id,
                        "assignment_hash": assignment.assignment_hash,
                        "label_order": list(assignment.label_order),
                        "prompt_paraphrase_id": assignment.prompt_paraphrase_id,
                        "prompt_hash": rendered_prompt_hash,
                        "prompt": rendered_prompt,
                        "response_schema": prompt_mode.value,
                        "prework_required": [],
                    }
                    if component.component_type == MilestoneComponentType.PARAPHRASE_AUDIT:
                        request["prework_required"] = ["materialize_paraphrase_pairs_before_provider_execution"]
                    already_exists = connection.execute(
                        "SELECT 1 FROM planned_api_calls WHERE api_call_id = ?",
                        (request["api_call_id"],),
                    ).fetchone() is not None
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO prompt_assignments (
                          assignment_hash, item_id, model_id, prompt_mode, label_order,
                          prompt_paraphrase_id, sample_id, seed
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            assignment.assignment_hash,
                            row.item_id,
                            model_id,
                            prompt_mode.value,
                            json_dumps(list(assignment.label_order)),
                            assignment.prompt_paraphrase_id,
                            sample_id,
                            seed,
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO planned_api_calls (
                          api_call_id, run_id, milestone, component_type, component_name,
                          item_id, dataset_id, model_id, prompt_mode, assignment_hash,
                          sample_id, prompt_hash, request_json, status, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(api_call_id) DO UPDATE SET
                          prompt_hash = excluded.prompt_hash,
                          request_json = excluded.request_json,
                          status = planned_api_calls.status
                        """,
                        (
                            request["api_call_id"],
                            run_id,
                            milestone.name,
                            component.component_type.value,
                            component.name,
                            row.item_id,
                            row.dataset_id,
                            model_id,
                            prompt_mode.value,
                            assignment.assignment_hash,
                            sample_id,
                            rendered_prompt_hash,
                            json_dumps(request),
                            "planned",
                            now,
                        ),
                    )
                    if not already_exists:
                        inserted += 1
    return inserted


def successful_api_call_ids(connection: sqlite3.Connection, run_id: str) -> set[str]:
    rows = connection.execute(
        """
        SELECT api_call_id
        FROM api_calls_raw
        WHERE run_id = ?
          AND api_error_flag = 0
          AND raw_response IS NOT NULL
          AND TRIM(raw_response) != ''
        """,
        (run_id,),
    ).fetchall()
    return {str(row["api_call_id"]) for row in rows}


def terminal_api_call_ids(connection: sqlite3.Connection, run_id: str) -> set[str]:
    rows = connection.execute(
        """
        SELECT api_call_id
        FROM api_calls_raw
        WHERE run_id = ? AND terminal_failure_flag = 1
        """,
        (run_id,),
    ).fetchall()
    return {str(row["api_call_id"]) for row in rows}


def earlier_non_target_call_count(
    connection: sqlite3.Connection,
    run_id: str,
    milestone_name: str,
    target_api_call_ids: set[str],
) -> int:
    earlier_milestones = tuple(
        milestone.name for milestone in CALL_MILESTONES if MILESTONE_RANK[milestone.name] < MILESTONE_RANK[milestone_name]
    )
    if not earlier_milestones:
        return 0
    placeholders = ",".join("?" for _ in earlier_milestones)
    rows = connection.execute(
        f"""
        SELECT api_call_id
        FROM planned_api_calls
        WHERE run_id = ? AND milestone IN ({placeholders})
        """,
        (run_id, *earlier_milestones),
    ).fetchall()
    return sum(1 for row in rows if str(row["api_call_id"]) not in target_api_call_ids)


def pending_requests(
    connection: sqlite3.Connection,
    run_id: str,
    milestone_name: str,
    target_api_call_ids: set[str] | None = None,
) -> list[dict[str, object]]:
    successes = successful_api_call_ids(connection, run_id)
    terminal_failures = terminal_api_call_ids(connection, run_id)
    rows = connection.execute(
        """
        SELECT api_call_id, request_json
        FROM planned_api_calls
        WHERE run_id = ?
        ORDER BY api_call_id
        """,
        (run_id,),
    ).fetchall()
    pending = []
    for row in rows:
        api_call_id = str(row["api_call_id"])
        if target_api_call_ids is not None and api_call_id not in target_api_call_ids:
            continue
        if api_call_id in successes or api_call_id in terminal_failures:
            continue
        request = json.loads(row["request_json"])
        request["target_milestone"] = milestone_name
        pending.append(request)
    return pending


def write_jsonl(path: Path, records: Iterable[dict[str, object]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json_dumps(record) + "\n")
            count += 1
    return count


def write_outputs(
    out_dir: Path,
    milestone: CallMilestone,
    component_rows: dict[str, list[ScruplesAnalysisRow]],
    pending: list[dict[str, object]],
    summary: dict[str, object],
    target_api_call_ids: set[str],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    selected_records: list[dict[str, object]] = []
    for component_type, rows in component_rows.items():
        for row in rows:
            selected_records.append(
                {
                    "milestone": milestone.name,
                    "component_type": component_type,
                    "item_id": row.item_id,
                    "dataset_id": row.dataset_id,
                    "split": row.split,
                    "disagreement_bin": row.disagreement_bin,
                    "source_majority_label": row.source_majority_label,
                    "source_majority_support": row.source_majority_support,
                    "source_entropy_normalized": row.source_entropy_normalized,
                }
            )
    write_jsonl(out_dir / f"selected_items_{milestone.name}.jsonl", selected_records)
    write_jsonl(out_dir / f"pending_api_calls_{milestone.name}.jsonl", pending)
    write_jsonl(
        out_dir / f"target_api_call_ids_{milestone.name}.jsonl",
        [{"api_call_id": api_call_id, "target_milestone": milestone.name} for api_call_id in sorted(target_api_call_ids)],
    )
    (out_dir / f"run_summary_{milestone.name}.json").write_text(json.dumps(summary, sort_keys=True, indent=2), encoding="utf-8")


def store_manifest(connection: sqlite3.Connection, run_id: str, milestone: CallMilestone, seed: int, model_ids: Sequence[str], splits: Sequence[str]) -> None:
    manifest = create_manifest(
        run_id,
        dataset_versions={"scruples": "scruples_anecdotes_v1", "splits": list(splits)},
        source_distribution_versions={"scruples": "dirichlet_alpha_0.5_scruples_anecdotes_v1"},
        model_versions={model_id: {"configured_model_id": model_id} for model_id in model_ids},
        random_seeds={"milestone_subset_seed": seed},
        call_milestone=milestone.to_dict(),
        planned_call_budget=milestone.planned_call_budget,
        planned_call_count=milestone.planned_calls,
        sequential_monitoring_plan="Resume-safe milestone prefix plan; 3k and 6k are development pilots, 13k is diagnostic.",
        operator_notes="This planner does not execute provider API calls. It emits pending calls that exclude successful api_calls_raw records.",
    )
    connection.execute(
        """
        INSERT OR REPLACE INTO run_manifest (run_id, manifest_json, created_at)
        VALUES (?, ?, ?)
        """,
        (run_id, manifest.to_json(), manifest.created_at),
    )


def run(args: argparse.Namespace) -> dict[str, object]:
    milestone = get_call_milestone(args.milestone)
    model_ids = parse_model_ids(args.models)
    splits = tuple(split.strip() for split in args.splits.split(",") if split.strip())
    out_dir = Path(args.out_dir) / args.run_id
    db_path = Path(args.db) if args.db else out_dir / "study.sqlite"

    source_rows = load_source_rows(splits=splits, alpha=args.alpha)
    connection = connect(db_path)
    migrate(connection)

    component_rows: dict[str, list[ScruplesAnalysisRow]] = {}
    target_api_call_ids: set[str] = set()
    inserted_total = 0
    for component in milestone.components:
        rows = select_component_rows(source_rows, component, seed=args.seed, milestone_name=milestone.name)
        component_rows[component.component_type.value] = rows
        inserted_total += insert_planned_calls(
            connection,
            milestone,
            component,
            rows,
            model_ids,
            args.seed,
            args.run_id,
            target_api_call_ids=target_api_call_ids,
        )

    store_manifest(connection, args.run_id, milestone, args.seed, model_ids, splits)
    connection.commit()

    pending = pending_requests(connection, args.run_id, milestone.name, target_api_call_ids=target_api_call_ids)
    blocked_prework_count = sum(1 for request in pending if request.get("prework_required"))
    earlier_non_target_count = earlier_non_target_call_count(connection, args.run_id, milestone.name, target_api_call_ids)
    planned_count = len(target_api_call_ids)
    completed_count = planned_count - len(pending)
    bin_counts = {
        component_type: dict(Counter(row.disagreement_bin for row in rows))
        for component_type, rows in component_rows.items()
    }
    summary = {
        "run_id": args.run_id,
        "milestone": milestone.name,
        "db_path": str(db_path),
        "output_dir": str(out_dir),
        "model_ids": list(model_ids),
        "uses_placeholder_models": model_ids == DEFAULT_MODELS,
        "planned_calls_for_milestone": milestone.planned_calls,
        "planned_calls_in_ledger": planned_count,
        "earlier_planned_calls_outside_target": earlier_non_target_count,
        "new_planned_calls_inserted": inserted_total,
        "completed_successful_calls": completed_count,
        "pending_calls": len(pending),
        "blocked_prework_calls": blocked_prework_count,
        "provider_executable_pending_calls": len(pending) - blocked_prework_count,
        "component_item_counts": {key: len(value) for key, value in component_rows.items()},
        "component_bin_counts": bin_counts,
        "ready_for_provider_execution": model_ids != DEFAULT_MODELS and blocked_prework_count < len(pending),
        "provider_execution_note": "Use production.execute_milestone or execute_milestone_run.bat with exactly five frozen model IDs. Paraphrase-audit calls require materialized paraphrase_pairs before execution.",
    }
    write_outputs(out_dir, milestone, component_rows, pending, summary, target_api_call_ids)
    ledger_export = write_api_call_ledger(connection, args.run_id, milestone.name, out_dir, target_api_call_ids=target_api_call_ids)
    report_export = write_milestone_report(connection, args.run_id, milestone.name, out_dir, target_api_call_ids=target_api_call_ids)
    summary["call_ledger_export"] = ledger_export
    summary["milestone_report_export"] = {
        "json_path": report_export["json_path"],
        "md_path": report_export["md_path"],
    }
    (out_dir / f"run_summary_{milestone.name}.json").write_text(json.dumps(summary, sort_keys=True, indent=2), encoding="utf-8")
    connection.close()
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a resume-safe milestone API-call ledger.")
    parser.add_argument("--milestone", choices=tuple(CALL_MILESTONE_BY_NAME), default="3k")
    parser.add_argument("--run-id", default="production_milestones")
    parser.add_argument("--out-dir", default="runs")
    parser.add_argument("--db")
    parser.add_argument("--models", help="Exactly five comma-separated frozen model IDs. Defaults to placeholders.")
    parser.add_argument("--splits", default="train,dev,test")
    parser.add_argument("--seed", type=int, default=20260615)
    parser.add_argument("--alpha", type=float, default=0.5)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = run(args)
    print(json.dumps(summary, sort_keys=True, indent=2))
    if summary["uses_placeholder_models"]:
        print("WARNING: STUDY_MODEL_IDS was not set; model IDs are placeholders. Do not execute API calls yet.")


if __name__ == "__main__":
    main()
