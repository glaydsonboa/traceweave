"""Traceweave CLI — version 0.1.

Commands:

- ``traceweave checkpoint`` — inspect the current Git repository and write a
  checkpoint JSON to ``.traceweave/checkpoints/<checkpoint_id>.json``.
- ``traceweave verify <checkpoint.json>`` — verify a checkpoint against the
  protocol rules. Exits non-zero when verification fails.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .checkpoint import (
    CheckpointOptions,
    SessionStore,
    build_checkpoint,
    load_checkpoint,
    write_checkpoint,
)
from .git_state import GitError, collect
from .verify import verify

ALLOWED_GRAPH_STATUSES = ("not_applicable", "unknown")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="traceweave",
        description="Verifiable continuity and provenance for AI coding sessions.",
    )
    parser.add_argument("--version", action="version", version=f"traceweave {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    checkpoint = subparsers.add_parser(
        "checkpoint", help="inspect the current Git repository and write a checkpoint"
    )
    checkpoint.add_argument("--summary", help="one-line summary of the work performed")
    checkpoint.add_argument(
        "--executor",
        required=True,
        help="human, CLI, agent or model that performed the work (SPEC.md: required)",
    )
    checkpoint.add_argument("--requested-by", help="who or what requested the work")
    checkpoint.add_argument("--prompt-generator", help="who or what generated the instruction")
    checkpoint.add_argument("--session-id", help="stable session identifier; default: auto-created and persisted")
    checkpoint.add_argument("--base-commit", help="commit from which the session started; default: session base or current HEAD")
    checkpoint.add_argument(
        "--graph-status",
        choices=ALLOWED_GRAPH_STATUSES,
        default="unknown",
        help="graph synchronization status; default unknown (version 0.1 supports not_applicable and unknown)",
    )
    checkpoint.add_argument(
        "--path",
        type=Path,
        default=None,
        help="repository path to inspect; default: current directory",
    )

    verify_parser = subparsers.add_parser("verify", help="verify a checkpoint JSON file")
    verify_parser.add_argument("checkpoint_file", type=Path, help="path to the checkpoint JSON")

    return parser


def _checkpoint(args: argparse.Namespace) -> int:
    try:
        root = None
        if args.path is not None:
            root = args.path
        from .git_state import repo_root_from
        root = repo_root_from(root)
        git = collect(root)
    except GitError as exc:
        print(f"traceweave: error: {exc}", file=sys.stderr)
        return 1

    # A checkpoint without a resolvable HEAD or branch would record a Git state
    # that does not exist. Fail clearly instead of writing an invalid checkpoint.
    if git.head_commit is None:
        print(
            "traceweave: error: repository has no HEAD commit "
            "(empty repository or unborn branch); cannot checkpoint",
            file=sys.stderr,
        )
        return 1
    if git.branch is None:
        print(
            "traceweave: error: repository is in detached HEAD state; "
            "cannot checkpoint without a branch",
            file=sys.stderr,
        )
        return 1

    opts = CheckpointOptions(
        summary=args.summary,
        executor=args.executor,
        requested_by=args.requested_by,
        prompt_generator=args.prompt_generator,
        session_id=args.session_id,
        base_commit=args.base_commit,
        graph_status=args.graph_status,
    )

    store = SessionStore(root)
    session = store.get_or_create(opts, git)
    checkpoint = build_checkpoint(opts, git, session)
    store.save(session)
    out_path = write_checkpoint(checkpoint, root)
    print(out_path)
    return 0


def _verify(args: argparse.Namespace) -> int:
    try:
        checkpoint = load_checkpoint(args.checkpoint_file)
    except (OSError, ValueError) as exc:
        print(f"traceweave: error: cannot read {args.checkpoint_file}: {exc}", file=sys.stderr)
        return 2

    result = verify(checkpoint)
    if result.ok:
        print(f"{args.checkpoint_file}: verification passed")
        return 0
    for error in result.errors:
        print(f"traceweave: error: {error}", file=sys.stderr)
    print(f"{args.checkpoint_file}: verification FAILED ({len(result.errors)} error(s))", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "checkpoint":
        return _checkpoint(args)
    if args.command == "verify":
        return _verify(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
