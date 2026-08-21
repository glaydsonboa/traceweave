"""Verification tests — valid, invalid and graph-revision mismatch cases."""

import copy
import json
import unittest
from pathlib import Path

from traceweave.cli import main
from traceweave.verify import verify

from helpers import new_repo


def run_cli(*argv: str) -> tuple[int, str]:
    import contextlib
    import io
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = main(list(argv))
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
    return code, buf.getvalue()


def generated_checkpoint(repo: Path) -> dict:
    run_cli("checkpoint", "--path", str(repo), "--executor", "DeepSeek")
    files = sorted((repo / ".traceweave" / "checkpoints").glob("*.json"))
    return json.loads(files[-1].read_text(encoding="utf-8"))


class TestVerify(unittest.TestCase):

    def test_valid_checkpoint_passes(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        result = verify(checkpoint)
        self.assertTrue(result.ok, result.errors)

    def test_invalid_checkpoint_status_fails(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        checkpoint["status"] = "finished"
        result = verify(checkpoint)
        self.assertFalse(result.ok)
        self.assertTrue(any("status must be one of" in e for e in result.errors))

    def test_invalid_checkpoint_fails(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        broken = copy.deepcopy(checkpoint)
        del broken["session"]["session_id"]
        result = verify(broken)
        self.assertFalse(result.ok)
        self.assertTrue(any("session.session_id" in e for e in result.errors))

    def test_missing_executor_fails(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        broken = copy.deepcopy(checkpoint)
        del broken["session"]["executor"]
        result = verify(broken)
        self.assertFalse(result.ok)
        self.assertTrue(any("session.executor" in e for e in result.errors))

    def test_verify_command_exit_code(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        files = sorted((repo / ".traceweave" / "checkpoints").glob("*.json"))
        code, _ = run_cli("verify", str(files[-1]))
        self.assertEqual(code, 0)

        broken = copy.deepcopy(checkpoint)
        del broken["checkpoint_id"]
        broken_path = repo / "broken.json"
        broken_path.write_text(json.dumps(broken), encoding="utf-8")
        code, _ = run_cli("verify", str(broken_path))
        self.assertEqual(code, 1)

    def test_test_entries_need_explicit_result(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        checkpoint["tests"] = [{"command": "pytest", "result": "maybe"}]
        result = verify(checkpoint)
        self.assertFalse(result.ok)
        self.assertTrue(any("result must be one of" in e for e in result.errors))

    def test_graph_revision_mismatch_fails(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        checkpoint["graph_sync"] = {
            "status": "synced",
            "engine": "graphify",
            "source_commit": "0" * 40,
            "verified_at": "2026-08-21T19:43:00Z",
        }
        result = verify(checkpoint)
        self.assertFalse(result.ok)
        self.assertTrue(any("does not match git.head_commit" in e for e in result.errors))

    def test_graph_synced_matching_passes(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        checkpoint["graph_sync"] = {
            "status": "synced",
            "engine": "graphify",
            "source_commit": checkpoint["git"]["head_commit"],
            "verified_at": "2026-08-21T19:43:00Z",
        }
        result = verify(checkpoint)
        self.assertTrue(result.ok, result.errors)

    def test_null_provenance_is_valid(self):
        repo = new_repo()
        checkpoint = generated_checkpoint(repo)
        checkpoint["provenance"] = {
            "requested_by": None,
            "prompt_generator": None,
            "executor": None,
        }
        result = verify(checkpoint)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
