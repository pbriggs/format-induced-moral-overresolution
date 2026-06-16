from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items (
  item_id TEXT PRIMARY KEY,
  dataset_id TEXT NOT NULL,
  source_item_id TEXT,
  item_text TEXT NOT NULL,
  canonical_label_schema_version TEXT NOT NULL,
  split TEXT,
  item_length_chars INTEGER,
  item_length_tokens_if_available INTEGER,
  source_url_or_origin_if_available TEXT,
  raw_metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS source_votes (
  item_id TEXT NOT NULL,
  dataset_id TEXT NOT NULL,
  count_author INTEGER NOT NULL,
  count_other INTEGER NOT NULL,
  count_everybody INTEGER NOT NULL,
  count_nobody INTEGER NOT NULL,
  count_info INTEGER NOT NULL,
  annotation_count INTEGER NOT NULL,
  source_vote_version TEXT NOT NULL,
  PRIMARY KEY (item_id, source_vote_version)
);

CREATE TABLE IF NOT EXISTS source_distributions (
  item_id TEXT NOT NULL,
  dataset_id TEXT NOT NULL,
  source_distribution_version TEXT NOT NULL,
  smoothing_method TEXT NOT NULL,
  alpha REAL NOT NULL,
  p_author REAL NOT NULL,
  p_other REAL NOT NULL,
  p_everybody REAL NOT NULL,
  p_nobody REAL NOT NULL,
  p_info REAL NOT NULL,
  majority_label TEXT NOT NULL,
  majority_support REAL NOT NULL,
  majority_margin REAL NOT NULL,
  entropy REAL NOT NULL,
  entropy_normalized REAL NOT NULL,
  disagreement_bin TEXT NOT NULL,
  posterior_draw_id_or_null TEXT,
  PRIMARY KEY (item_id, source_distribution_version, posterior_draw_id_or_null)
);

CREATE TABLE IF NOT EXISTS prompt_templates (
  prompt_template_id TEXT PRIMARY KEY,
  prompt_mode TEXT NOT NULL,
  prompt_template_hash TEXT NOT NULL,
  template_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prompt_assignments (
  assignment_hash TEXT PRIMARY KEY,
  item_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  prompt_mode TEXT NOT NULL,
  label_order TEXT NOT NULL,
  prompt_paraphrase_id TEXT NOT NULL,
  sample_id INTEGER,
  seed INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS planned_api_calls (
  api_call_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  milestone TEXT NOT NULL,
  component_type TEXT NOT NULL,
  component_name TEXT NOT NULL,
  item_id TEXT NOT NULL,
  dataset_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  prompt_mode TEXT NOT NULL,
  assignment_hash TEXT NOT NULL,
  sample_id INTEGER,
  prompt_hash TEXT NOT NULL,
  request_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'planned',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_registry (
  model_id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  api_route TEXT NOT NULL,
  model_family TEXT NOT NULL,
  model_display_name TEXT NOT NULL,
  provider_model_id TEXT NOT NULL,
  provider_model_version_if_available TEXT,
  open_weight_flag INTEGER NOT NULL,
  structured_output_mode TEXT NOT NULL,
  batch_supported_flag INTEGER NOT NULL,
  sampling_control_available INTEGER NOT NULL,
  logprobs_available INTEGER NOT NULL,
  run_freeze_verified_at TEXT,
  provider_metadata_json TEXT,
  pricing_metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS api_calls_raw (
  api_call_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  milestone TEXT,
  call_type TEXT,
  is_pilot INTEGER NOT NULL DEFAULT 0,
  is_confirmatory INTEGER NOT NULL DEFAULT 0,
  item_id TEXT NOT NULL,
  dataset_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  api_route TEXT NOT NULL,
  prompt_mode TEXT NOT NULL,
  prompt_template_id TEXT,
  prompt_hash TEXT NOT NULL,
  prompt_paraphrase_id TEXT,
  label_order_id TEXT,
  label_order TEXT,
  sample_id INTEGER,
  sampling_condition TEXT,
  temperature_or_null REAL,
  top_p_or_null REAL,
  seed_if_available INTEGER,
  reasoning_effort_or_null TEXT,
  structured_output_mode TEXT,
  request_json TEXT NOT NULL,
  raw_response TEXT,
  provider_response_id TEXT,
  provider_generation_id_or_null TEXT,
  finish_reason_or_null TEXT,
  input_tokens INTEGER,
  output_tokens INTEGER,
  cached_input_tokens_or_null INTEGER,
  cost_usd_if_available REAL,
  timestamp_started TEXT,
  timestamp_completed TEXT,
  api_error_flag INTEGER NOT NULL DEFAULT 0,
  api_error_type TEXT,
  http_status_code INTEGER,
  response_headers_json TEXT,
  error_response_body TEXT,
  transport_error_message TEXT,
  retry_after_seconds REAL,
  terminal_failure_flag INTEGER NOT NULL DEFAULT 0,
  retry_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS api_call_attempts (
  attempt_id TEXT PRIMARY KEY,
  api_call_id TEXT NOT NULL,
  run_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  api_route TEXT NOT NULL,
  prompt_mode TEXT NOT NULL,
  attempt_index INTEGER NOT NULL,
  request_json TEXT NOT NULL,
  raw_response TEXT,
  response_headers_json TEXT,
  http_status_code INTEGER,
  api_error_type TEXT,
  error_response_body TEXT,
  transport_error_message TEXT,
  retry_after_seconds REAL,
  timestamp_started TEXT NOT NULL,
  timestamp_completed TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS parsed_outputs (
  api_call_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  item_id TEXT NOT NULL,
  dataset_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  prompt_mode TEXT NOT NULL,
  validity_status TEXT NOT NULL,
  repair_attempted INTEGER NOT NULL,
  repair_successful INTEGER NOT NULL,
  refusal_flag INTEGER NOT NULL,
  malformed_flag INTEGER NOT NULL,
  off_schema_label_flag INTEGER NOT NULL,
  probability_sum REAL,
  chosen_label TEXT,
  estimated_source_community_agreement REAL,
  moral_certainty REAL,
  p_author REAL,
  p_other REAL,
  p_everybody REAL,
  p_nobody REAL,
  p_info REAL,
  most_likely_label TEXT,
  recognition_status TEXT,
  recognition_confidence REAL,
  parsed_json TEXT
);

CREATE TABLE IF NOT EXISTS metric_outputs (
  metric_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  item_id TEXT NOT NULL,
  dataset_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  prompt_mode_or_pair TEXT NOT NULL,
  source_distribution_version TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  metric_value REAL NOT NULL,
  disagreement_bin TEXT,
  analysis_subset TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS baseline_outputs (
  baseline_output_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  item_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  baseline_type TEXT NOT NULL,
  label_probabilities_json TEXT NOT NULL,
  most_likely_label TEXT NOT NULL,
  source_distribution_version TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_outputs (
  audit_output_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  item_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  audit_type TEXT NOT NULL,
  audit_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS paraphrase_pairs (
  paraphrase_pair_id TEXT PRIMARY KEY,
  item_id TEXT NOT NULL,
  original_text TEXT NOT NULL,
  paraphrased_text TEXT NOT NULL,
  helper_model_id TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exclusion_log (
  exclusion_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  item_id TEXT,
  api_call_id TEXT,
  exclusion_rule TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS run_manifest (
  run_id TEXT PRIMARY KEY,
  manifest_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    if str(path) == ":memory:":
        connection = sqlite3.connect(":memory:")
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = TRUNCATE")
    connection.execute("PRAGMA synchronous = NORMAL")
    return connection


def migrate(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_SQL)
    ensure_columns(
        connection,
        "api_calls_raw",
        {
            "http_status_code": "INTEGER",
            "response_headers_json": "TEXT",
            "error_response_body": "TEXT",
            "transport_error_message": "TEXT",
            "retry_after_seconds": "REAL",
            "terminal_failure_flag": "INTEGER NOT NULL DEFAULT 0",
            "retry_count": "INTEGER NOT NULL DEFAULT 0",
            "milestone": "TEXT",
            "call_type": "TEXT",
            "is_pilot": "INTEGER NOT NULL DEFAULT 0",
            "is_confirmatory": "INTEGER NOT NULL DEFAULT 0",
        },
    )
    ensure_columns(
        connection,
        "api_call_attempts",
        {
            "retry_after_seconds": "REAL",
        },
    )
    connection.commit()


def ensure_columns(connection: sqlite3.Connection, table: str, columns: dict[str, str]) -> None:
    existing = {row["name"] for row in connection.execute(f"PRAGMA table_info({table})")}
    for name, definition in columns.items():
        if name not in existing:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")
