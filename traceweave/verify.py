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

    return result
