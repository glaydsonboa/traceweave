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


if __name__ == "__main__":
    unittest.main()
