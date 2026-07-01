from __future__ import annotations

from http import client as http_client
import os
import unittest
from unittest.mock import patch

from common.llm_api import (
    ApiFailureKind,
    RetryConfig,
    classify_api_failure,
    load_provider_configs,
    parse_json_output,
    parse_provider_map,
    post_json_with_retry,
)
from common.llm_api.json_output import JsonOutputStatus


class CommonApiTests(unittest.TestCase):
    def test_extracts_one_json_object_and_validates(self) -> None:
        parsed = parse_json_output(
            'Answer follows: {"label":"yes","score":0.8}\nDone.',
            required_fields=("label", "score"),
            allowed_values={"label": {"yes", "no"}},
            numeric_ranges={"score": (0.0, 1.0)},
        )
        self.assertEqual(parsed.status, JsonOutputStatus.VALID_EXTRACTED_JSON)
        self.assertEqual(parsed.value, {"label": "yes", "score": 0.8})

    def test_rejects_ambiguous_multiple_objects(self) -> None:
        parsed = parse_json_output('{"a":1} then {"a":2}')
        self.assertEqual(parsed.status, JsonOutputStatus.INVALID_JSON)

    def test_provider_map(self) -> None:
        self.assertEqual(
            parse_provider_map("custom=openai,qwen/x=openrouter"),
            {"custom": "openai", "qwen/x": "openrouter"},
        )

    def test_openrouter_account_limit_is_retryable(self) -> None:
        failure = classify_api_failure(
            http_status_code=403,
            error_response_body='{"error":{"message":"Key limit exceeded (total limit)"}}',
        )
        self.assertEqual(failure.kind, ApiFailureKind.RATE_LIMIT)
        self.assertTrue(failure.retryable)

    def test_original_llama_env_aliases_load_openrouter(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "LLAMA_API_KEY": "test-key",
                    "LLAMA_BASE_URL": "https://example.test/v1",
                },
                clear=True,
            ),
            patch("common.llm_api.config._read_windows_user_env", return_value=None),
        ):
            configs, routes = load_provider_configs(["qwen/example"])
        self.assertEqual(routes["qwen/example"], "openrouter")
        self.assertEqual(configs["openrouter"].api_key, "test-key")
        self.assertEqual(configs["openrouter"].base_url, "https://example.test/v1")

    def test_retries_incomplete_read(self) -> None:
        calls = 0

        class Headers:
            def items(self):
                return []

        class Response:
            status = 200
            headers = Headers()

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

            def read(self):
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise http_client.IncompleteRead(b"partial")
                return b'{"ok":true}'

        with patch("common.llm_api.providers.request.urlopen", return_value=Response()):
            body, status, latency, headers, attempts = post_json_with_retry(
                "https://example.test",
                {},
                {"prompt": "hello"},
                RetryConfig(max_attempts=2, base_backoff_seconds=0, jitter_seconds=0),
            )
        self.assertEqual(body, {"ok": True})
        self.assertEqual(status, 200)
        self.assertGreaterEqual(latency, 0)
        self.assertEqual(headers, {})
        self.assertEqual(attempts, 2)


if __name__ == "__main__":
    unittest.main()
