from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traceweave import mcp_server


class TraceweaveMcpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Traceweave Test"], cwd=self.root, check=True)
        (self.root / "README.md").write_text("initial\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=self.root, check=True, capture_output=True)
        self.env = patch.dict(
            os.environ,
            {
                "TRACEWEAVE_ROOT": str(self.root),
                "TRACEWEAVE_MCP_SCOPES": "read",
            },
            clear=False,
        )
        self.env.start()

    def tearDown(self) -> None:
        self.env.stop()
        self.tmp.cleanup()

    def test_default_read_scope_does_not_authorize_write(self) -> None:
        mcp_server._require("read")
        with self.assertRaises(PermissionError):
            mcp_server._require("write")

    def test_path_cannot_escape_repository(self) -> None:
        with self.assertRaises(ValueError):
            mcp_server._safe_path("../outside.txt")

    def test_git_internals_are_forbidden(self) -> None:
        with self.assertRaises(ValueError):
            mcp_server._safe_path(".git/config")

    def test_expected_sha_prevents_stale_overwrite(self) -> None:
        target = self.root / "README.md"
        expected = hashlib.sha256(target.read_bytes()).hexdigest()
        with patch.dict(os.environ, {"TRACEWEAVE_MCP_SCOPES": "read,write"}, clear=False):
            result = mcp_server.traceweave_write_text("README.md", "changed\n", expected)
            self.assertEqual(result["before_sha256"], expected)
            with self.assertRaises(RuntimeError):
                mcp_server.traceweave_write_text("README.md", "stale\n", expected)

    def test_commit_refuses_pre_staged_work(self) -> None:
        (self.root / "other.txt").write_text("other\n", encoding="utf-8")
        subprocess.run(["git", "add", "other.txt"], cwd=self.root, check=True)
        (self.root / "new.txt").write_text("new\n", encoding="utf-8")
        with patch.dict(os.environ, {"TRACEWEAVE_MCP_SCOPES": "read,write,publish"}, clear=False):
            with self.assertRaisesRegex(RuntimeError, "another execution has staged paths"):
                mcp_server.traceweave_git_commit(["new.txt"], "should not commit")

    def test_search_query_starting_with_dash_is_searched_not_parsed(self) -> None:
        (self.root / "notes.md").write_text("--open-files-in-pager=boom\n", encoding="utf-8")
        subprocess.run(["git", "add", "notes.md"], cwd=self.root, check=True)
        result = mcp_server.traceweave_search_text("--open-files-in-pager=boom")
        self.assertEqual(result["count"], 1)
        self.assertIn("notes.md", result["results"][0])

    def test_readback_rejects_option_shaped_ref(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not start with '-'"):
            mcp_server.traceweave_git_readback("--output=pwned.txt", "README.md")
        self.assertFalse((self.root / "pwned.txt").exists())

    def test_readback_returns_committed_bytes(self) -> None:
        result = mcp_server.traceweave_git_readback("HEAD", "README.md")
        self.assertEqual(result["content"], "initial\n")
        self.assertEqual(result["sha256"], hashlib.sha256(b"initial\n").hexdigest())

    def test_push_rejects_unknown_and_option_shaped_remote(self) -> None:
        with patch.dict(os.environ, {"TRACEWEAVE_MCP_SCOPES": "read,write,publish"}, clear=False):
            with self.assertRaisesRegex(ValueError, "must not start with '-'"):
                mcp_server.traceweave_git_push("--receive-pack=boom")
            with self.assertRaisesRegex(ValueError, "Unknown remote"):
                mcp_server.traceweave_git_push("https://example.invalid/x.git")

    def test_push_rejects_remote_outside_allowed_repository(self) -> None:
        subprocess.run(
            ["git", "remote", "add", "origin", "https://github.com/someone-else/traceweave.git"],
            cwd=self.root, check=True,
        )
        scopes = {"TRACEWEAVE_MCP_SCOPES": "read,write,publish", "TRACEWEAVE_ALLOWED_REMOTE": "glaydsonboa/traceweave"}
        with patch.dict(os.environ, scopes, clear=False):
            with self.assertRaisesRegex(PermissionError, "not to the allowed repository"):
                mcp_server.traceweave_git_push("origin")

    def test_commit_preserves_trailing_whitespace(self) -> None:
        (self.root / "quote.md").write_text("literal speech with trailing space \n", encoding="utf-8")
        with patch.dict(os.environ, {"TRACEWEAVE_MCP_SCOPES": "read,write,publish"}, clear=False):
            result = mcp_server.traceweave_git_commit(["quote.md"], "record literal quote")
        self.assertEqual(result["paths"], ["quote.md"])
        stored = subprocess.run(["git", "show", "HEAD:quote.md"], cwd=self.root, capture_output=True, check=True).stdout
        self.assertEqual(stored, b"literal speech with trailing space \n")


if __name__ == "__main__":
    unittest.main()
