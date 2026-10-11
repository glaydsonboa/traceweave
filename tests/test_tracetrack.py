"""TraceTrack server — discovery, PROMPT_ID gate, job run with a stub command, HTTP guards.

Never touches the real ~/.claude or ~/.codex: every test points the roots at a
temporary directory and runs jobs with a stub executor (the Python interpreter).
"""

import http.client
import json
import os
import re
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

from traceweave import tracetrack as tt


def write_claude_session(root: Path, name: str, rows: list[dict]) -> Path:
    project = root / "proj"
    project.mkdir(parents=True, exist_ok=True)
    path = project / f"{name}.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def claude_rows(model: str, assistant_text: str) -> list[dict]:
    return [
        {"type": "user", "timestamp": "2026-10-11T10:00:00Z", "message": {"role": "user", "content": "Did you push?"}},
        {"type": "assistant", "timestamp": "2026-10-11T10:00:05Z",
         "message": {"role": "assistant", "model": model, "content": [{"type": "text", "text": assistant_text}]}},
    ]


class Env(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="tracetrack-")
        base = Path(self.tmp.name)
        self.claude_root, self.codex_root, self.state = base / "claude", base / "codex", base / "state"
        self.claude_root.mkdir()
        self.codex_root.mkdir()
        self.env = mock.patch.dict(os.environ, {
            "TRACETRACK_CLAUDE_ROOT": str(self.claude_root),
            "TRACETRACK_CODEX_ROOT": str(self.codex_root),
        })
        self.env.start()
        self.store = tt.JobStore(base, [], state_dir=self.state)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()


class TestDiscovery(Env):

    def test_sessions_found_and_deepseek_told_apart(self):
        write_claude_session(self.claude_root, "a", claude_rows("claude-opus-5-5", "Hello."))
        write_claude_session(self.claude_root, "b", claude_rows("deepseek-v4-pro", "Hello."))
        rollout = self.codex_root / "2026" / "10" / "11"
        rollout.mkdir(parents=True)
        (rollout / "rollout-x-01abc.jsonl").write_text("{}\n", encoding="utf-8")
        by_name = {s["name"]: s["executor"] for s in tt.discover_sessions()}
        self.assertEqual(by_name, {"a.jsonl": "claude", "b.jsonl": "deepseek", "rollout-x-01abc.jsonl": "codex"})

    def test_summary_carries_hash_prompt_and_findings(self):
        path = write_claude_session(self.claude_root, "s", claude_rows("claude-opus-5-5", "Yes, I pushed the branch."))
        summary = tt.summarize_session(path, [])
        self.assertEqual(len(summary["sha256"]), 64)
        self.assertEqual(summary["first_prompt"], "Did you push?")
        self.assertEqual([f["check"] for f in summary["findings"]], ["action-without-tool-call"])


class TestGate(Env):

    def test_prompt_id_has_random_tail(self):
        ids = {tt.new_prompt_id() for _ in range(50)}
        self.assertEqual(len(ids), 50)
        self.assertTrue(all(re.fullmatch(r"TW-\d{8}-\d{6}-[A-HJ-NP-Z2-9]{8}", i) for i in ids))

    def test_public_view_never_exposes_the_full_prompt_id_before_authorization(self):
        job = self.store.create("claude", "hello")
        self.assertNotIn(job._prompt_id, json.dumps(job.public()))

    def test_wrong_code_three_times_locks(self):
        job = self.store.create("claude", "hello")
        for _ in range(2):
            with self.assertRaises(ValueError):
                self.store.authorize(job.job_id, "TW-WRONG")
        with self.assertRaisesRegex(ValueError, "locked"):
            self.store.authorize(job.job_id, "TW-WRONG")
        with self.assertRaises(ValueError):
            self.store.authorize(job.job_id, job._prompt_id)
        self.assertEqual(job.status, "locked")

    def test_expired_code_is_refused(self):
        job = self.store.create("claude", "hello")
        job._expires = time.time() - 1
        with self.assertRaisesRegex(ValueError, "expired"):
            self.store.authorize(job.job_id, job._prompt_id)

    def test_deepseek_without_key_fails_clearly(self):
        with mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": ""}):
            with self.assertRaisesRegex(RuntimeError, "DEEPSEEK_API_KEY"):
                tt._command("deepseek", "hi")

    def test_correct_code_runs_job_and_audits_its_transcript(self):
        # The stub prints a stream line with a session id, then writes that session's
        # transcript where the server will look for it.
        transcript = self.claude_root / "proj" / "sess-1.jsonl"
        script = (
            "import json,pathlib,sys;"
            f"p=pathlib.Path(r'{transcript}');p.parent.mkdir(parents=True,exist_ok=True);"
            "p.write_text(json.dumps({'type':'user','timestamp':'t1','message':{'role':'user','content':'push?'}})+'\\n'"
            "+json.dumps({'type':'assistant','timestamp':'t2','message':{'role':'assistant','content':[{'type':'text','text':'I pushed it.'}]}})+'\\n');"
            "print(json.dumps({'type':'system','session_id':'sess-1'}));"
            "print(json.dumps({'type':'result','subtype':'success','result':'ok'}))"
        )
        with mock.patch.dict(os.environ, {"TRACETRACK_CMD_CLAUDE": json.dumps([sys.executable, "-c", script])}):
            job = self.store.create("claude", "push it")
            self.store.authorize(job.job_id, " " + job._prompt_id.lower() + " ")  # spaces and case tolerated
            for _ in range(100):
                if job.status != "running":
                    break
                time.sleep(0.05)
        self.assertEqual(job.status, "done", job.error)
        self.assertEqual(job.transcript, str(transcript))
        self.assertEqual([f["check"] for f in job.findings], ["action-without-tool-call"])
        self.assertTrue(any("result" in line for line in job.log))
        events = [json.loads(l)["event"] for l in (self.state / "jobs.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(events, ["created", "authorized", "done"])


class TestRestore(Env):

    def test_queue_survives_restart_without_the_prompt_id(self):
        waiting = self.store.create("claude", "never authorized")
        self.assertNotIn(waiting._prompt_id, (self.state / "jobs.jsonl").read_text(encoding="utf-8"))
        restarted = tt.JobStore(Path(self.tmp.name), [], state_dir=self.state)
        job = restarted.jobs[waiting.job_id]
        self.assertEqual(job.status, "expired")
        self.assertEqual(job.prompt, "never authorized")
        with self.assertRaises(ValueError):
            restarted.authorize(job.job_id, waiting._prompt_id)


class TestHttp(Env):

    def setUp(self):
        super().setUp()
        self.httpd = tt.make_server(0, Path(self.tmp.name), [], state_dir=self.state)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def req(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        h = {"Host": f"127.0.0.1:{self.port}"}
        h.update(headers or {})
        data = json.dumps(body).encode() if body is not None else None
        if data is not None:
            h.setdefault("Content-Type", "application/json")
        conn.request(method, path, body=data, headers=h)
        r = conn.getresponse()
        raw = r.read()
        conn.close()
        return r.status, raw

    def test_page_and_state_served(self):
        status, raw = self.req("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"TraceTrack", raw)
        status, raw = self.req("GET", "/api/state")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(raw)["executors"], ["claude", "codex", "deepseek"])

    def test_foreign_host_rejected(self):
        status, _ = self.req("GET", "/api/sessions", headers={"Host": "evil.example"})
        self.assertEqual(status, 403)

    def test_cross_origin_post_rejected(self):
        status, _ = self.req("POST", "/api/jobs", {"executor": "claude", "prompt": "x"},
                             headers={"Origin": "https://evil.example"})
        self.assertEqual(status, 403)

    def test_post_without_json_rejected(self):
        status, _ = self.req("POST", "/api/jobs", headers={"Content-Type": "text/plain"})
        self.assertEqual(status, 415)

    def test_unknown_session_id_cannot_read_arbitrary_files(self):
        status, _ = self.req("GET", "/api/session?id=../../etc/passwd")
        self.assertEqual(status, 404)

    def test_job_flow_over_http(self):
        status, raw = self.req("POST", "/api/jobs", {"executor": "claude", "prompt": "hello"})
        self.assertEqual(status, 201)
        job = json.loads(raw)
        self.assertEqual(job["status"], "awaiting_authorization")
        status, raw = self.req("POST", f"/api/jobs/{job['job_id']}/authorize", {"prompt_id": "TW-NOPE"})
        self.assertEqual(status, 400)
        self.assertIn("wrong PROMPT_ID", json.loads(raw)["error"])


if __name__ == "__main__":
    unittest.main()
