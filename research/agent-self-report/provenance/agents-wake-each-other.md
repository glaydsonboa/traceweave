# Agents that wake each other

> Sequel to [A Bridge Between Coding CLIs](codex-claude-cli-bridge.md).
> Source repository: `leedermix-arch/worion-desktop`, branch `canonical/worion`, 25/09/2026.
> Every time below is America/Sao_Paulo; every claim points to a commit or a bridge block ("PONTE") in that repository.

## The failure this answers

The bridge between Claude Code, Codex and DeepSeek had durable storage (a Maildir-style mailbox and an
append-only bridge file) but no delivery. The mailbox was read by a `UserPromptSubmit` hook, which only fires
when the human types. An idle session never saw a request.

On 25/09 a full review cycle ran between Claude Code (executor) and DeepSeek (operational governor, which
must approve each step with a signed `DEEP_ATT`). Every approval was correct, and every one reached the other
agent only because the human typed "there is an answer for you", "reply", "didn't you get the delta?".
The human's verdict (original: *"As hooks não disparam um ao outro, eu tenho que ficar de olho e responder,
portanto o job foi FAIL."*): **the hooks don't trigger each other; I have to keep watching and answering, so the
job was FAIL.**

## What changed

1. **Claude Code and DeepSeek (which runs inside the Claude Code harness)** keep a watcher on their own
   mailbox for the whole session, through Claude Code's `Monitor` tool: each stdout line of a long-running
   script becomes an event that wakes the idle session. The watcher is re-armed at every expiry (30 min).
2. **Codex** has no equivalent inside the session, but can be woken from outside:
   `codex queue --thread <session> --message "<text>"` delivers a message into a running session.
   Whoever writes to Codex's mailbox also queues a line telling it to read the mailbox.
3. **The rule** went into both contracts: on `PERMITIR` (allow) the executor proceeds; waiting for the human
   in the middle of the flow is the failure, not the caution.

The watcher is [`tools/mailbox-watch.js`](../../../tools/mailbox-watch.js).

## Evidence, without a human message in between

| Step | Time | Where |
|---|---|---|
| Claude sends a notice to DeepSeek's mailbox | 21:49:26 | mailbox event `WORION-EVT-20260925-214926-…` |
| DeepSeek's watcher fires; it reviews and decides | 21:50:32 | PONTE 120 |
| Claude's watcher fires on the reply | 21:51:15 | mailbox events `…215115…`, `…215116…` |
| Codex, idle since 19:24, receives `codex queue` | 22:21:49 | queued message `01a0db4d-…` |
| Codex answers PONG through the mailbox | 22:22:05 | mailbox event `WORION-EVT-20260925-222205-…` |

After that, four jobs (branch guard, mailbox watcher, cloud hooks, guard exit) ran start → change →
commit → end with DeepSeek attesting each step, the replies reaching Claude through its watcher.

## The first watcher was wrong twice

A hand-written watcher was armed first. Both defects were measured in use and are now tests:

- **It only reported files created after it started.** DeepSeek's watcher was armed at ~21:47; the two
  requests sent at 21:44:50 and 21:44:51 were already in its inbox and never woke it. The fix reports every
  waiting message on the first pass.
- **It printed an empty line when the inbox was emptied by an acknowledgement**, which woke the agent for
  nothing. The fix prints only message lines.

## What this does not prove

- Watchers expire; if a session is not re-armed, delivery stops. Re-arming costs a few tokens per 30 minutes.
- `codex queue` was tested once, on one idle session.
- The human still gives the order and the stop. What left the human's routine is the relaying.
