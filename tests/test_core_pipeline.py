from __future__ import annotations

import json
from argparse import Namespace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil
import uuid

import pytest

from analysis.scruples_analysis import global_source_baseline, load_source_analysis_rows, summarize_source_rows
from data.scruples_loader import analysis_rows, iter_scruples_anecdotes, load_scruples_anecdotes
from metrics.agreement_surplus import agreement_surplus
from metrics.distribution_gap import distribution_agreement_gap
from metrics.distributions import jensen_shannon_divergence, total_variation_distance
from metrics.sampling_compression import sample_label_distribution, sampling_compression
from models.baselines.predictors import majority_only_oracle, uniform_baseline
from parsing.validate_json import parse_and_validate
from parsing.validity_status import ValidityStatus
from prompts.prompt_templates import render_prompt
from production.config import load_execution_config
from production.execute_milestone import _executable_requests, _recent_api_failures, parse_skip_model_ids, parsed_output_is_invalid_for_primary_summary, progress_message, run as execute_milestone_run
from production.progress_status import _count_shards, _db_progress
from pilot.pilot_diagnostics import evaluate_milestone_alignment, milestone_validity_check
from production.failure_policy import (
    ApiFailureKind,
    circuit_breaker_decision,
    classify_api_failure,
    should_retry_call,
)
from production.providers import InferenceRequest, google_generation_config, openai_response_payload
from production.reporting import _decision_with_completion_gate, _decision_with_validity_gate, row_has_complete_distribution
from production.run_milestone import (
    DEFAULT_MODELS,
    earlier_non_target_call_count,
    insert_planned_calls,
    load_source_rows,
    pending_requests,
    planned_call_id,
    select_component_rows,
    terminal_api_call_ids,
)
from production.shards import first_incomplete_shard, iter_jsonl, shard_state_path, write_json, write_shard_plan
from protocol.call_milestones import (
    CALL_MILESTONES,
    MilestoneComponentType,
    get_call_milestone,
)
from protocol.endpoint_registry import PRIMARY_ENDPOINTS
from protocol.exclusion_rules import primary_output_exclusion
from protocol.disagreement_bins import disagreement_bin
from protocol.preregistration_export import preregistration_payload
from protocol.prompt_modes import PromptMode
from randomization.assignment import make_assignment
from source_uncertainty.posterior_draws import dirichlet_posterior_draws
from source_uncertainty.smoothing import dirichlet_smooth_counts
from storage.db import connect, migrate


def _require_scruples_data(*splits: str) -> None:
    root = Path("data/scruples/anecdotes")
    split_files = {
        "train": "train.scruples-anecdotes.jsonl",
        "dev": "dev.scruples-anecdotes.jsonl",
        "test": "test.scruples-anecdotes.jsonl",
    }
    missing = [split for split in splits if not (root / split_files[split]).exists()]
    if missing:
        pytest.skip(f"SCRUPLES raw split files are not present in this checkout: {', '.join(missing)}")


def test_source_distribution_and_bins():
    dist = dirichlet_smooth_counts({"author": 6, "other": 3, "everybody": 1, "nobody": 0, "info": 0}, alpha=0.5)
    assert dist.majority_label == "author"
    assert dist.disagreement_bin == disagreement_bin(dist.majority_support)
    assert abs(sum(dist.probabilities.values()) - 1.0) < 1e-12


def test_posterior_draws_are_seed_reproducible():
    counts = {"author": 6, "other": 3, "everybody": 1, "nobody": 0, "info": 0}
    assert dirichlet_posterior_draws(counts, n_draws=2, seed=7) == dirichlet_posterior_draws(counts, n_draws=2, seed=7)


def test_json_validation_normalizes_near_sum():
    raw = json.dumps(
        {
            "label_probabilities": {
                "author": 0.2,
                "other": 0.2,
                "everybody": 0.2,
                "nobody": 0.2,
                "info": 0.199,
            },
            "most_likely_label": "author",
        }
    )
    parsed = parse_and_validate(raw, PromptMode.DISTRIBUTION)
    assert parsed.status == ValidityStatus.VALID_STRICT_SCHEMA
    assert parsed.normalized_probability_sum
    assert abs(sum(parsed.parsed_json["label_probabilities"].values()) - 1.0) < 1e-12


def test_json_validation_accepts_one_extracted_object_with_extra_text():
    raw = 'Here is the answer:\n{"chosen_label":"author","estimated_source_community_agreement":0.61}\nThanks.'
    parsed = parse_and_validate(raw, PromptMode.DESCRIPTIVE_VERDICT)
    assert parsed.status == ValidityStatus.VALID_EXTRACTED_JSON
    assert parsed.extracted_json
    assert parsed.parsed_json["chosen_label"] == "author"


def test_prompts_name_required_json_fields():
    labels = ("author", "other", "everybody", "nobody", "info")
    distribution = render_prompt(PromptMode.DISTRIBUTION, "Example situation.", labels)
    assert "label_probabilities" in distribution
    assert "most_likely_label" in distribution
    assert '"author": 0.0' in distribution

    verdict = render_prompt(PromptMode.DESCRIPTIVE_VERDICT, "Example situation.", labels)
    assert "chosen_label" in verdict
    assert "estimated_source_community_agreement" in verdict


def test_primary_metrics():
    source = {"author": 0.55, "other": 0.25, "everybody": 0.10, "nobody": 0.05, "info": 0.05}
    model = {"author": 0.80, "other": 0.10, "everybody": 0.05, "nobody": 0.03, "info": 0.02}
    assert total_variation_distance(source, model) > 0
    assert jensen_shannon_divergence(source, model) > 0
    assert abs(agreement_surplus(0.75, source, "author") - 0.20) < 1e-12
    assert abs(distribution_agreement_gap(0.75, model, "author") - -0.05) < 1e-12


def test_sampling_compression_and_baselines():
    source = {"author": 0.55, "other": 0.25, "everybody": 0.10, "nobody": 0.05, "info": 0.05}
    sampled = ["author", "author", "other", "author"]
    assert sample_label_distribution(sampled)["author"] == 0.75
    assert sampling_compression(source, sampled) > 0
    assert uniform_baseline().label_probabilities["info"] == 0.2
    assert majority_only_oracle(source).most_likely_label == "author"


def test_assignment_is_reproducible():
    a = make_assignment("item1", "model1", PromptMode.DESCRIPTIVE_VERDICT, seed=123)
    b = make_assignment("item1", "model1", PromptMode.DESCRIPTIVE_VERDICT, seed=123)
    assert a == b


def test_storage_migration():
    connection = connect(":memory:")
    migrate(connection)
    tables = {row["name"] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"items", "planned_api_calls", "api_calls_raw", "parsed_outputs", "metric_outputs", "run_manifest"} <= tables
    api_call_columns = {row["name"] for row in connection.execute("PRAGMA table_info(api_calls_raw)")}
    assert {
        "raw_response",
        "request_json",
        "http_status_code",
        "response_headers_json",
        "error_response_body",
        "transport_error_message",
        "retry_after_seconds",
        "terminal_failure_flag",
        "milestone",
        "call_type",
        "is_pilot",
        "is_confirmatory",
    } <= api_call_columns
    tables = {row["name"] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "api_call_attempts" in tables


def test_protocol_registries_lock_primary_contract():
    assert [endpoint.name for endpoint in PRIMARY_ENDPOINTS] == [
        "agreement_surplus",
        "distribution_agreement_gap",
        "sampling_compression",
    ]
    assert primary_output_exclusion("valid_after_repair").include_primary
    assert primary_output_exclusion("valid_extracted_json").include_primary
    assert not primary_output_exclusion("invalid_json").include_primary


def test_executor_invalid_counter_uses_primary_valid_statuses():
    assert not parsed_output_is_invalid_for_primary_summary(ValidityStatus.VALID_STRICT_SCHEMA)
    assert not parsed_output_is_invalid_for_primary_summary(ValidityStatus.VALID_EXTRACTED_JSON)
    assert parsed_output_is_invalid_for_primary_summary(ValidityStatus.MISSING_REQUIRED_FIELD)


def test_executor_progress_message_reports_completed_and_left():
    message = progress_message(
        3,
        10,
        {
            "run_id": "run",
            "target_milestone": "50",
            "model_id": "model",
            "prompt_mode": "distribution_mode",
        },
        "parsed:valid_strict_schema",
    )
    assert "completed=3/10" in message
    assert "left=7" in message
    assert "model=model" in message


def test_executor_can_temporarily_skip_model_ids():
    requests = [
        {"api_call_id": "a", "model_id": "gemini-3.5-flash", "prework_required": []},
        {"api_call_id": "b", "model_id": "gpt-5.5", "prework_required": []},
        {"api_call_id": "c", "model_id": "qwen/qwen3.7-max", "prework_required": ["paraphrase"]},
    ]
    skip_model_ids = parse_skip_model_ids("gemini-3.5-flash")
    executable = _executable_requests(requests, allow_prework_blocked=False, skip_model_ids=skip_model_ids)
    assert [request["api_call_id"] for request in executable] == ["b"]


def test_failed_shard_plan_rewrites_to_current_pending_calls():
    shard_dir = Path("runs") / "test_shards" / uuid.uuid4().hex
    try:
        original = [{"api_call_id": "a"}, {"api_call_id": "b"}, {"api_call_id": "c"}]
        [shard_path] = write_shard_plan(shard_dir, original, 1)
        write_json(shard_state_path(shard_path), {"shard": shard_path.name, "status": "failed"})

        [rewritten_path] = write_shard_plan(shard_dir, [{"api_call_id": "c"}], 1)

        assert [row["api_call_id"] for row in iter_jsonl(rewritten_path)] == ["c"]
        assert json.loads(shard_state_path(rewritten_path).read_text(encoding="utf-8"))["status"] == "pending"
    finally:
        shutil.rmtree(shard_dir, ignore_errors=True)


def test_pending_stale_shard_plan_rewrites_to_current_pending_calls():
    shard_dir = Path("runs") / "test_shards" / uuid.uuid4().hex
    try:
        original = [{"api_call_id": "a"}, {"api_call_id": "b"}, {"api_call_id": "c"}]
        [shard_path] = write_shard_plan(shard_dir, original, 1)
        write_json(shard_state_path(shard_path), {"shard": shard_path.name, "status": "pending"})

        [rewritten_path] = write_shard_plan(shard_dir, [{"api_call_id": "c"}], 1)

        assert [row["api_call_id"] for row in iter_jsonl(rewritten_path)] == ["c"]
        assert json.loads(shard_state_path(rewritten_path).read_text(encoding="utf-8"))["status"] == "pending"
    finally:
        shutil.rmtree(shard_dir, ignore_errors=True)


def test_empty_shards_are_not_incomplete():
    shard_dir = Path("runs") / "test_shards" / uuid.uuid4().hex
    try:
        shard_paths = write_shard_plan(shard_dir, [{"api_call_id": "only"}], 3)
        first_state = json.loads(shard_state_path(shard_paths[0]).read_text(encoding="utf-8"))
        empty_states = [json.loads(shard_state_path(path).read_text(encoding="utf-8")) for path in shard_paths[1:]]
        assert first_state["status"] == "pending"
        assert all(state["status"] == "passed" and state["planned_calls"] == 0 for state in empty_states)

        write_json(shard_state_path(shard_paths[0]), {**first_state, "status": "passed"})
        assert first_incomplete_shard(shard_paths) is None
    finally:
        shutil.rmtree(shard_dir, ignore_errors=True)


def test_extra_stale_shards_are_retired_when_shard_count_shrinks():
    shard_dir = Path("runs") / "test_shards" / uuid.uuid4().hex
    try:
        original_paths = write_shard_plan(shard_dir, [{"api_call_id": "a"}, {"api_call_id": "b"}], 2)
        write_json(shard_state_path(original_paths[1]), {"shard": original_paths[1].name, "status": "pending", "planned_calls": 1})

        [remaining_path] = write_shard_plan(shard_dir, [{"api_call_id": "a"}], 1)

        retired_state = json.loads(shard_state_path(original_paths[1]).read_text(encoding="utf-8"))
        assert [row["api_call_id"] for row in iter_jsonl(remaining_path)] == ["a"]
        assert retired_state["status"] == "passed"
        assert retired_state["planned_calls"] == 0
        assert list(iter_jsonl(original_paths[1])) == []
    finally:
        shutil.rmtree(shard_dir, ignore_errors=True)


def test_progress_status_ignores_attempt_and_event_state_files():
    run_root = Path("runs") / "test_progress_status" / uuid.uuid4().hex
    shard_dir = run_root / "run" / "execution_shards" / "3k"
    try:
        shard_dir.mkdir(parents=True, exist_ok=True)
        write_json(shard_dir / "shard_0000.state.json", {"status": "pending", "planned_calls": 1})
        write_json(shard_dir / "shard_0000.attempts.state.json", {"status": "pending", "planned_calls": 99})
        write_json(shard_dir / "shard_0000.events.state.json", {"status": "pending", "planned_calls": 99})

        counts = _count_shards(run_root, "run", "3k")

        assert counts == {"passed": 0, "pending_or_failed": 1, "active": 1, "total": 1}
    finally:
        shutil.rmtree(run_root, ignore_errors=True)


def test_call_milestones_lock_planned_call_budgets_and_core_modes():
    expected_calls = {
        "1": 1,
        "10": 10,
        "50": 50,
        "3k": 3000,
        "6k": 6000,
        "13k": 13000,
        "25k": 24750,
        "35k": 35000,
        "50k": 47500,
    }
    assert {milestone.name: milestone.planned_calls for milestone in CALL_MILESTONES} == expected_calls

    for name in ("3k", "6k", "13k", "25k", "35k", "50k"):
        core = get_call_milestone(name).component(MilestoneComponentType.CORE_CROSS_FORMAT)
        assert core.prompt_modes == (PromptMode.DISTRIBUTION, PromptMode.DESCRIPTIVE_VERDICT)
        assert core.model_count == 5

    assert get_call_milestone("1").planned_calls == 1
    assert get_call_milestone("10").planned_calls == 10
    assert get_call_milestone("50").planned_calls == 50


def test_small_milestones_exclude_normative_certainty_until_35k():
    early_component_types = {
        component.component_type for name in ("3k", "6k", "13k") for component in get_call_milestone(name).components
    }
    assert MilestoneComponentType.NORMATIVE_CERTAINTY not in early_component_types
    assert get_call_milestone("35k").component(MilestoneComponentType.NORMATIVE_CERTAINTY).planned_calls == 2500


def test_larger_milestones_extend_smaller_component_subsets():
    _require_scruples_data("train", "dev", "test")
    rows = load_source_rows(("train", "dev", "test"), alpha=0.5)
    adjacent_pairs = (("3k", "6k"), ("6k", "13k"), ("13k", "25k"), ("25k", "35k"), ("35k", "50k"))
    for smaller_name, larger_name in adjacent_pairs:
        smaller = get_call_milestone(smaller_name)
        larger = get_call_milestone(larger_name)
        for smaller_component in smaller.components:
            try:
                larger_component = larger.component(smaller_component.component_type)
            except KeyError:
                continue
            smaller_rows = select_component_rows(rows, smaller_component, seed=20260615, milestone_name=smaller.name)
            larger_rows = select_component_rows(rows, larger_component, seed=20260615, milestone_name=larger.name)
            assert {row.item_id for row in smaller_rows} <= {row.item_id for row in larger_rows}


def test_local_scruples_data_can_satisfy_largest_allocations():
    _require_scruples_data("train", "dev", "test")
    rows = load_source_rows(("train", "dev", "test"), alpha=0.5)
    largest = get_call_milestone("50k")
    for component in largest.components:
        selected = select_component_rows(rows, component, seed=20260615, milestone_name=largest.name)
        assert len(selected) == component.item_count


def _target_call_ids(milestone_name: str, run_id: str = "production_milestones_cumulative_v1") -> set[str]:
    _require_scruples_data("train", "dev", "test")
    rows = load_source_rows(("train", "dev", "test"), alpha=0.5)
    milestone = get_call_milestone(milestone_name)
    call_ids: set[str] = set()
    for component in milestone.components:
        selected_rows = select_component_rows(rows, component, seed=20260615, milestone_name=milestone_name)
        for row in selected_rows:
            for model_id in DEFAULT_MODELS[: component.model_count]:
                for prompt_mode in component.prompt_modes:
                    sample_ids = range(component.samples_per_item) if component.samples_per_item > 1 else (None,)
                    for sample_id in sample_ids:
                        call_ids.add(planned_call_id(run_id, component, row, model_id, prompt_mode.value, sample_id))
    return call_ids


def test_call_targets_are_cumulative_through_13k_and_25k():
    targets = {name: _target_call_ids(name) for name in ("3k", "6k", "13k", "25k", "35k", "50k")}
    assert targets["3k"] <= targets["6k"]
    assert targets["6k"] <= targets["13k"]
    assert targets["13k"] <= targets["25k"]
    assert len(targets["25k"] - targets["35k"]) == 1000
    assert len(targets["35k"] - targets["50k"]) == 500


def test_preregistration_exports_call_milestones():
    payload = preregistration_payload()
    assert [milestone["name"] for milestone in payload["call_milestones"]] == ["1", "10", "50", "3k", "6k", "13k", "25k", "35k", "50k"]
    assert payload["call_milestones"][3]["planned_calls"] == 3000


def test_milestone_validity_and_alignment_decisions():
    rows = [
        {
            "model_id": "m1",
            "prompt_mode": PromptMode.DISTRIBUTION.value,
            "validity_status": "valid_strict_schema",
        },
        {
            "model_id": "m1",
            "prompt_mode": PromptMode.DESCRIPTIVE_VERDICT.value,
            "validity_status": "valid_after_repair",
        },
    ]
    check = milestone_validity_check(rows, "3k")
    assert check["proceed"]
    assert check["overall_validity_rate"] == 1.0

    continue_decision = evaluate_milestone_alignment(
        "13k",
        {
            "overall_validity_rate": 0.98,
            "min_model_mode_validity_rate": 0.94,
            "positive_gap_models": 4,
            "positive_surplus_models": 4,
            "low_diffuse_distribution_agreement_gap_mean": 0.12,
            "low_diffuse_agreement_surplus_mean": 0.11,
            "high_consensus_distribution_agreement_gap_mean": 0.02,
            "positive_sampling_compression_models": 3,
            "paraphrase_preserves_direction": True,
            "distribution_outputs_item_sensitive": True,
            "agreement_estimates_interpretable": True,
        },
    )
    assert continue_decision["decision"] == "continue"

    stop_decision = evaluate_milestone_alignment(
        "13k",
        {
            "positive_gap_models": 2,
            "low_diffuse_distribution_agreement_gap_mean": -0.01,
            "distribution_outputs_item_sensitive": False,
        },
    )
    assert stop_decision["decision"] == "stop_or_redesign"


def test_milestone_planner_is_resume_safe():
    _require_scruples_data("dev")
    run_id = "test_resume"
    milestone = get_call_milestone("3k")
    component = milestone.component(MilestoneComponentType.CORE_CROSS_FORMAT)
    rows = select_component_rows(load_source_rows(("dev",), alpha=0.5), component, seed=20260615, milestone_name="3k")
    connection = connect(":memory:")
    migrate(connection)

    first_inserted = insert_planned_calls(connection, milestone, component, rows, DEFAULT_MODELS, 20260615, run_id)
    second_inserted = insert_planned_calls(connection, milestone, component, rows, DEFAULT_MODELS, 20260615, run_id)
    assert first_inserted == 2000
    assert second_inserted == 0
    assert len(pending_requests(connection, run_id, "3k")) == 2000
    source_distribution_counts = connection.execute(
        """
        SELECT COUNT(*) AS n, COUNT(DISTINCT item_id) AS distinct_items
        FROM source_distributions
        WHERE posterior_draw_id_or_null IS NULL
        """
    ).fetchone()
    assert source_distribution_counts["n"] == source_distribution_counts["distinct_items"]

    api_call_id = connection.execute(
        "SELECT api_call_id FROM planned_api_calls WHERE run_id = ? ORDER BY api_call_id LIMIT 1",
        (run_id,),
    ).fetchone()["api_call_id"]
    connection.execute(
        """
        INSERT INTO api_calls_raw (
          api_call_id, run_id, item_id, dataset_id, model_id, provider, api_route,
          prompt_mode, prompt_hash, request_json, raw_response, api_error_flag
        )
        SELECT api_call_id, run_id, item_id, dataset_id, model_id, 'test_provider', 'test_route',
               prompt_mode, prompt_hash, request_json, '{"ok":true}', 0
        FROM planned_api_calls
        WHERE api_call_id = ?
        """,
        (api_call_id,),
    )
    connection.commit()
    assert len(pending_requests(connection, run_id, "3k")) == 1999

    terminal_call_id = connection.execute(
        """
        SELECT api_call_id FROM planned_api_calls
        WHERE run_id = ? AND api_call_id != ?
        ORDER BY api_call_id LIMIT 1
        """,
        (run_id, api_call_id),
    ).fetchone()["api_call_id"]
    connection.execute(
        """
        INSERT INTO api_calls_raw (
          api_call_id, run_id, item_id, dataset_id, model_id, provider, api_route,
          prompt_mode, prompt_hash, request_json, api_error_flag, api_error_type,
          http_status_code, error_response_body, terminal_failure_flag
        )
        SELECT api_call_id, run_id, item_id, dataset_id, model_id, 'test_provider', 'test_route',
               prompt_mode, prompt_hash, request_json, 1, 'bad_request', 400,
               '{"error":"bad schema"}', 1
        FROM planned_api_calls
        WHERE api_call_id = ?
        """,
        (terminal_call_id,),
    )
    connection.commit()
    assert terminal_call_id in terminal_api_call_ids(connection, run_id)
    assert len(pending_requests(connection, run_id, "3k")) == 1998


def test_api_failure_policy_stops_wasteful_retry_loops():
    server_failure = classify_api_failure(http_status_code=503)
    assert server_failure.kind == ApiFailureKind.SERVER_ERROR
    assert should_retry_call(0, server_failure)
    assert not should_retry_call(3, server_failure)

    rate_limit = classify_api_failure(http_status_code=429, retry_after_seconds=60)
    assert rate_limit.kind == ApiFailureKind.RATE_LIMIT
    assert rate_limit.retry_after_seconds == 60

    bad_request = classify_api_failure(http_status_code=400)
    assert bad_request.terminal
    assert not should_retry_call(0, bad_request)

    breaker = circuit_breaker_decision([{"http_status_code": 503, "api_error_type": "server_error"} for _ in range(10)])
    assert breaker.abort
    assert "5xx" in breaker.reason


def test_recent_api_failures_age_out_old_transient_errors():
    connection = connect(":memory:")
    migrate(connection)
    old_completed = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
    recent_completed = datetime.now(timezone.utc).isoformat()
    for api_call_id, completed in (("old", old_completed), ("recent", recent_completed)):
        connection.execute(
            """
            INSERT INTO api_calls_raw (
              api_call_id, run_id, milestone, item_id, dataset_id, model_id, provider,
              api_route, prompt_mode, prompt_hash, request_json, api_error_flag,
              api_error_type, http_status_code, terminal_failure_flag, timestamp_completed
            ) VALUES (?, 'run', '3k', ?, 'dataset', 'gemini-3.5-flash', 'google',
              'route', 'distribution_mode', 'hash', '{}', 1, 'server_error', 503, 0, ?)
            """,
            (api_call_id, api_call_id, completed),
        )
    connection.commit()

    failures = _recent_api_failures(connection, "run", window_minutes=10)
    assert len(failures) == 1
    assert failures[0]["http_status_code"] == 503
    assert failures[0]["provider"] == "google"
    connection.close()


def test_execution_config_uses_old_run_env_var_names(monkeypatch):
    models = ("gpt-test", "claude-test", "gemini-test", "qwen-test-large", "qwen-test-small")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-key")
    monkeypatch.setenv("ANTHROPIC_MODEL", "claude-test")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-key")
    monkeypatch.setenv("GOOGLE_MODEL", "gemini-test")
    monkeypatch.setenv("LLAMA_API_KEY", "llama-key")
    monkeypatch.setenv("LLAMA_MODEL", "meta-llama-test")
    config = load_execution_config(models)
    assert config.model_to_provider == {
        "gpt-test": "openai",
        "claude-test": "anthropic",
        "gemini-test": "google",
        "qwen-test-large": "llama",
        "qwen-test-small": "llama",
    }


def test_google_generation_config_requests_json_and_low_thinking():
    req = InferenceRequest(
        model_id="gemini-3.5-flash",
        prompt="Return JSON.",
        prompt_mode=PromptMode.DISTRIBUTION.value,
    )
    config = google_generation_config(req)
    assert config["responseMimeType"] == "application/json"
    assert config["maxOutputTokens"] == 1024
    assert config["thinkingConfig"] == {"thinkingLevel": "low"}


def test_openai_response_payload_uses_larger_budget_and_no_reasoning():
    req = InferenceRequest(
        model_id="gpt-5.5",
        prompt="Return JSON.",
        prompt_mode=PromptMode.DISTRIBUTION.value,
    )
    payload = openai_response_payload(req)
    assert payload["max_output_tokens"] == 1024
    assert payload["reasoning"] == {"effort": "none"}


def test_distribution_gap_report_skips_incomplete_distribution_rows():
    complete = {"p_author": 0.8, "p_other": 0.1, "p_everybody": 0.05, "p_nobody": 0.03, "p_info": 0.02}
    incomplete = dict(complete)
    incomplete["p_author"] = None
    assert row_has_complete_distribution(complete)
    assert not row_has_complete_distribution(incomplete)


def test_report_decision_honors_validity_gate():
    decision = {"milestone": "50", "decision": "continue", "failures": [], "revision_reasons": [], "observed": {}}
    adjusted = _decision_with_validity_gate(decision, {"proceed": False}, "50", {"overall_validity_rate": 0.98})
    assert adjusted["decision"] == "stop_or_redesign"
    assert "JSON validity gate failed" in adjusted["failures"]


def test_report_decision_waits_for_complete_milestone():
    premature = {"milestone": "3k", "decision": "stop_or_redesign", "failures": ["partial signal"], "revision_reasons": [], "observed": {}}
    attempted = {"planned": 3000, "completed_successful": 125, "terminal_failures": 0}
    adjusted = _decision_with_completion_gate(premature, attempted, "3k", {"overall_validity_rate": 1.0})
    assert adjusted["decision"] == "pending_insufficient_outputs"
    assert "milestone execution incomplete" in adjusted["revision_reasons"]


def test_progress_status_reports_total_executable_and_skipped_left():
    scratch_dir = Path("runs") / "test_progress_status" / uuid.uuid4().hex
    db_path = scratch_dir / "study.sqlite"
    connection = connect(db_path)
    migrate(connection)
    try:
        requests = [
            ("done", "model", {}),
            ("open", "model", {}),
            ("blocked", "model", {"prework_required": True}),
            ("skipped", "gemini-3.5-flash", {}),
        ]
        for api_call_id, model_id, request in requests:
            connection.execute(
                """
                INSERT INTO planned_api_calls (
                  api_call_id, run_id, milestone, component_type, component_name,
                  item_id, dataset_id, model_id, prompt_mode, assignment_hash,
                  prompt_hash, request_json, status, created_at
                ) VALUES (?, 'run', '3k', 'core_cross_format', 'core', ?, 'dataset', ?,
                  'distribution_mode', ?, 'hash', ?, 'planned', 'now')
                """,
                (api_call_id, api_call_id, model_id, api_call_id, json.dumps(request)),
            )
        connection.execute(
            """
            INSERT INTO api_calls_raw (
              api_call_id, run_id, milestone, item_id, dataset_id, model_id, provider,
              api_route, prompt_mode, prompt_hash, request_json, raw_response, api_error_flag
            ) VALUES ('done', 'run', '3k', 'done', 'dataset', 'model', 'provider',
              'route', 'distribution_mode', 'hash', '{}', '{}', 0)
            """
        )
        connection.commit()
    finally:
        connection.close()

    try:
        progress = _db_progress(db_path, "run", "3k", skip_model_ids={"gemini-3.5-flash"})
        assert progress["completed_successful"] == 1
        assert progress["left_total"] == 3
        assert progress["provider_executable_left"] == 2
        assert progress["provider_executable_left_now"] == 1
        assert progress["prework_blocked_left"] == 1
        assert progress["skip_model_left"] == 1
    finally:
        shutil.rmtree(scratch_dir, ignore_errors=True)


def test_mock_executor_retains_raw_attempts_and_resumes_without_recalling_successes():
    _require_scruples_data("dev")
    models = "mock-a,mock-b,mock-c,mock-d,mock-e"
    run_id = f"mock_executor_resume_{uuid.uuid4().hex}"
    out_dir = Path("runs") / "test_executor"
    args = Namespace(
        milestone="3k",
        run_id=run_id,
        out_dir=str(out_dir),
        db=None,
        models=models,
        splits="dev",
        seed=20260615,
        alpha=0.5,
        shard_count=1,
        max_calls=3,
        mock_provider=True,
        allow_prework_blocked=False,
    )
    first = execute_milestone_run(args)
    assert first["status"] == "passed"
    assert first["completed_calls"] == 3

    db_path = out_dir / run_id / "study.sqlite"
    connection = connect(db_path)
    migrate(connection)
    raw_rows = connection.execute("SELECT raw_response, api_error_flag FROM api_calls_raw").fetchall()
    attempt_rows = connection.execute("SELECT raw_response, http_status_code FROM api_call_attempts").fetchall()
    parsed_rows = connection.execute("SELECT validity_status FROM parsed_outputs").fetchall()
    ledger_path = out_dir / run_id / "call_ledger_3k.csv"
    report_path = out_dir / run_id / "milestone_report_3k.md"
    assert len(raw_rows) == 3
    assert all(row["api_error_flag"] == 0 and row["raw_response"] for row in raw_rows)
    assert len(attempt_rows) == 3
    assert all(row["http_status_code"] == 200 and row["raw_response"] for row in attempt_rows)
    assert len(parsed_rows) == 3
    assert all(row["validity_status"] == ValidityStatus.VALID_STRICT_SCHEMA.value for row in parsed_rows)
    assert ledger_path.exists()
    assert report_path.exists()
    ledger_text = ledger_path.read_text(encoding="utf-8")
    assert "planned_call_id" in ledger_text
    assert "is_pilot" in ledger_text
    assert "source_p_author" in ledger_text
    report_text = report_path.read_text(encoding="utf-8")
    assert "## 1. Calls Attempted And Completed" in report_text
    assert "## 10. Continue / Revise / Stop Decision" in report_text
    connection.close()

    second = execute_milestone_run(args)
    assert second["completed_calls"] == 3
    connection = connect(db_path)
    try:
        assert connection.execute("SELECT COUNT(*) AS n FROM api_calls_raw").fetchone()["n"] == 6
        assert connection.execute("SELECT COUNT(DISTINCT api_call_id) AS n FROM api_calls_raw").fetchone()["n"] == 6
    finally:
        connection.close()

    complete_run_id = f"mock_executor_already_complete_{uuid.uuid4().hex}"
    complete_args = Namespace(
        milestone="1",
        run_id=complete_run_id,
        out_dir=str(out_dir),
        db=None,
        models=models,
        splits="dev",
        seed=20260615,
        alpha=0.5,
        shard_count=1,
        max_calls=None,
        skip_model_ids="mock-a",
        mock_provider=True,
        allow_prework_blocked=False,
    )
    complete = execute_milestone_run(complete_args)
    complete_summary_path = out_dir / complete_run_id / "execution_summary_1.json"
    assert complete["status"] == "already_complete"
    assert json.loads(complete_summary_path.read_text(encoding="utf-8"))["status"] == "already_complete"


def test_larger_milestone_pending_includes_prior_successes_without_recalling_them():
    _require_scruples_data("train", "dev", "test")
    run_id = "test_cumulative_resume"
    source_rows = load_source_rows(("train", "dev", "test"), alpha=0.5)
    connection = connect(":memory:")
    migrate(connection)

    three = get_call_milestone("3k")
    three_core = three.component(MilestoneComponentType.CORE_CROSS_FORMAT)
    three_rows = select_component_rows(source_rows, three_core, seed=20260615, milestone_name="3k")
    assert insert_planned_calls(connection, three, three_core, three_rows, DEFAULT_MODELS, 20260615, run_id) == 2000

    api_call_id = connection.execute(
        "SELECT api_call_id FROM planned_api_calls WHERE run_id = ? ORDER BY api_call_id LIMIT 1",
        (run_id,),
    ).fetchone()["api_call_id"]
    connection.execute(
        """
        INSERT INTO api_calls_raw (
          api_call_id, run_id, item_id, dataset_id, model_id, provider, api_route,
          prompt_mode, prompt_hash, request_json, raw_response, api_error_flag
        )
        SELECT api_call_id, run_id, item_id, dataset_id, model_id, 'test_provider', 'test_route',
               prompt_mode, prompt_hash, request_json, '{"ok":true}', 0
        FROM planned_api_calls
        WHERE api_call_id = ?
        """,
        (api_call_id,),
    )

    six = get_call_milestone("6k")
    six_core = six.component(MilestoneComponentType.CORE_CROSS_FORMAT)
    six_rows = select_component_rows(source_rows, six_core, seed=20260615, milestone_name="6k")
    assert insert_planned_calls(connection, six, six_core, six_rows, DEFAULT_MODELS, 20260615, run_id) == 2000
    connection.commit()

    assert len(pending_requests(connection, run_id, "6k")) == 3999
    assert earlier_non_target_call_count(connection, run_id, "6k", _target_call_ids("6k", run_id=run_id)) == 0


def test_scruples_anecdotes_loader_uses_downloaded_data():
    _require_scruples_data("dev")
    anecdotes = load_scruples_anecdotes(splits=["dev"])
    assert len(anecdotes) == 2500
    first = anecdotes[0]
    assert first.dataset_id == "scruples_anecdotes_v1"
    assert set(first.label_scores) == {"author", "other", "everybody", "nobody", "info"}
    assert first.annotation_count == sum(first.label_scores.values())
    row = next(analysis_rows([first]))
    assert row.item_id == first.item_id
    assert abs(sum(row.source_distribution().values()) - 1.0) < 1e-12
    assert row.source_distribution_version == "dirichlet_alpha_0.5_scruples_anecdotes_v1"


def test_scruples_source_analysis_summary_and_baseline():
    _require_scruples_data("dev")
    rows = load_source_analysis_rows(splits=["dev"], alpha=0.5)
    summary = summarize_source_rows(rows)
    assert summary["n_items"] == 2500
    assert summary["split_counts"] == {"dev": 2500}
    assert sum(summary["disagreement_bin_counts"].values()) == 2500
    baseline = global_source_baseline(rows)
    assert baseline.baseline_type == "global_base_rate"
    assert abs(sum(baseline.label_probabilities.values()) - 1.0) < 1e-12
