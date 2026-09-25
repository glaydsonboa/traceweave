"""Checkpoint verification for Traceweave protocol version 0.1.

Verification is purely structural: it checks that the checkpoint contains the
facts it claims and that claims do not contradict each other. It never touches
Git, the network, or the repository — a checkpoint file alone is verified.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import TRACEWEAVE_VERSION


@dataclass
class VerificationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _error(result: VerificationResult, message: str) -> None:
    result.errors.append(message)


def verify(checkpoint: dict) -> VerificationResult:
    result = VerificationResult()

    if not isinstance(checkpoint, dict):
        _error(result, "checkpoint is not a JSON object")
        return result

    version = checkpoint.get("traceweave_version")
    if version != TRACEWEAVE_VERSION:
        _error(result, f"traceweave_version must be {TRACEWEAVE_VERSION!r}, got {version!r}")

    # Checkpoint status is normative in SPEC.md §9.
    checkpoint_status = checkpoint.get("status")
    allowed_checkpoint_statuses = {"complete", "partial", "blocked"}
    if checkpoint_status not in allowed_checkpoint_statuses:
        _error(
            result,
            f"status must be one of {sorted(allowed_checkpoint_statuses)}, got {checkpoint_status!r}",
        )

    # 1. session_id exists
    session = checkpoint.get("session")
    session_id = session.get("session_id") if isinstance(session, dict) else None
    if not session_id or not isinstance(session_id, str):
        _error(result, "session.session_id missing or not a string")

    # 1b. session.executor exists — SPEC.md §2 lists executor as required.
    executor = session.get("executor") if isinstance(session, dict) else None
    if not executor or not isinstance(executor, str):
        _error(result, "session.executor missing or not a string")

    # 2. checkpoint_id exists
    checkpoint_id = checkpoint.get("checkpoint_id")
    if not checkpoint_id or not isinstance(checkpoint_id, str):
        _error(result, "checkpoint_id missing or not a string")

    # 3. base_commit exists
    git = checkpoint.get("git")
    if not isinstance(git, dict):
        _error(result, "git block missing")
    else:
        base_commit = git.get("base_commit")
        if not base_commit or not isinstance(base_commit, str):
            _error(result, "git.base_commit missing or not a string")

        # 4. head_commit exists
        head_commit = git.get("head_commit")
        if not head_commit or not isinstance(head_commit, str):
            _error(result, "git.head_commit missing or not a string")

    # 5. every test entry has an explicit result
    allowed_results = {"passed", "failed", "not_run"}
    tests = checkpoint.get("tests", [])
    if not isinstance(tests, list):
        _error(result, "tests must be a list")
    else:
        for index, entry in enumerate(tests):
            if not isinstance(entry, dict):
                _error(result, f"tests[{index}] is not an object")
                continue
            if entry.get("result") not in allowed_results:
                _error(result, f"tests[{index}].result must be one of {sorted(allowed_results)}")

    # 6. provenance links are explicit values or null
    provenance = checkpoint.get("provenance")
    if not isinstance(provenance, dict):
        _error(result, "provenance block missing")
    else:
        for key in ("requested_by", "prompt_generator", "executor"):
            value = provenance.get(key)
            if value is None:
                continue
            if not isinstance(value, dict):
                _error(result, f"provenance.{key} must be an object or null")
                continue
            if "name" not in value or "type" not in value:
                _error(result, f"provenance.{key} must have explicit 'name' and 'type' fields")

    # 7. graph_sync consistency
    graph_sync = checkpoint.get("graph_sync")
    if not isinstance(graph_sync, dict):
        _error(result, "graph_sync block missing")
    else:
        status = graph_sync.get("status")
        allowed_statuses = {"synced", "stale", "not_applicable", "unknown"}
        if status not in allowed_statuses:
            _error(result, f"graph_sync.status must be one of {sorted(allowed_statuses)}")
        if status == "synced":
            if isinstance(git, dict):
                head_commit = git.get("head_commit")
                source_commit = graph_sync.get("source_commit")
                if head_commit != source_commit:
                    _error(result, (
                        "graph_sync.status is 'synced' but graph_sync.source_commit "
                        f"({source_commit!r}) does not match git.head_commit ({head_commit!r})"
                    ))

    # 8. SPEC.md §10 rule 7 — no unsupported claim is promoted to fact. SPEC.md §9 defines
    # "complete" as "contains the evidence required by the current session boundary". A
    # checkpoint that claims "complete" must therefore carry that evidence: every test entry
    # has a result other than not_run and a non-empty evidence, and the working tree is clean.
    if checkpoint_status == "complete":
        if isinstance(tests, list):
            if not tests:
                _error(result, "status 'complete' requires at least one test entry with evidence (SPEC.md §10 rule 7)")
            for index, entry in enumerate(tests):
                if not isinstance(entry, dict):
                    continue
                if entry.get("result") == "not_run":
                    _error(result, f"status 'complete' but tests[{index}].result is 'not_run' (SPEC.md §10 rule 7)")
                if not entry.get("evidence"):
                    _error(result, f"status 'complete' but tests[{index}] has no evidence (SPEC.md §10 rule 7)")
        if isinstance(git, dict) and git.get("working_tree") != "clean":
            _error(result, "status 'complete' but git.working_tree is not 'clean' (SPEC.md §10 rule 7)")

    return result


def verify_against_repo(checkpoint: dict, repo) -> VerificationResult:
    """Check the checkpoint's Git claims against a real repository (opt-in).

    verify() is purely structural and never touches Git. This function is the other half: it
    catches claims that were false at the moment of recording, which a hash chain would only
    seal — a head_commit that does not exist, a base_commit that is not an ancestor of it, or
    a working_tree state that contradicts the repository when head_commit is the current HEAD.
    """
    import subprocess
    from pathlib import Path

    result = VerificationResult()
    git = checkpoint.get("git") if isinstance(checkpoint, dict) else None
    if not isinstance(git, dict):
        _error(result, "git block missing")
        return result
    root = str(Path(repo))

    def run(*args):
        return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)

    def exists(sha):
        return isinstance(sha, str) and sha and not sha.startswith("-") and             run("cat-file", "-e", "--end-of-options", f"{sha}^{{commit}}").returncode == 0

    head, base = git.get("head_commit"), git.get("base_commit")
    if not exists(head):
        _error(result, f"git.head_commit {head!r} does not exist in {root}")
    if not exists(base):
        _error(result, f"git.base_commit {base!r} does not exist in {root}")
    if exists(head) and exists(base) and run("merge-base", "--is-ancestor", base, head).returncode != 0:
        _error(result, f"git.base_commit {base!r} is not an ancestor of git.head_commit {head!r}")
    current = run("rev-parse", "HEAD").stdout.strip()
    if exists(head) and current == head:
        # Ignore .traceweave/ — the checkpoint writes there itself, as git_state.collect does.
        dirty = bool(run("status", "--porcelain", "--", ".", ":(exclude).traceweave").stdout.strip())
        actual = "dirty" if dirty else "clean"
        claimed = git.get("working_tree")
        if claimed in ("clean", "dirty") and claimed != actual:
            _error(result, f"git.working_tree claims {claimed!r} but the repository at HEAD is {actual!r}")
    return result
