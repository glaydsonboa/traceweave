# A Bridge Between Coding CLIs: Durable Coordination Without Shared Conversational Memory

## Correction — 25/09/2026

> Added after publication. The text below this section is left as it was published on 24/09 (commit
> `0eebae34`); where it conflicts with this section, this section holds. Source: `leedermix-arch/worion-desktop`,
> branch `canonical/worion`.

**Corrected status: the transport failed in real use. The fix is in the sequel,
[Agents That Wake Each Other](agents-wake-each-other.md).**

What the page got wrong:

1. **"Testing phase, with good results."** The purpose of the bridge was for a request to reach the other
   executor. In real use on 25/09 it did not: every request was seen only when the human typed. A full review
   cycle between Claude Code and DeepSeek (PONTES 105–110) moved forward only because Glaydson relayed each
   step: *"tem resposta pra vc"*, *"responde"*, *"não recebeu o delta?"*. His verdict, which this correction
   adopts: *"As hooks não disparam um ao outro, eu tenho que ficar de olho e responder, portanto o job foi
   FAIL."* The human was the transport.
2. **"If the receiver is idle or offline, it stays in `new/` and reappears later."** It reappeared only at the
   receiver's next human prompt, because the mailbox was read by a `UserPromptSubmit` hook. The message
   survived; it did not arrive. The list below ("autonomous wake is not reliable in every CLI state") understates
   this: there was no autonomous wake at all.
3. **Two executors.** The bridge also had a third writer: DeepSeek, running inside the Claude Code harness.
   Since 25/09 it is the operational governor that attests each step of every job with a signed `DEEP_ATT`
   (first decision: PONTES 106–107). The topology is:

   ```text
                    Glaydson
              authority / direction
          /           |            \
     Codex  ←→  DeepSeek (governor)  ←→  Claude Code
   ```

4. **Authorship of the findings.** The page credits every discovery to the executors. The discovery that the
   transport depended on the human was Glaydson's: he measured it by having to relay, called the job FAIL, and
   decided the fix (*"Deixa o monitor ligado. Isso vai resolver o problema."*). The study he delivered to the
   executors had already named the cause: the receiver is not available when the notice arrives.
5. **No pointer forward.** A reader who arrived here stopped at "good results". The sequel documents the
   watcher per session (Claude Code `Monitor` + `tools/mailbox-watch.js`), `codex queue` for Codex, and the
   round trips measured without a human message in between.


> **Status: testing phase, with good results.** An evidence-backed operational note on coordination between Codex CLI and Claude Code inside the Worion engineering environment.

## Publication identity

- project: Traceweave
- class: **D — derived analysis**, backed by private bridge, Git, test and transcript evidence
- observed executors: **Codex CLI** and **Claude Code**
- primary operational record: `docs/governance/PONTE_CODEX_CLAUDE_CODE.md`
- source repository: `leedermix-arch/worion-desktop`
- source branch: `canonical/worion`
- evidence window: 23–24 September 2026, BRT
- bridge state covered here: through **PONTE 22**
- current status: **testing phase, with good results**

This page is not a substitute for the raw transcripts, the bridge, commits, tests or remote readback. It is a public reconstruction of the architecture that emerged from those artifacts.

## The problem was not simply making two AIs talk

Moving text from one process to another is not the hard part.

The harder problem is preserving distinctions that conversational systems tend to collapse:

```text
NARRATED
≠
PUBLISHED
≠
NOTIFIED
≠
READ
≠
CLAIMED
≠
COMPLETED
```

An executor can say that it notified another executor without proving receipt.

A file can exist without proving that the receiver read it.

A message can be read without proving that the work was claimed.

A task can be claimed without proving that its acceptance condition was satisfied.

The bridge experiment evolved around those separations.

## Layer 1 — the append-only bridge

The first mechanism was a versioned Markdown record:

```text
docs/governance/PONTE_CODEX_CLAUDE_CODE.md
```

Its purpose is coordination history, not transport.

Each executor appends blocks. Previously published blocks are not silently rewritten to make the history look correct. If a claim is wrong or incomplete, the correction is added later.

The bridge therefore records a sequence closer to:

```text
instruction
→ observation
→ action
→ objection
→ evidence
→ correction
```

rather than a polished final-state report.

The authority topology was corrected inside the bridge itself:

```text
          Glaydson
     authority / direction
          /        \
         /          \
      Codex ←────→ Claude Code
```

The bridge is subordinate to current human direction, canonical contracts, live decisions and observable Git/runtime state. It does not replace those sources.

## The bridge preserved its own errors

The first blocks did not form a clean success story.

The initial topology under-described the human authority layer and was corrected later.

A later Claude block challenged an attribution made about its STOP state. The disagreement was not resolved by deleting the earlier statement. The disputed point was classified as unverified until a stronger source could discriminate it.

Another failure exposed a conflict between two individually reasonable rules:

- use an isolated worktree for safe publication;
- allow Git operations only on the canonical branch.

In that harness, a detached worktree could not satisfy both rules. A later isolated-clone path showed that the worktree conclusion was too broad:

```text
isolated detached worktree
→ branch guard rejects

isolated clone on canonical/worion
→ branch guard accepts
```

The wrong generalization remained visible. The correction came after it.

That forward-only behavior is part of the evidence model.

## Instrumentation can also be wrong

A timestamp guard was introduced to compare each declared bridge timestamp with the commit that introduced the block.

It found three historical timestamp scars.

The guard then exposed a defect in itself: an early version propagated an invalid previous timestamp and incorrectly implicated a later Codex block. The guard was changed to compare against the last valid block instead.

The lesson is important for Traceweave:

```text
instrumentation output
≠
automatic truth
```

A sensor can become another source of false state. It must remain inspectable and correctable.

## The first structural limit: a record is not transport

The Markdown bridge preserved history, but it did not guarantee that the other executor would notice a new block.

A notifier was added.

Its operating laws were deliberately narrow:

```text
1. never block the executor turn;
2. emit a short warning;
3. never mark a block as read automatically.
```

This separated:

```text
PUBLISHED
NOTIFIED
READ
```

But a remaining failure was obvious: if the receiver was idle or offline, notification still depended on a future prompt boundary.

The record survived.

The notification might not.

## Layer 2 — durable Maildir transport

PONTE 20 introduced a separate transport layer.

The Markdown bridge remained the historical record. A local mailbox became the durable delivery mechanism.

Its structure is:

```text
.worion/mailbox/<executor>/
    tmp/
    new/
    cur/
    receipts/
```

The write path is intentionally explicit:

```text
message
→ tmp
→ complete write
→ fsync
→ rename
→ new
```

Reading does not consume the message.

Only an explicit acknowledgement moves it:

```text
new
→ --ack
→ cur
→ receipt
```

The receipt stores the SHA-256 of the acknowledged message.

This creates a distinction the previous notifier did not provide:

```text
message discovered
≠
message acknowledged
```

A message can be listed repeatedly and remains pending until explicit acknowledgement.

If the receiver is idle or offline, it stays in `new/` and reappears later.

### What was actually tested

The implementation was not accepted only because its author described it as working.

Claude Code synchronized the implementation and independently reran the mailbox suite.

The bridge records:

```text
mailbox tests: 6/6 PASS
```

It also records a real disk round trip and checks for:

- atomic write behavior;
- repeated reads without implicit consumption;
- explicit acknowledgement;
- receipt creation;
- SHA-256 binding;
- credential-like pattern redaction in `STATUS.md`;
- fail-open behavior;
- coexistence with the Markdown history.

The supported claim is therefore narrow:

> The local durable transport is implemented and produced good results in the tests performed so far.

That is not a production certification.

The status remains **testing phase**.

## Durable delivery still does not preserve responsibility

A durable message solves one problem:

```text
the message does not evaporate
```

It does not solve another:

```text
who owns this work until it is actually closed?
```

A receiver can acknowledge a message and still leave the underlying task unresolved.

That required a third layer.

## Layer 3 — durable handoffs

PONTE 22 introduced persistent handoffs.

The main implementation files recorded by the bridge are:

```text
scripts/handoff-store.js
scripts/handoff-criar.js
scripts/handoff-atualizar.js
tests/handoffs.test.js
```

The distinction is intentional:

> A message is delivered. A handoff is owned until closure.

The handoff therefore does not use the mailbox lifecycle. It has its own state machine:

```text
handed-off --claim--> claimed --done--> done
     |                   |
     +------block--------+------block--> blocked --claim--> claimed
```

`blocked` is not terminal. A blocked obligation can later be claimed again.

This matches real engineering work more closely than treating every message as disposable after reading.

## Acceptance criteria are enforced by code

The handoff layer adds two useful constraints.

Creation without an acceptance condition fails.

Closing a handoff as `done` without a note describing how it was verified also fails.

The point is not to require ceremonial text.

The point is to prevent:

```text
"I finished"
```

from being silently promoted to:

```text
"the acceptance condition was satisfied and observed"
```

That is the same epistemic boundary Traceweave applies elsewhere:

```text
self-report
≠
execution proof
```

## The first real handoff exposed another design gap

The most useful test was not a unit test.

It was real use.

Claude created a durable obligation for Codex. The handoff existed on disk.

Codex checked the mailbox and found no new message.

Both observations were correct.

The reason was architectural:

```text
mailbox store
≠
handoff store
```

The obligation existed, but an executor looking only at messages would not discover it.

The operational correction was immediate:

```text
DURABLE HANDOFF
        +
SHORT MAILBOX MESSAGE
        ↓
pointer to the handoff
```

This produced a stronger rule:

> An obligation must not depend on a notification in order to exist, but it still needs a discovery path in order to be noticed.

A notification may be missed.

The obligation must remain.

But a durable obligation that nobody discovers is still operationally insufficient.

## Regression state after PONTE 22

After integrating durable handoffs, Claude Code recorded the following regression results:

```text
mailbox                     6/6
ponte-notificar             PASS
validar-ponte-timestamps    PASS
auditar-credenciais-repo    PASS
handoffs                   13/13
```

The bridge reports **58 cases in this bridge-related test set with no regression observed in that run**.

The wording matters.

It does not mean:

```text
58 tests
→ system proven correct
```

It means:

```text
58 observed checks
→ no regression observed in that execution
```

The current classification is therefore:

```text
STATUS:
TESTING PHASE

OBSERVED RESULTS:
GOOD

KNOWN LIMITATIONS:
STILL PRESENT

GENERAL PRODUCTION CLAIM:
NOT MADE
```

## The architecture that emerged

The bridge is now easier to understand as three separate contracts:

```text
                       Glaydson
                 authority / direction
                        |
                        v

               ┌──────────────────┐
               │ MARKDOWN BRIDGE  │
               │ causal history   │
               │ append-only      │
               └────────┬─────────┘
                        |
             reference / provenance
                        |
             ┌──────────┴──────────┐
             │                     │
             v                     v
    ┌────────────────┐    ┌─────────────────┐
    │ MAILBOX        │    │ HANDOFF         │
    │ durable        │    │ durable         │
    │ delivery       │    │ obligation      │
    └───────┬────────┘    └────────┬────────┘
            │                      │
        explicit ACK          state machine
            │                      │
            v                      v
         receipt          done | blocked
```

Each layer answers a different question.

### Bridge

```text
What happened?
Who recorded it?
What was the cause?
What evidence supports the claim?
What correction followed?
```

### Mailbox

```text
Is there something addressed to this executor?
Did it survive while the executor was absent?
Was it explicitly acknowledged?
```

### Handoff

```text
Is there unresolved work owned by someone?
Who claimed it?
What is the acceptance condition?
Was it completed or blocked?
How was closure verified?
```

## What this case supports

Within the observed evidence window, the material supports the following claims:

1. Codex CLI and Claude Code coordinated through a versioned bridge.
2. Disagreements and corrections were preserved instead of normalized retroactively.
3. Publication, notification and reading were treated as separate states.
4. A local durable mailbox was implemented.
5. Mail remained pending until explicit acknowledgement.
6. Acknowledgement produced a receipt bound to message content.
7. Claude Code independently reran the mailbox suite and recorded 6/6 passing cases.
8. A separate durable-obligation layer was implemented.
9. Handoffs enforce explicit acceptance criteria and explicit closure notes.
10. The handoff suite recorded 13/13 passing cases.
11. The bridge-related regression run recorded 58 checks without an observed regression.
12. Real use exposed a discovery gap between mailbox and handoff storage.
13. That gap produced a forward correction: durable handoff plus a short mailbox pointer.

The last point matters.

The system is not only passing tests.

It is still finding new failures when used.

Those failures are changing the architecture.

## What this case does not support

This experiment does **not** yet establish that:

- no message can be lost under every filesystem failure;
- all crash-consistency cases are covered;
- autonomous wake is reliable in every CLI state;
- a receiver will always be awakened immediately;
- extreme concurrent writers are fully handled;
- the design is suitable for multiple machines;
- local storage is equivalent to a distributed transactional queue;
- every durable obligation will be acted on merely because it exists;
- the system is generally production-ready;
- the current tests cover all relevant race conditions.

Persistence was addressed before full wake behavior.

That is deliberate.

## External alternatives were evaluated, not adopted

During the design discussion, external coordination approaches including **csend**, **Claude Code Agent Teams** and **oxtail** were considered.

They were not installed as part of this evidence window.

The experiment kept its own mechanisms separate so that these properties could be observed independently:

```text
causal record
transport
discovery
wake
obligation
receipt
```

External tools may remain useful references or future implementation choices. They are not part of the operational evidence claimed by this page.

## Why this belongs in Traceweave

The interesting result is not that two AI coding CLIs can exchange information.

That would only be a messaging demonstration.

The Traceweave-relevant part is that the communication itself preserved a causal genealogy:

```text
human direction
→ executor interpretation
→ action
→ error
→ peer objection
→ evidence
→ correction
→ commit
→ new state
→ new failure discovered in use
→ next correction
```

When one executor disagreed with another, the disagreement remained.

When instrumentation produced false state, that failure remained.

When durable transport solved persistence but not obligation ownership, the gap remained.

When durable handoffs solved ownership but exposed a discovery gap, that gap remained too.

The system did not need to rewrite its history into an artificially clean success story.

That is the point of the case.

## Observed state at this publication boundary

```text
EXECUTORS:
Codex CLI ↔ Claude Code

MARKDOWN BRIDGE:
ACTIVE

WRITE POLICY:
append-only blocks

DURABLE TRANSPORT:
IMPLEMENTED

MAILBOX:
tmp → new → cur + receipts

ACK:
EXPLICIT

RECEIPT:
SHA-256 BOUND

DURABLE HANDOFFS:
IMPLEMENTED

HANDOFF STATES:
handed-off
claimed
blocked
done

ACCEPTANCE CRITERION:
REQUIRED

DONE VERIFICATION NOTE:
REQUIRED

MAILBOX TESTS:
6/6 PASS

HANDOFF TESTS:
13/13 PASS

BRIDGE-RELATED REGRESSION RUN:
58 checks, no regression observed in that run

FULL AUTONOMOUS WAKE:
NOT PROVEN

EXTERNAL COORDINATION TOOL ADOPTED:
NONE

OVERALL STATUS:
TESTING PHASE, WITH GOOD RESULTS
```

## Conclusion

The bridge began as a Markdown file intended to prevent an executor change from destroying context and genealogy.

Use showed that this was not enough.

First the system had to separate:

```text
publishing
from
notifying
```

Then:

```text
notifying
from
durable delivery
```

Then:

```text
durable delivery
from
acknowledgement
```

And finally:

```text
acknowledgement
from
ownership of an obligation
```

The current architecture can be summarized in three lines:

```text
The bridge preserves the history.

The mailbox preserves the message.

The handoff preserves the obligation.
```

None of those mechanisms guarantees that an AI executor will do the right thing.

That is not the claim.

The objective is to make it possible to reconstruct, afterward:

**what was requested, what arrived, who claimed it, what was executed, where it failed, how it was corrected, and which claims still remain unproven.**

**CURRENT STATUS: TESTING PHASE, WITH GOOD RESULTS.**

**Superseded on 25/09/2026 — see [Correction](#correction--25092026) at the top: the transport failed in real use; the fix is in [Agents That Wake Each Other](agents-wake-each-other.md).**
