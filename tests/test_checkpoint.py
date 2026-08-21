"""Checkpoint generation tests — structure, provenance and persistence."""

import json
import unittest

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


class TestCheckpointGeneration(unittest.TestCase):

    def test_checkpoint_generation(self):
        repo = new_repo()
        code, out = run_cli(
            "checkpoint", "--path", str(repo),
            "--summary", "Add configuration validation",
            "--executor", "DeepSeek",
        )
        self.assertEqual(code, 0, out)
        out_path = repo / ".traceweave" / "checkpoints"
        files = list(out_path.glob("*.json"))
        self.assertEqual(len(files), 1)
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(checkpoint["traceweave_version"], "0.1")
        self.assertIsInstance(checkpoint["checkpoint_id"], str)
        self.assertEqual(checkpoint["work"]["summary"], "Add configuration validation")
        self.assertEqual(checkpoint["session"]["executor"], "DeepSeek")
        self.assertEqual(checkpoint["status"], "partial")
        self.assertEqual(checkpoint["git"]["working_tree"], "clean")
        self.assertEqual(checkpoint["graph_sync"]["status"], "unknown")
        self.assertEqual(
            checkpoint["tests"],
            [{"command": None, "result": "not_run", "evidence": None}],
        )
        self.assertEqual(checkpoint["git"]["base_commit"], checkpoint["git"]["head_commit"])

    def test_unknown_provenance_is_null(self):
        repo = new_repo()
        code, _ = run_cli("checkpoint", "--path", str(repo), "--executor", "DeepSeek")
        self.assertEqual(code, 0)
        files = list((repo / ".traceweave" / "checkpoints").glob("*.json"))
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertIsNone(checkpoint["provenance"]["requested_by"])
        self.assertIsNone(checkpoint["provenance"]["prompt_generator"])
        self.assertEqual(checkpoint["provenance"]["executor"]["name"], "DeepSeek")
        self.assertIsNone(checkpoint["provenance"]["executor"]["type"])

    def test_provenance_has_no_inferred_chain(self):
        repo = new_repo()
        code, _ = run_cli(
            "checkpoint", "--path", str(repo), "--executor", "DeepSeek",
            "--requested-by", "Glaydson", "--prompt-generator", "ChatGPT",
        )
        self.assertEqual(code, 0)
        files = list((repo / ".traceweave" / "checkpoints").glob("*.json"))
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertNotIn("chain", checkpoint["provenance"])
        self.assertEqual(
            set(checkpoint["provenance"].keys()),
            {"requested_by", "prompt_generator", "executor"},
        )

    def test_requested_by_preserves_explicit_name_without_inferred_type(self):
        repo = new_repo()
        code, _ = run_cli(
            "checkpoint", "--path", str(repo), "--executor", "DeepSeek",
            "--requested-by", "Glaydson",
        )
        self.assertEqual(code, 0)
        files = list((repo / ".traceweave" / "checkpoints").glob("*.json"))
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        link = checkpoint["provenance"]["requested_by"]
        self.assertEqual(link, {"type": None, "name": "Glaydson"})

    def test_prompt_generator_preserves_explicit_name_without_inferred_type(self):
        repo = new_repo()
        code, _ = run_cli(
            "checkpoint", "--path", str(repo), "--executor", "DeepSeek",
            "--prompt-generator", "ChatGPT",
        )
        self.assertEqual(code, 0)
        files = list((repo / ".traceweave" / "checkpoints").glob("*.json"))
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        link = checkpoint["provenance"]["prompt_generator"]
        self.assertEqual(link, {"type": None, "name": "ChatGPT"})

    def test_executor_preserves_explicit_name_without_inferred_type(self):
        repo = new_repo()
        code, _ = run_cli("checkpoint", "--path", str(repo), "--executor", "Codex CLI")
        self.assertEqual(code, 0)
        files = list((repo / ".traceweave" / "checkpoints").glob("*.json"))
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        link = checkpoint["provenance"]["executor"]
        self.assertEqual(link, {"type": None, "name": "Codex CLI"})

    def test_generated_checkpoint_passes_verification(self):
        repo = new_repo()
        code, _ = run_cli(
            "checkpoint", "--path", str(repo), "--executor", "DeepSeek",
            "--requested-by", "Glaydson",
        )
        self.assertEqual(code, 0)
        files = list((repo / ".traceweave" / "checkpoints").glob("*.json"))
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        result = verify(checkpoint)
        self.assertTrue(result.ok, result.errors)

    def test_executor_is_required(self):
        repo = new_repo()
        code, _ = run_cli("checkpoint", "--path", str(repo))
        self.assertNotEqual(code, 0)
        self.assertFalse((repo / ".traceweave" / "checkpoints").exists())

    def test_session_is_stable_across_checkpoints(self):
        repo = new_repo()
        run_cli("checkpoint", "--path", str(repo), "--executor", "DeepSeek")
        run_cli("checkpoint", "--path", str(repo), "--executor", "DeepSeek")
        files = sorted((repo / ".traceweave" / "checkpoints").glob("*.json"))
        self.assertEqual(len(files), 2)
        first = json.loads(files[0].read_text(encoding="utf-8"))
        second = json.loads(files[1].read_text(encoding="utf-8"))
        self.assertEqual(first["session"]["session_id"], second["session"]["session_id"])
        self.assertEqual(first["session"]["base_commit"], second["session"]["base_commit"])

    def test_dirty_tree_is_recorded(self):
        repo = new_repo()
        (repo / "uncommitted.txt").write_text("x\n", encoding="utf-8")
        code, _ = run_cli("checkpoint", "--path", str(repo), "--executor", "DeepSeek")
        self.assertEqual(code, 0)
        files = list((repo / ".traceweave" / "checkpoints").glob("*.json"))
        checkpoint = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(checkpoint["git"]["working_tree"], "dirty")
        self.assertIn("uncommitted.txt", checkpoint["work"]["files_changed"])

    def test_detached_head_fails(self):
        repo = new_repo()
        from helpers import run_git
        run_git(repo, "checkout", "-q", "--detach", "HEAD")
        code, _ = run_cli("checkpoint", "--path", str(repo), "--executor", "DeepSeek")
        self.assertNotEqual(code, 0)
        self.assertFalse((repo / ".traceweave" / "checkpoints").exists())

    def test_repository_without_head_fails(self):
        from helpers import new_empty_repo
        repo = new_empty_repo()
        code, _ = run_cli("checkpoint", "--path", str(repo), "--executor", "DeepSeek")
        self.assertNotEqual(code, 0)
        self.assertFalse((repo / ".traceweave" / "checkpoints").exists())


if __name__ == "__main__":
    unittest.main()
