"""TraceTrack — local web page over ``traceweave claims``.

Serves one page on 127.0.0.1 that:

- lists the native session logs on this machine (Claude Code, Codex; DeepSeek
  runs under the Claude Code harness and is told apart by its model name);
- opens a session: first prompt (extracted, never generated), the tool calls it
  made, its last message, the SHA-256 of the log and the ``traceweave claims``
  findings;
- runs jobs: the composer creates a job with a PROMPT_ID; the job starts only
  after that PROMPT_ID is typed back. The PROMPT_ID travels out of band: by SMS
  when Twilio is configured, otherwise printed in the terminal that runs the
  server (the machine of the developer). The page never shows it.

Local only: the server binds to 127.0.0.1, rejects other Host headers (DNS
rebinding) and requires a same-origin JSON body on every POST. Nothing leaves
the machine except the optional SMS.

Standard library only.
"""

from __future__ import annotations

import getpass
import hashlib
import hmac
import json
import os
import secrets
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
from base64 import b64encode
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .claims import _excerpt, audit, load_events

STATIC = Path(__file__).resolve().parent / "tracetrack_static"
EXECUTORS = ("claude", "codex", "deepseek")
AUTH_TTL_SECONDS = 600
AUTH_MAX_ATTEMPTS = 3
LOG_LINES_KEPT = 400

# --------------------------------------------------------------------------- sessions


def _claude_root() -> Path:
    return Path(os.environ.get("TRACETRACK_CLAUDE_ROOT", Path.home() / ".claude" / "projects"))


def _codex_root() -> Path:
    return Path(os.environ.get("TRACETRACK_CODEX_ROOT", Path.home() / ".codex" / "sessions"))


def _session_id(path: Path) -> str:
    return hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:12]


def _claude_executor(path: Path) -> str:
    """'deepseek' when the session's assistant messages name a DeepSeek model."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for n, line in enumerate(fh):
                if '"model"' in line and '"assistant"' in line:
                    return "deepseek" if '"model":"deepseek' in line.replace(" ", "").lower() else "claude"
                if n > 400:
                    break
    except OSError:
        pass
    return "claude"


def discover_sessions(limit: int = 40) -> list[dict]:
    found: list[tuple[float, Path, str]] = []
    croot, xroot = _claude_root(), _codex_root()
    if croot.is_dir():
        for p in croot.glob("*/*.jsonl"):
            found.append((p.stat().st_mtime, p, "claude"))
    if xroot.is_dir():
        for p in xroot.rglob("rollout-*.jsonl"):
            found.append((p.stat().st_mtime, p, "codex"))
    found.sort(key=lambda t: t[0], reverse=True)
    out = []
    for mtime, p, kind in found[:limit]:
        st = p.stat()
        out.append({
            "id": _session_id(p),
            "executor": _claude_executor(p) if kind == "claude" else "codex",
            "name": p.name,
            "path": str(p),
            "modified": datetime.fromtimestamp(mtime, timezone.utc).isoformat(timespec="seconds"),
            "bytes": st.st_size,
        })
    return out


_SUMMARY_CACHE: dict[tuple[str, float, int], dict] = {}
_SUMMARY_LOCK = threading.Lock()


def summarize_session(path: Path, repos: list[Path]) -> dict:
    st = path.stat()
    key = (str(path), st.st_mtime, st.st_size)
    with _SUMMARY_LOCK:
        if key in _SUMMARY_CACHE:
            return _SUMMARY_CACHE[key]
    data = path.read_bytes()
    events = load_events(path)
    # Harness injections arrive as user messages (Codex: AGENTS.md, <environment_context>;
    # Claude Code: <command-…>, <system-reminder>); they are not prompts the person typed.
    prompts = [e for e in events if e.role == "user" and e.kind == "text" and e.text.strip()
               and not e.text.lstrip().startswith(("<", "# AGENTS.md instructions"))]
    calls = [e for e in events if e.kind == "tool_call"]
    answers = [e for e in events if e.role == "assistant" and e.kind == "text" and e.text.strip()]
    report = audit(path, repos=repos)
    summary = {
        "path": str(path),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "events": len(events),
        "first_prompt": _excerpt(prompts[0].text, 400) if prompts else None,
        "last_prompt": _excerpt(prompts[-1].text, 400) if prompts else None,
        "prompts": len(prompts),
        "tool_calls": len(calls),
        "recent_actions": [{"ts": e.ts, "line": e.line, "action": _excerpt(e.text, 160)} for e in calls[-25:]],
        "last_answer": _excerpt(answers[-1].text, 600) if answers else None,
        "findings": report["findings"],
        "counts": report["counts"],
    }
    with _SUMMARY_LOCK:
        _SUMMARY_CACHE[key] = summary
    return summary


# --------------------------------------------------------------------------- jobs


@dataclass
class Job:
    job_id: str
    executor: str
    prompt: str
    workdir: str
    created_at: str
    status: str = "awaiting_authorization"   # → running → done | failed | expired | locked
    delivery: str = ""
    attempts: int = 0
    started_at: str | None = None
    ended_at: str | None = None
    exit_code: int | None = None
    transcript: str | None = None
    findings: list = field(default_factory=list)
    log: list = field(default_factory=list)
    error: str | None = None
    _prompt_id: str = ""
    _expires: float = 0.0

    def public(self) -> dict:
        d = {k: v for k, v in asdict(self).items() if not k.startswith("_")}
        d["prompt_id_hint"] = self._prompt_id[:12] + "…" if self.status == "awaiting_authorization" else self._prompt_id
        return d


def new_prompt_id(now: datetime | None = None) -> str:
    """TW-<UTC date>-<UTC time>-<8 random chars>. The random tail is what makes
    it usable as a one-time code: date and time alone are guessable."""
    now = now or datetime.now(timezone.utc)
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O, 1/I
    tail = "".join(secrets.choice(alphabet) for _ in range(8))
    return f"TW-{now:%Y%m%d-%H%M%S}-{tail}"


def _normalize_code(code: str) -> str:
    return "".join(code.split()).upper()


def deliver_prompt_id(job: "Job") -> str:
    """Send the PROMPT_ID out of band. Returns a description of the channel."""
    sid, token = os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN")
    sender, to = os.environ.get("TWILIO_FROM"), os.environ.get("TRACETRACK_SMS_TO")
    body = f"traceweave: PROMPT_ID do job {job.job_id}: {job._prompt_id}"
    if sid and token and sender and to:
        req = urllib.request.Request(
            f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
            data=urllib.parse.urlencode({"From": sender, "To": to, "Body": body}).encode(),
            headers={"Authorization": "Basic " + b64encode(f"{sid}:{token}".encode()).decode()},
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                if 200 <= resp.status < 300:
                    return f"sms:{to[:-4]}****"
        except OSError as exc:
            print(f"[tracetrack] SMS failed ({exc}); falling back to terminal", file=sys.stderr)
    print(f"\n[tracetrack] {body}\n", file=sys.stderr, flush=True)
    return "terminal"


def _command(executor: str, prompt: str) -> tuple[list[str], dict]:
    """Command and extra environment for one executor. ``TRACETRACK_CMD_<EXECUTOR>``
    (a JSON list, with ``{prompt}`` placeholders) overrides the default."""
    override = os.environ.get(f"TRACETRACK_CMD_{executor.upper()}")
    if override:
        return [part.replace("{prompt}", prompt) for part in json.loads(override)], {}
    if executor == "codex":
        return ["codex", "exec", "--json", prompt], {}
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose"]
    if executor == "deepseek":
        key = os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("DEEPSEEK_API_KEY is not set in the server environment")
        env = {"ANTHROPIC_BASE_URL": os.environ.get("TRACETRACK_DEEPSEEK_URL", "https://api.deepseek.com/anthropic"),
               "ANTHROPIC_AUTH_TOKEN": key}
        if os.environ.get("TRACETRACK_DEEPSEEK_MODEL"):
            env["ANTHROPIC_MODEL"] = os.environ["TRACETRACK_DEEPSEEK_MODEL"]
        return cmd, env
    return cmd, {}


def _find_transcript(executor: str, session_id: str) -> Path | None:
    if not session_id:
        return None
    root = _codex_root() if executor == "codex" else _claude_root()
    pattern = f"rollout-*{session_id}*.jsonl" if executor == "codex" else f"{session_id}.jsonl"
    hits = sorted(root.rglob(pattern), key=lambda p: p.stat().st_mtime, reverse=True) if root.is_dir() else []
    return hits[0] if hits else None


class JobStore:
    def __init__(self, workdir: Path, repos: list[Path], state_dir: Path | None = None):
        self.workdir = workdir
        self.repos = repos
        self.jobs: dict[str, Job] = {}
        self.lock = threading.Lock()
        self.state_file = (state_dir or Path.home() / ".traceweave" / "tracetrack") / "jobs.jsonl"
        self._restore()

    def _restore(self) -> None:
        """Rebuild the queue from the event record (last row per job wins). The PROMPT_ID is
        never written to disk, so a job still waiting for it cannot be authorized after a
        restart: it comes back expired. A job that was running was cut by the restart."""
        if not self.state_file.is_file():
            return
        last: dict[str, dict] = {}
        with open(self.state_file, encoding="utf-8") as fh:
            for raw in fh:
                try:
                    row = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if isinstance(row, dict) and row.get("job_id"):
                    last[row["job_id"]] = row
        fields = {f for f in Job.__dataclass_fields__ if not f.startswith("_")}
        for job_id, row in last.items():
            job = Job(**{k: v for k, v in row.items() if k in fields})
            if job.status == "awaiting_authorization":
                job.status, job.error = "expired", "server restarted before authorization"
            elif job.status == "running":
                job.status, job.error = "failed", "server restarted during the run"
            self.jobs[job_id] = job

    def _record(self, job: Job, event: str) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "a", encoding="utf-8") as fh:
            row = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "event": event}
            row.update({k: v for k, v in job.public().items() if k != "log"})
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    def create(self, executor: str, prompt: str) -> Job:
        if executor not in EXECUTORS:
            raise ValueError(f"executor must be one of {EXECUTORS}")
        if not prompt.strip():
            raise ValueError("prompt is empty")
        job = Job(job_id=secrets.token_hex(4), executor=executor, prompt=prompt.strip(),
                  workdir=str(self.workdir), created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        job._prompt_id = new_prompt_id()
        job._expires = time.time() + AUTH_TTL_SECONDS
        with self.lock:
            self.jobs[job.job_id] = job
        job.delivery = deliver_prompt_id(job)
        self._record(job, "created")
        return job

    def authorize(self, job_id: str, code: str) -> Job:
        with self.lock:
            job = self.jobs.get(job_id)
            if job is None:
                raise KeyError(job_id)
            if job.status != "awaiting_authorization":
                raise ValueError(f"job is {job.status}")
            if time.time() > job._expires:
                job.status = "expired"
                self._record(job, "expired")
                raise ValueError("PROMPT_ID expired; create the job again")
            job.attempts += 1
            if not hmac.compare_digest(_normalize_code(code), job._prompt_id):
                if job.attempts >= AUTH_MAX_ATTEMPTS:
                    job.status = "locked"
                    self._record(job, "locked")
                    raise ValueError("wrong PROMPT_ID; job locked after 3 attempts")
                self._record(job, "rejected")
                raise ValueError(f"wrong PROMPT_ID ({AUTH_MAX_ATTEMPTS - job.attempts} attempt(s) left)")
            job.status = "running"
            job.started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._record(job, "authorized")
        threading.Thread(target=self._run, args=(job,), daemon=True).start()
        return job

    def _run(self, job: Job) -> None:
        session_id = ""
        try:
            cmd, extra_env = _command(job.executor, job.prompt)
            exe = shutil.which(cmd[0]) or cmd[0]
            env = {**os.environ, **extra_env}
            proc = subprocess.Popen([exe, *cmd[1:]], cwd=job.workdir, env=env, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, encoding="utf-8", errors="replace")
            for raw in proc.stdout:
                line = raw.rstrip("\n")
                session_id = session_id or _session_from_line(line)
                with self.lock:
                    job.log.append(_display_line(line))
                    del job.log[:-LOG_LINES_KEPT]
            job.exit_code = proc.wait()
            job.status = "done" if job.exit_code == 0 else "failed"
        except Exception as exc:  # noqa: BLE001 — any failure is reported on the job
            job.status, job.error = "failed", str(exc)
        job.ended_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        transcript = _find_transcript(job.executor, session_id)
        if transcript is not None:
            job.transcript = str(transcript)
            try:
                job.findings = audit(transcript, repos=self.repos)["findings"]
            except OSError as exc:
                job.error = f"audit failed: {exc}"
        self._record(job, job.status)

    def list(self) -> list[dict]:
        with self.lock:
            jobs = sorted(self.jobs.values(), key=lambda j: j.created_at, reverse=True)
            return [j.public() for j in jobs]


def _session_from_line(line: str) -> str:
    try:
        obj = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return ""
    if not isinstance(obj, dict):
        return ""
    return str(obj.get("session_id") or obj.get("thread_id") or "")


def _display_line(line: str) -> str:
    """One readable line per stream event: assistant text, tool use, or the raw line."""
    try:
        obj = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return _excerpt(line, 300)
    if not isinstance(obj, dict):
        return _excerpt(line, 300)
    msg = obj.get("message") or {}
    parts = msg.get("content") if isinstance(msg, dict) else None
    if isinstance(parts, list):
        out = []
        for p in parts:
            if p.get("type") == "text":
                out.append(p.get("text", ""))
            elif p.get("type") == "tool_use":
                out.append(f"→ {p.get('name')} {json.dumps(p.get('input'), ensure_ascii=False)}")
            elif p.get("type") == "tool_result":
                out.append("← result")
        if out:
            return _excerpt(" ".join(out), 300)
    if obj.get("type") == "result":
        return f"■ result: {obj.get('subtype', '')} {_excerpt(str(obj.get('result', '')), 200)}"
    item = obj.get("item") or {}
    if isinstance(item, dict) and item.get("type"):
        text = item.get("text") or item.get("command") or ""
        return _excerpt(f"{item['type']}: {text}", 300)
    return _excerpt(obj.get("type", line) if isinstance(obj.get("type"), str) else line, 300)


# --------------------------------------------------------------------------- HTTP


class Handler(BaseHTTPRequestHandler):
    server_version = "TraceTrack"
    store: JobStore
    repos: list[Path]
    port: int

    def log_message(self, fmt, *args):  # quiet: the terminal is the PROMPT_ID channel
        pass

    def _host_ok(self) -> bool:
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("127.0.0.1", "localhost")

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        if not self._host_ok():
            return self._json(403, {"error": "host not allowed"})
        url = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(url.query)
        if url.path in ("/", "/index.html"):
            return self._send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")
        if url.path == "/api/state":
            return self._json(200, {
                "user": os.environ.get("TRACETRACK_USER", getpass.getuser()),
                "workdir": str(self.store.workdir),
                "executors": list(EXECUTORS),
                "deepseek_ready": bool(os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("TRACETRACK_CMD_DEEPSEEK")),
                "sms_ready": all(os.environ.get(k) for k in
                                 ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM", "TRACETRACK_SMS_TO")),
            })
        if url.path == "/api/sessions":
            return self._json(200, discover_sessions())
        if url.path == "/api/session":
            sid = (q.get("id") or [""])[0]
            match = next((s for s in discover_sessions(limit=400) if s["id"] == sid), None)
            if match is None:
                return self._json(404, {"error": "unknown session"})
            return self._json(200, {**match, **summarize_session(Path(match["path"]), self.repos)})
        if url.path == "/api/jobs":
            return self._json(200, self.store.list())
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        if not self._host_ok():
            return self._json(403, {"error": "host not allowed"})
        origin = self.headers.get("Origin")
        if origin and urllib.parse.urlparse(origin).hostname not in ("127.0.0.1", "localhost"):
            return self._json(403, {"error": "origin not allowed"})
        if not (self.headers.get("Content-Type") or "").startswith("application/json"):
            return self._json(415, {"error": "JSON body required"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        except json.JSONDecodeError:
            return self._json(400, {"error": "invalid JSON"})
        parts = urllib.parse.urlparse(self.path).path.strip("/").split("/")
        try:
            if parts == ["api", "jobs"]:
                job = self.store.create(str(body.get("executor", "")), str(body.get("prompt", "")))
                return self._json(201, job.public())
            if len(parts) == 4 and parts[:2] == ["api", "jobs"] and parts[3] == "authorize":
                job = self.store.authorize(parts[2], str(body.get("prompt_id", "")))
                return self._json(200, job.public())
        except KeyError:
            return self._json(404, {"error": "unknown job"})
        except ValueError as exc:
            return self._json(400, {"error": str(exc)})
        return self._json(404, {"error": "not found"})


def make_server(port: int, workdir: Path, repos: list[Path], state_dir: Path | None = None) -> ThreadingHTTPServer:
    handler = type("BoundHandler", (Handler,), {"store": JobStore(workdir, repos, state_dir), "repos": repos})
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def serve(port: int, workdir: Path, repos: list[Path]) -> int:
    httpd = make_server(port, workdir, repos)
    print(f"TraceTrack on http://127.0.0.1:{port}  (workdir {workdir}) — Ctrl+C to stop", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0
