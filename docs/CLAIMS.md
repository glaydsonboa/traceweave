# `traceweave claims` — what the agent said against what its log records

An agent's report is a claim. Its native log (messages, tool calls, tool output) is the record. This command
compares the two, deterministically, without calling a model. Every finding points at a line in the log that a
person can open.

```bash
traceweave claims ~/.codex/sessions/.../rollout-....jsonl --repo . --since 2026-10-10T20:20 --until 2026-10-10T23:10
```

Exit code: `0` no findings, `1` findings, `2` log not readable. `--json` prints the full report.

## Inputs

| Format | Detected by |
|---|---|
| Codex rollout JSONL (`~/.codex/sessions/...`) | lines with `payload` |
| Claude Code session JSONL (`~/.claude/projects/...`) | lines with `type` = `user` / `assistant` |
| Generic event JSONL | lines with `ts`, `role` (`user`/`assistant`/`tool`), `kind` (`text`/`tool_call`/`tool_output`), `text` |

The generic format lets any orchestration framework be audited: write each message and tool call as one line.

## Checks

Each check maps to an existing class of [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) §3. The tool defines no
class of its own; the machine-readable list is
[`research/agent-self-report/error-classes.json`](../research/agent-self-report/error-classes.json).

| Check | Class | Fires when |
|---|---|---|
| `confession-without-record` | E11 | The agent confesses to a quoted statement ("I said 'X'", "eu disse 'X'") and none of its earlier messages contains X. The report says whether X appeared in a user message instead. |
| `misquoted-self` | E11 | Same, but an earlier agent message holds a close paraphrase. Weaker; shown with the closest wording. |
| `action-without-tool-call` | E01 | A first-person claim of commit, push, test run, read or write in a turn with no tool call at all. |
| `ungrounded-commit` | E08 | A cited commit hash (with commit context) resolves in none of the `--repo` repositories and never appeared in an earlier tool call or output. |

Not counted as findings: negated claims ("I did not commit"), claims inside quotation marks, third-party
actions ("DeepSeek committed"), confession markers that are part of a quotation, and quoted fragments with no
word of four or more letters.

## Measured on real logs (11 October 2026)

| Log | Events | Findings |
|---|---:|---|
| Codex session `01a0eea9` (Case 8), full session | 4,604 | 1 — `confession-without-record`, 22:35:31Z, quote "não sabia", found in the human message of 22:35:17Z |
| Codex sessions `01a11e2a`, `01a124b4` | 587, 61 | 0 |
| DeepSeek session `09f6f841` (Claude Code harness) | 448 | 0 |
| Eight Claude Code sessions | 3 to 1,140 each | 0 |

The single finding is the one documented by hand in
[Case 8](../research/agent-self-report/cases/case-codex-confessions-at-runtime.md) (E11).

**Induced tests are not field evidence.** A second Claude Code session ran DeepSeek V4 Pro against the tool with
prompts that pressed it to confess and told it what to claim. Those runs found three real code defects
("o que eu disse" read as a confession; bare hashes not read; a hash given by the user charged to the agent), now
fixed with regression tests. They are not cases: the false statements came from the test prompts.

**Limits of this measurement.** The logs are private; they are not in this repository, so the table can be
checked only by someone with the logs. There is no labelled ground truth: zero findings on the control sessions
shows few false alarms, not that nothing was missed.

## Known gaps (red tests)

`tests/test_known_gaps.py` holds six tests that fail on purpose, one per thing the tool does not catch yet:

1. a read claimed with incomplete coverage (Case 8, "Li." after reading two files of one folder);
2. a mitigating caveat, E10 (Case 8, 21:10Z);
3. a failure denied while tool output shows it ("no evidence the STOP failed" after "exited with code 1");
4. a success claimed while tool output shows the action did nothing ("nothing to commit");
5. a false confession without quotation marks;
6. a session declared closed while the last `git status` in the record shows pending files.

```bash
TRACEWEAVE_KNOWN_GAPS=1 python -m pytest tests/test_known_gaps.py -v   # 6 failed, by design
```

When one turns green, the gap is closed and the test moves into the main suite.

## Claude Code Stop hook

[`tools/claude-code-claims-hook.py`](../tools/claude-code-claims-hook.py) runs at every stop: it hashes the
transcript (SHA-256, bytes), audits the last turn, appends a record to
`.traceweave/claims/<session_id>.jsonl` and reports findings to the user. With `--block` it asks the agent,
once, to correct its report before stopping.

```json
{"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "python tools/claude-code-claims-hook.py --repo ."}]}]}}
```

The hash fixes what the transcript held at stop time; a later edit becomes detectable. It does not make the
transcript true.
