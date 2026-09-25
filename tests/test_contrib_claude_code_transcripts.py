"""Contributions to simonw/claude-code-transcripts (contributions/claude-code-transcripts)."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "contributions" / "claude-code-transcripts"
QUEUED = ROOT / "queued-prompts"
PLAIN = ROOT / "plain-text-prompts"


def load_accounting():
    spec = importlib.util.spec_from_file_location(
        "account_queued_prompts", QUEUED / "account_queued_prompts.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestQueuedPromptAccounting(unittest.TestCase):

    def test_every_queued_prompt_in_the_example_is_accounted_for(self):
        lines = (QUEUED / "example-session.jsonl").read_text(encoding="utf-8").splitlines()
        counts = load_accounting().account(lines)
        self.assertEqual(counts["enqueued"], 4, "task notifications are not prompts")
        self.assertEqual(counts["delivered_mid_turn"], 1)
        self.assertEqual(counts["delivered_as_user_message"], 1)
        self.assertEqual(counts["delivered_with_changes"], 1)
        self.assertEqual(counts["not_delivered"], 1)

    def test_task_notifications_and_non_human_origins_are_not_prompts(self):
        accounting = load_accounting()
        notification = {"attachment": {"type": "queued_command", "commandMode": "task-notification", "prompt": "x"}}
        agent = {"attachment": {"type": "queued_command", "commandMode": "prompt", "origin": {"kind": "agent"}, "prompt": "x"}}
        human = {"attachment": {"type": "queued_command", "commandMode": "prompt", "origin": {"kind": "human"}, "prompt": "x"}}
        self.assertIsNone(accounting._mid_turn_prompt(notification))
        self.assertIsNone(accounting._mid_turn_prompt(agent))
        self.assertEqual(accounting._mid_turn_prompt(human), "x")


class TestPatches(unittest.TestCase):

    def test_queued_prompts_patch_reads_the_delivery_record(self):
        patch = (QUEUED / "keep-queued-prompts.patch").read_text(encoding="utf-8")
        self.assertIn("+def _queued_user_prompt(obj):", patch)
        self.assertIn('"queued_command"', patch)
        self.assertIn("test_jsonl_keeps_prompts_queued_while_claude_was_working", patch)

    def test_plain_text_patch_escapes_user_prompts(self):
        patch = (PLAIN / "user-prompts-plain-text.patch").read_text(encoding="utf-8")
        self.assertIn("+def render_user_text(text):", patch)
        self.assertIn("html.escape(text)", patch)
        self.assertIn("test_user_prompts_are_rendered_as_plain_text", patch)


if __name__ == "__main__":
    unittest.main()
