# Repository hooks in cloud sessions

Hooks committed in `.claude/settings.json` also run when the repository is opened in a Claude Code cloud
session. Hooks that write local records (transcripts, session summaries) then write into the cloud container.

## The deadlock (25/09/2026)

In a cloud session the transcript and summary hooks created two untracked files under `records/`. The cloud
environment's own stop hook requires every untracked file to be committed and pushed. The repository's branch
guard forbids any write outside the canonical branch, and the cloud session was on a generated `claude/*`
branch. One hook demanded a commit, the other forbade it, at every turn.

## The rule

Local-record hooks exit without writing when `CLAUDE_CODE_REMOTE=true` (set in cloud sessions, absent in the
local CLI, per the Claude Code documentation). What the cloud session produces is recovered locally anyway:
`claude --teleport <session>` brings the conversation into a local JSONL, from which the transcript is generated.

## Evidence

Source repository `leedermix-arch/worion-desktop`: commit `d7bc23a4`. Tests run each hook with and without the
variable: with it, nothing is written; without it, the same input writes the record. Mutations that ignore the
variable fail both tests.
