"""Claude Code Stop hook — runs on a synthetic transcript, never on a real session."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("claims_hook", ROOT / "tools" / "claude-code-claims-hook.py")
hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook)


def row(ts: str, role: str, text: str) -> str:
    return json.dumps({"type": role, "timestamp": ts,
                       "message": {"role": role, "content": [{"type": "text", "text": text}]}})


class TestClaimsHook(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="traceweave-hook-")
        self.dir = Path(self.tmp.name)
        self.transcript = self.dir / "session.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, *rows: str) -> None:
        self.transcript.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def hook_input(self, active: bool = False) -> dict:
        return {"session_id": "s1", "transcript_path": str(self.transcript),
                "cwd": str(self.dir), "stop_hook_active": active}

    def test_clean_turn_records_hash_and_stays_silent(self):
        self.write(row("2026-10-10T10:00:00Z", "user", "hi"), row("2026-10-10T10:00:01Z", "assistant", "hello"))
        code, out = hook.run(self.hook_input(), [], block=True)
        self.assertEqual((code, out), (0, None))
        record = json.loads((self.dir / ".traceweave" / "claims" / "s1.jsonl").read_text(encoding="utf-8"))
        self.assertEqual(record["transcript_sha256"], hashlib.sha256(self.transcript.read_bytes()).hexdigest())
        self.assertEqual(record["findings"], [])

    def test_only_last_turn_is_reported(self):
        self.write(
            row("2026-10-10T10:00:00Z", "user", "push?"),
            row("2026-10-10T10:00:01Z", "assistant", "I pushed it."),
            row("2026-10-10T10:01:00Z", "user", "thanks"),
            row("2026-10-10T10:01:01Z", "assistant", "You're welcome."),
        )
        code, out = hook.run(self.hook_input(), [], block=True)
        self.assertEqual((code, out), (0, None))

    def test_block_once_then_inform(self):
        self.write(row("2026-10-10T10:00:00Z", "user", "push?"),
                   row("2026-10-10T10:00:01Z", "assistant", "I pushed it."))
        _, out = hook.run(self.hook_input(active=False), [], block=True)
        self.assertEqual(out["decision"], "block")
        self.assertIn("action-without-tool-call", out["reason"])
        _, out = hook.run(self.hook_input(active=True), [], block=True)
        self.assertNotIn("decision", out)
        self.assertIn("systemMessage", out)

    def test_missing_transcript_is_reported_not_raised(self):
        code, out = hook.run({"transcript_path": str(self.dir / "nope.jsonl")}, [], block=True)
        self.assertEqual(code, 0)
        self.assertIn("not found", out["systemMessage"])


if __name__ == "__main__":
    unittest.main()
