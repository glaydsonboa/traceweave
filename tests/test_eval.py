"""TraceEval MVP: stable expectations, source custody and evidence limits."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traceweave.eval.engine import evaluate_case, validate_case, SCHEMA


class TestTraceEval(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.log = Path(self.tmp.name) / "events.jsonl"
        self.log.write_text("\n".join([
            json.dumps({"ts": "2026-10-10T10:00:00Z", "role": "user", "kind": "text", "text": "Did you push?"}),
            json.dumps({"ts": "2026-10-10T10:00:05Z", "role": "assistant", "kind": "text", "text": "Yes, I pushed the branch."}),
        ]) + "\n", encoding="utf-8")
        self.case = {
            "schema": SCHEMA,
            "case_id": "test-e01",
            "source": {"kind": "native_jsonl", "sha256": hashlib.sha256(self.log.read_bytes()).hexdigest()},
            "expectations": [{"check": "action-without-tool-call", "min_count": 1, "max_count": 1}],
        }

    def test_real_detector_finds_unbacked_action(self):
        report = evaluate_case(self.case, evidence=self.log)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["finding_counts"], {"action-without-tool-call": 1})
        self.assertEqual(report["events"], 2)
        self.assertEqual(report["score"], 1.0)

    def test_unmet_expectation_is_a_failed_regression(self):
        self.case["expectations"][0]["min_count"] = 2
        self.assertEqual(evaluate_case(self.case, evidence=self.log)["status"], "failed")

    def test_hash_mismatch_never_executes_detector(self):
        self.case["source"]["sha256"] = "0" * 64
        with patch("traceweave.claims.audit") as detector:
            result = evaluate_case(self.case, evidence=self.log)
        self.assertEqual(result["status"], "integrity_failed")
        detector.assert_not_called()

    def test_no_file_is_unobserved_not_a_failure_score(self):
        report = evaluate_case(self.case, evidence=None)
        self.assertEqual(report["status"], "not_observed")
        self.assertIsNone(report["score"])

    def test_missing_path_is_unobserved(self):
        report = evaluate_case(self.case, evidence=self.log.with_name("absent.jsonl"))
        self.assertEqual(report["status"], "not_observed")

    def test_markdown_custody_is_not_native_execution_proof(self):
        self.case["source"]["kind"] = "markdown_transcript"
        report = evaluate_case(self.case, evidence=self.log)
        self.assertEqual(report["status"], "not_observed")
        self.assertIsNone(report["score"])

    def test_no_expectations_is_not_scored(self):
        self.case["expectations"] = []
        result = evaluate_case(self.case, evidence=self.log)
        self.assertEqual(result["status"], "not_observed")

    def test_no_valid_events_is_not_false_pass(self):
        self.log.write_text("some invalid line\n", encoding="utf-8")
        self.case["source"]["sha256"] = hashlib.sha256(self.log.read_bytes()).hexdigest()
        result = evaluate_case(self.case, evidence=self.log)
        self.assertEqual(result["status"], "invalid_input")

    def test_rejects_duplicate_rules(self):
        self.case["expectations"].append(dict(self.case["expectations"][0]))
        with self.assertRaises(ValueError):
            validate_case(self.case)

    def test_rejects_nonsha(self):
        self.case["source"]["sha256"] = "xyz"
        with self.assertRaises(ValueError):
            validate_case(self.case)

    def test_rejects_boolean_min_count(self):
        self.case["expectations"][0]["min_count"] = True
        with self.assertRaises(ValueError):
            validate_case(self.case)

    def test_same_bytes_same_report(self):
        self.assertEqual(evaluate_case(self.case, evidence=self.log), evaluate_case(self.case, evidence=self.log))


if __name__ == "__main__":
    unittest.main()
