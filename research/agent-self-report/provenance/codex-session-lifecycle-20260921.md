# Codex session lifecycle provenance — STOP / RESUME / remote readback

This note is a public provenance bridge from a private engineering case. It records only the evidence needed to reconstruct the lifecycle work performed by Codex on 21 September 2026. It does not publish passwords, tokens, `.env` values, private transcript contents, or private repository source code.

The underlying software project is context. The research object is the separation between **narrated state, observed state, and executed state** in an AI-assisted engineering workflow.

## Source anchors

Primary Codex session:

```text
session_id:
01a0c1d6-95f3-7470-9e3a-0c96331b06c2
```

The session exists in two preserved forms supplied for this research pass:

```text
derived Markdown transcript SHA-256:
0135732f9255ebd568c0fd546c984b216b1c7d755996bb2131af10e29e5193b7

native Codex rollout JSONL SHA-256:
50a74f0ccd0c41d776c2e2913b395a302178d7dda1eb1e055caf89c2745fd1a3

supporting full CLI capture SHA-256:
f11f53edccd49f22c5e809f67c145a278d89f00e6ae9e19f3521ba638f0e654a
```

The raw JSONL is not published in this commit. These hashes are chronology and integrity anchors for a later source bundle.

## Prompt identity was observed before mutation

The native session record preserves an observed invocation of the repository's canonical prompt-ID generator before the first patch in the migration cause.

```text
PROMPT_ID:
WORION-PROMPT-20260921-001351-migracao-governanca-v2-proveniencia-life
```

The important claim is not that this string exists. The important claim is that the generator invocation and returned value are present in the native execution record before mutation.

That distinction follows the evidence rule:

```text
reported ID != observed generation event
```

## What was implemented and independently anchored in Git

The private engineering repository preserves the following commits. The references below are included as provenance anchors; the private source code itself is not reproduced here.

| Commit | Material fact |
|---|---|
| `8cefd8a14fbae3bb82fcd7407ae80c4701dce8d3` | Preserve textual Claude thinking blocks in the derived Markdown transcript when the native source exposes them |
| `721b99cafa6a9a087470c619fa46d0d09ccd7763` | Resolve the canonical transcript root outside a Git worktree |
| `942811ef24779c7e0384575b3dc5e9a12ec019d7` | Preserve a concurrent remote commit while integrating the transcript-root correction |
| `79ec14d27831f687f8a433aedc711ed0e7e2d3ae` | Add verified STOP evidence, append-only RESUME recording and related tests/bindings |
| `6ad72b25eb537102344579c023acb3f024e3b543` | Record runtime proof for the hourly RESUME path |
| `6357238233d2a1c0be6dac6b57faa1b3b907cf14` | Add official Claude hook semantics to the engineering evidence note |
| `f2910d9f1e6fa9c907c18267df21cda92bbf15e5` | Adopt the V2 governance contracts while preserving previous rules as historical/superseded |
| `ef0d4470a568ba8820d901409ca5a02b3de2f77b` | Manual deterministic STOP closure for the Codex session, including transcript, derived report and handoff |

Each of the commits above was re-read through the GitHub repository interface during preparation of this public note.

## Failure that exposed the transcript-root problem

The project used a separate Git worktree for the active canonical branch while transcript files were stored under the main repository root.

Conceptually:

```text
active worktree
  <private-root>/.worktrees/canonical

canonical transcript store
  <private-root>/records/transcripts/
```

The earlier STOP path looked for the transcript under the worktree itself. The transcript existed, but in the external canonical transcript root, so STOP classified the session as `PARTIAL` with a missing/pending transcript.

The correction introduced a root resolver used by the transcript archive and finalizers. The evidence value of this failure is methodological: a file can exist while an observer aimed at the wrong root reports it as absent.

```text
absence in the observed path != absence of the artifact
```

## Lifecycle implemented by the deterministic path

The resulting closure design is:

```text
exact "stop" command
        ↓
UserPromptSubmit hook marks SESSION_ID
        ↓
Stop event
        ↓
locate canonical transcript root
        ↓
update primary transcript
        ↓
preserve native source when applicable
        ↓
stage byte-identical evidence copy
        ↓
derive report + handoff
        ↓
commit
        ↓
push
        ↓
remote HEAD readback
        ↓
remote blob/hash readback
```

The finalizer does not promote a local commit to published state merely because `git commit` succeeded. Remote readback is a separate evidence step.

## Claude-side dual source preservation

The same engineering line created two complementary Claude artifacts:

```text
native JSONL
  = primary provenance source for the CLI record

derived Markdown
  = readable projection
```

When the native JSONL exposes textual `thinking` blocks, the derived Markdown keeps those text blocks in native order. Structured `tool_use` / `tool_result` payloads and redacted/encrypted thinking are not promoted into the readable projection.

The native JSONL remains a separate source and is not treated as byte-equivalent to the Markdown.

A previous commit also implemented byte-for-byte preservation of Claude's native JSONL at STOP with SHA-256 linkage and remote receipt:

```text
3f81d0b3eff9403a66bd3582b80ad053e1fb95ab
```

A later commit staged an independent post-hook evidence mirror:

```text
406ec2243db7ef5686ee9af5e68b8325c36fdc93
```

Those two mechanisms are relevant because a readable transcript and the native execution record answer different provenance questions.

## RESUME as an append-only factual checkpoint

The implemented RESUME path records four sections:

```text
Feito
Em andamento
Pendente ou bloqueado
Próximo passo exato
```

The hourly runner uses the same producer and appends to the same session file rather than rewriting previous blocks.

Observed runtime evidence from the Codex session records:

```text
scheduled task:
Worion-Hourly-Checkpoint

interval:
PT1H

manual task run result:
0

resume file SHA-256 after an immediate second run:
155C4EE97AAECA376143D2A8E07EDD9ED31CAC08B283EEA370646CACD6DADBAF

second result:
not_due

hash changed:
no
```

The recorded test battery reports 33/33 passing STOP/transcript tests plus the specific RESUME test.

## Manual STOP closure that reached remote readback

The strongest executed result in this session is the deterministic manual invocation of the same STOP finalizer path.

The finalizer produced:

```text
commit:
ef0d4470a568ba8820d901409ca5a02b3de2f77b

branch:
canonical/worion

artifacts:
- session transcript
- derived STOP report
- HANDOFF_VIGENTE.md
```

The source transcript and the copy stored in Git were reported with the same SHA-256:

```text
b4ddbc84df4f6560739e5d97c80db8ad2d9bbbcfbd9c09d29d073e9db3dc7d9c
```

Git push and remote readback returned the same commit SHA.

This supports the narrower statement:

> The deterministic STOP finalizer path produced a transcript, derived report and handoff, committed them, pushed the commit and read the same revision back from the remote repository.

## Evidence layers

### NARRATED

The agent described an intended lifecycle in which STOP preserves the session and publishes the closure artifacts.

### OBSERVED

The record contains:

- the prompt-ID generator invocation and output;
- source and transcript paths;
- SHA-256 comparisons;
- test results;
- scheduled-task result;
- Git commit identifiers;
- push results;
- remote readbacks;
- GitHub commit objects for the referenced revisions.

### EXECUTED

The manual finalizer path reached:

```text
transcript
→ derived report
→ handoff
→ commit
→ push
→ remote readback
```

The automatic harness-triggered closure was not promoted to `COMPLETE` when its own evidence remained insufficient. The session continued to label those attempts `PARTIAL`.

That distinction is part of the result, not an inconvenience to hide:

```text
working code path
!=
proof that every active hook binding executed that path
```

## Official mechanism references preserved in the engineering record

The private engineering note cites the official hook mechanisms used by the implementation:

- OpenAI Codex hooks: <https://developers.openai.com/pt-BR/docs/hooks>
- OpenAI Codex advanced configuration: <https://developers.openai.com/pt-BR/docs/config-file/config-advanced>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks>
- Claude Code settings: <https://code.claude.com/docs/en/settings>
- Claude Code hooks guide: <https://code.claude.com/docs/en/hooks-guide>

Those references establish that local lifecycle hooks are supported mechanisms. They do not prove that a particular local binding ran; that requires the local transcript, effects, Git state and readback described above.

## Why this matters to Traceweave

This case demonstrates several protocol-level distinctions:

```text
source artifact != readable projection

commit != push

push != remote readback

configured hook != executed hook

reported ID != observed ID generation

reported completion != evidenced completion

Git author identity != real executor
```

The engineering process therefore converged on a stronger continuity rule:

> A session boundary is not a narrative event. It is a chain of independently inspectable artifacts whose relationships can be rechecked later.

## Publication boundary

This commit publishes the provenance index, not the private source corpus.

No password, access token, Supabase value, `.env` content, or private transcript body is included here.

The preserved raw sources can be compared against the hashes above when a source bundle is released separately.
