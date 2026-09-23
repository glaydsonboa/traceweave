# Proven Governance

## Why this folder exists

**Proven governance** is governance that can be reconstructed from evidence.

It is not a policy document that asks the reader to trust that a process was followed. It is a process in which authority, instruction, execution, artifacts, destination identities, readback, correction, and closure remain independently inspectable.

In Traceweave terms, governance becomes stronger when the system can answer, with evidence:

- Who had authority to request the change?
- What instruction or prompt defined the change?
- Which executor acted?
- What artifact was produced?
- What content identity did that artifact have?
- Where was it materialized?
- What native identity did each destination assign?
- Was the destination read back after the write?
- Are the returned bytes the same bytes that were intended?
- Was runtime behavior measured separately from the narrative about runtime?
- Was the user-visible or persisted effect proved?
- If an earlier claim was wrong, was it preserved and corrected forward instead of silently rewritten?

This folder explains that model.

## Downloadable generic governance artifacts

The three documents below are sanitized, English, public-reference derivatives of internal governance artifacts. Personal names are replaced with `<user name>`; project-specific IDs, paths, dates, commits, machine details, private repository names, and model-specific rules are generalized.

- [01 — Operational Law: Dual Provenance and Source Headers](./01_DUAL_PROVENANCE_AND_HEADER_LAW.md)
- [02 — Devil's Advocate Governor: Independent Adversarial Audit](./02_ADVERSARIAL_GOVERNANCE_AUDITOR.md)
- [03 — Daily Provenance Governor](./03_DAILY_PROVENANCE_GOVERNOR.md)

### Provenance correction — document 03

Document 03 was **formulated by ChatGPT under `<user name>`'s authority and direction**. This attribution is recorded forward-only; the earlier publication remains in Git history.

Current causal pair identifiers:

- `PAIR_KEY`: `20260923-153843-governanca-comprovada-arquivos-genericos`
- `GITHUB_ID`: `PROV-GITHUB-20260923-153843-governanca-comprovada-arquivos-genericos`
- `NOTION_ID`: `PROV-NOTION-20260923-153843-governanca-comprovada-arquivos-genericos`
- paired manifest: [04 — Paired Publication Manifest](./04_PAIRED_PUBLICATION_MANIFEST.md)

These public derivatives preserve the governance logic while intentionally not preserving private operational identifiers.

It does **not** claim that governance is correct merely because a document exists. The governing principle is the opposite:

> A governance claim must remain distinguishable from the evidence that can verify or invalidate it.

---

## 1. The core idea

Traditional governance can collapse several different statements into one:

```text
a rule exists
therefore
the rule was followed
therefore
the expected effect happened
```

Traceweave rejects that collapse.

A stronger causal chain is:

```text
AUTHORITY
→ CAUSE
→ INSTRUCTION / PROMPT
→ EXECUTOR
→ LIFECYCLE EVIDENCE
→ SOURCE ARTIFACT
→ CONTENT IDENTITY
→ DESTINATION MATERIALIZATION
→ DESTINATION-NATIVE IDENTITY
→ READBACK
→ TEST / RUNTIME OBSERVATION
→ EFFECT PROOF
→ CLOSURE
```

Each arrow is a boundary.

Evidence at one boundary does not automatically prove the next.

For example:

```text
file exists
≠ file is loaded
≠ file is called
≠ code executed
≠ expected effect occurred
≠ user received the effect
```

This is the first rule of proven governance:

> **Do not promote a lower evidence level into a higher one by narrative inference.**

---

## 2. Human authority and execution are different identities

Governance begins with authority.

The person or process that has authority to define the cause, accept a correction, or approve a mutation is not necessarily the same actor that writes the code or creates the external artifact.

A useful distinction is:

```text
authority
≠ originator
≠ prompt author
≠ executor
≠ committer
≠ runtime identity
≠ reviewer
```

These identities may sometimes belong to the same person or system, but governance should not assume that they do.

This matters especially in AI-assisted engineering.

An AI may:

- propose a plan;
- write code;
- execute commands;
- create commits;
- create documentation;
- report completion.

None of those facts automatically gives the AI architectural authority.

Likewise, a `Co-Authored-By` trailer, a session label, or a model name is provenance metadata. It is not cryptographic proof of who physically executed every command.

Proven governance records the distinction instead of flattening it.

---

## 3. Executed state, observed state, and narrated state

Traceweave treats these as three independent dimensions:

```text
executed state
≠ observed state
≠ narrated state
```

### Executed state

What commands, mutations, writes, commits, tool calls, or runtime actions actually occurred.

### Observed state

What an independent observation surface can see afterward: Git state, returned API state, filesystem state, test output, database row, runtime trace, remote readback, or destination object.

### Narrated state

What an executor, report, agent, checkpoint, or STOP message says happened.

A narrated statement can be correct.

It can also be incomplete, stale, overconfident, or false.

Therefore:

> **Agent self-report is evidence of what the agent reported, not proof that the reported effect occurred.**

This is not an accusation of intent. It is a measurement rule.

---

## 4. Temporal continuity: START, RESUME, and STOP

Traceweave V2 models lifecycle continuity through explicit events:

```text
START → RESUME* → STOP
```

These events answer different questions.

- **START**: what state and authority boundary existed when the work began?
- **RESUME**: what prior state is the current execution explicitly recovering from?
- **STOP**: what artifact, state, evidence, or unresolved condition exists at closure?

A valid STOP does not retroactively make an invalid START valid.

A valid RESUME does not prove that every earlier event was recorded correctly.

The chain is therefore evaluated link by link.

Example:

```text
START: PARTIAL
RESUME: CONFIRMED
STOP: CONFIRMED

OVERALL TEMPORAL CONTINUITY: PARTIAL
```

This rule prevents a strong closing statement from laundering a weak beginning.

---

## 5. Causal identity is not content identity

Traceweave keeps several identity layers separate:

```text
session identity
≠ event identity
≠ content identity
≠ causal pair identity
≠ native destination identity
≠ proof of materialization
```

### Content identity

A cryptographic digest such as SHA-256 identifies the bytes of an artifact.

### Causal pair identity

A logical identity such as `PAIR_KEY` correlates two projections intended to represent the same causal update.

### Native destination identity

GitHub and Notion assign their own immutable or destination-specific identities: commit SHA, blob SHA, page ID, attachment ID, and similar identifiers.

These must not be conflated.

A logical ID does not prove that anything was written.

A SHA-256 does not prove where the content was published.

A Git commit does not prove a Notion attachment.

A Notion page does not prove the Git object.

Proven governance requires the identities to remain distinct and linkable.

---

## 6. Paired publication

A paired publication can be represented as:

```text
PAIR_KEY
├── GITHUB_ID
│   └── native GitHub identity
│       └── content identity
│           └── readback
└── NOTION_ID
    └── native Notion identity
        └── content identity
            └── readback
```

The logical identifiers correlate the two descendants.

They are **not receipts**.

A pair becomes materially stronger only after both destinations independently provide:

1. destination-native identity;
2. content identity;
3. confirmed readback.

For source artifacts, the publication should also expose a downloadable artifact descriptor containing at least:

- filename;
- extension;
- byte length;
- SHA-256;
- download reference.

Rendered code is a view.

It is not a substitute for the source artifact.

---

## 7. Independent custody is not paired publication

Traceweave V2 deliberately separates two mechanisms that are often both described as “dual provenance”:

```text
independent custody mirror
≠
paired GitHub / Notion publication
```

### Independent custody

The objective is preservation.

```text
SOURCE BYTES
→ source SHA-256 + byte count
→ independently controlled replica
→ replica SHA-256 + byte count
→ readback
→ overwrite protection
```

A confirmed custody record requires exact content preservation and independent control strong enough that one ordinary writer cannot silently remove both copies.

### Paired publication

The objective is causal external materialization.

```text
SOURCE / UPDATE
→ PAIR_KEY
→ GitHub descendant
→ Notion descendant
→ native identities
→ readback
```

Custody can exist without publication.

Publication can exist without independent custody.

One must never be reported as the other.

---

## 8. Byte identity means exact bytes

Human-visible equality is not byte equality.

Two payloads may render identically while being different artifacts.

For example:

```text
payload A: "same visible line\n"
payload B: "same visible line\n\r\n"
```

Those payloads differ.

Their byte counts differ.

Their SHA-256 hashes differ.

Therefore:

> **Byte identity requires readback of the destination artifact, not visual inspection of rendered text.**

Line-ending normalization, appended newlines, encoding conversion, BOM insertion, or any other transport mutation must be visible to verification.

A two-byte difference is still a failed byte-identity claim.

---

## 9. Readback is part of the write

In proven governance, “write succeeded” is not the final statement.

The operational sequence is closer to:

```text
write
→ destination accepts mutation
→ obtain native destination identity
→ read the destination again
→ verify returned state/content
→ record the evidence
```

Readback protects against several classes of false closure:

- writing to the wrong destination;
- writing to the wrong branch;
- writing stale content;
- silent normalization;
- partial API success;
- confusing a local object with a remote object;
- treating a generated ID as proof of external existence.

The strongest statement is not:

> “The tool returned success.”

It is:

> “The destination was written, independently read back, and the returned artifact/state satisfied the declared verification contract.”

---

## 10. Forward-only correction

Proven governance does not require history to look perfect.

It requires history to remain reconstructable.

When an earlier published claim is wrong:

```text
ERROR / INVALIDATED CLAIM
→ preserve prior evidence
→ issue a new correction identity
→ create a new commit or artifact
→ prove the corrected state
→ link the correction to what it supersedes
```

The preferred rule is:

> **Do not rewrite the past to make the present look cleaner. Correct forward.**

In practical terms, this means avoiding retroactive identity fabrication and avoiding history-changing corrections merely to hide an error.

If an earlier artifact had no `PROMPT_ID`, `COMMAND_ID`, `EXECUTION_ID`, or pair identity, the absence is part of the evidence.

A later system may document that gap.

It should not pretend the historical ID existed.

This creates genealogy instead of cosmetic consistency.

---

## 11. Mutation prompts are part of governance

Governance does not begin only after code exists.

The mutation instruction itself is part of the evidence chain.

A mutation prompt should define, as applicable:

- cause;
- allowed scope;
- protected scope;
- expected artifacts;
- identity requirements;
- header reconciliation;
- sanity checks;
- commit boundary;
- remote publication/readback requirement;
- runtime verification;
- effect proof;
- closure criteria.

For source code, scripts, tests, or configuration files that use canonical governance headers, a mutation instruction should explicitly require those headers to be reconciled with the post-change state.

If that obligation is required by the project contract but is missing from the prompt, the correct classification is not silent compliance.

It is a prompt defect that must be surfaced before mutation.

This turns the prompt from informal prose into an auditable boundary.

---

## 12. Headers are evidence-bearing metadata

A source header should describe the artifact that actually exists after the change.

It should not preserve a stale description merely because the implementation changed below it.

At the same time, provenance headers should not be retroactively rewritten to invent historical identities.

The distinction is:

```text
reconcile current descriptive metadata
≠
rewrite historical provenance
```

A good governance header can help answer:

- what this file does;
- what consumes it;
- what contract it participates in;
- what evidence surface proves its use;
- which identity fields are genuinely available.

A header is not a substitute for runtime proof.

It is an index into the causal structure.

---

## 13. The operational proof sequence

A complete engineering mutation may follow a sequence such as:

```text
CAUSE
→ PLAN
→ IDS
→ HEADERS
→ CODE
→ SANITY
→ COMMIT
→ PUSH
→ REMOTE READBACK
→ TEST
→ MUTATION / EXTERNAL WRITE
→ RUNTIME OBSERVATION
→ EFFECT PROOF
→ CLOSURE
```

This sequence distinguishes several common false positives.

### Sanity is not runtime

Syntax checks, type checks, static tests, and schema validation prove important properties.

They do not prove the live effect.

### Runtime is not effect

A function can execute successfully while producing the wrong user-visible or persisted result.

### Commit is not publication

A local commit does not prove that the expected remote branch contains it.

### Push is not readback

A push command returning success should still be followed by remote observation when closure depends on the remote state.

---

## 14. Failure and partial states are valid outcomes

A governance system becomes unreliable when every path is forced into “success.”

Traceweave allows unresolved states to remain unresolved.

Useful classifications include:

```text
CONFIRMED
PARTIAL
UNVERIFIED
FAILED
SUPERSEDED
INVALIDATED
UNKNOWN
```

The names may vary by implementation, but the principle is stable:

> **Unknown is better than fabricated certainty. Partial is better than a false complete.**

Examples:

- GitHub materialized, Notion unavailable → publication pair remains partial.
- Both destinations exist but pair identities were generated only afterward → content may be confirmed while causal pair validity remains partial.
- Bytes differ after readback → byte identity fails even if the UI looks identical.
- STOP says complete but runtime effect was not measured → narrated closure exists; effect proof does not.
- A private corroborating commit is cited but cannot be independently inspected by a public reader → it is corroboration, not self-sufficient public proof.

---

## 15. Evidence levels

A practical evidence ladder is:

### E0 — Narrative

A person or agent says something happened.

### E1 — Local artifact

A file, report, transcript, or generated object exists locally.

### E2 — Content identity

The artifact has measured bytes and a cryptographic digest.

### E3 — Native materialization

An external destination assigns a native identity.

### E4 — Readback

The destination is independently read after the write.

### E5 — Causal correlation

The destination materializations can be shown to descend from the same pre-existing causal identity.

### E6 — Runtime proof

The relevant code path or operational path is observed executing.

### E7 — Effect proof

The intended persisted, external, or user-visible effect is observed.

A project may refine this ladder, but it should not narratively jump from E1 to E7.

---

## 16. Public evidence already present in Traceweave

This repository contains public artifacts that exercise these ideas.

### Traceweave V2 causal continuity

Commit:

`a2e4890bcc7d94db7488dbe9b9e77132864ed2b2`

Published the V2 causal-continuity specification, reference primitives, schema, examples, and tests.

It joins temporal continuity with paired provenance, content identity, destination identity, readback, and forward-only correction.

### Custody separated from paired publication

Commit:

`57000375902f7042d2e23d17a6764e0893116369`

Made the public boundary explicit:

```text
independent byte-preserving custody mirror
≠
paired GitHub / Notion publication
```

It also strengthened exact-byte verification and source-artifact requirements.

### Audited multi-agent reconstruction

Commit:

`df1a8f86a3c41b3d2f5348447fe5c28524595232`

Published a longitudinal reconstruction that preserved an earlier overclaim and recorded the primary-evidence correction instead of erasing the contradiction.

### Operational causal chain

Commit:

`99f1e0c6ecd46b0cb9f2b8bc5f827e22eb4e7bb4`

Published an operational reconstruction comparing declared governance with observed behavior.

A key result was itself governance-relevant: content identity and destination readback could be confirmed while causal pair identity at the first write was missing. The correct result remained partial rather than being upgraded by narrative.

That is an important property of the protocol:

> The process is allowed to reveal that the process failed its own rule.

---

## 17. What “proven governance” can prove

When properly instrumented, this model can support claims such as:

- a specific artifact existed with a specific content hash;
- a specific destination materialized an artifact under a native identity;
- that destination was read back;
- two destination artifacts were or were not byte-identical;
- a causal pair identity existed before materialization;
- an earlier claim was preserved and later corrected;
- an execution path was observed;
- an intended effect was or was not observed;
- a governance rule was satisfied, partially satisfied, or violated.

This makes governance inspectable instead of ceremonial.

---

## 18. What it does not prove by itself

Provenance is not omniscience.

This model does not, by itself, prove:

- a person's psychological intent;
- that an AI consciously intended to mislead;
- that a commit author executed every command in a session;
- that an unobserved event did not happen;
- that two matching hashes imply correct semantics;
- that a valid STOP contains a complete account of the entire session;
- that source-code presence implies runtime use;
- that runtime execution implies correct user-visible effect;
- that a logical pair ID proves external publication.

A mature governance system records these limits explicitly.

---

## 19. Audit checklist

A reviewer can use the following questions.

### Authority

- Is the authority for the change identified?
- Is authority separated from executor identity?

### Instruction

- Is the cause explicit?
- Is the mutation scope explicit?
- Are protected areas identified?
- Were required IDs generated before first materialization?
- Were required headers included in the mutation contract?

### Artifact

- Is the source artifact available?
- Is the byte length known?
- Is SHA-256 recorded?
- If it is source code, is the native downloadable file preserved?

### Git

- Is there a commit or native Git object?
- Is the intended branch known?
- Was remote state read back?
- Is the blob/content identity available where needed?

### External destination

- Does the destination have a native identity?
- Was the destination read back?
- Does the readback correspond to the intended artifact?

### Pairing

- Was `PAIR_KEY` created before destination materialization?
- Do both descendants retain their own native identities?
- Is one destination being incorrectly used as proof of the other?

### Byte verification

- Were actual destination bytes compared?
- Were line endings and trailing bytes preserved?
- Does byte count match?
- Does SHA-256 match?

### Runtime

- Was the relevant code path actually observed?
- Is the observer independent of the executor's narrative where possible?

### Effect

- Was the intended persisted or user-visible effect observed?

### Closure

- Is the result honestly classified?
- Are partial and unknown states preserved?
- If a prior claim was wrong, was correction forward-only?

---

## 20. A compact definition

**Proven governance** is the practice of making the governance process itself subject to the same evidentiary discipline as the system it governs.

In compact form:

```text
rule
≠ compliance

instruction
≠ execution

execution
≠ observation

observation
≠ narration

logical ID
≠ publication receipt

rendered equality
≠ byte identity

commit
≠ remote readback

runtime
≠ effect

correction
≠ erasure
```

The objective is not to eliminate error.

The objective is to make error, correction, authority, execution, and proof reconstructable.

---

## 21. Final principle

The strongest property of this governance model is not that every execution passes.

It is that a contradiction between rule and operation is allowed to become evidence.

```text
if operation contradicts governance
→ preserve the contradiction
→ classify the failure
→ generate a new causal correction
→ prove the corrected state
→ keep the old evidence inspectable
```

That is the difference between governance that is merely declared and governance that can be tested.

That is **proven governance**.

---

## Publication status of this document

This README is currently a **GitHub materialization** in the public Traceweave repository.

Its presence here does not, by itself, claim a completed GitHub/Notion publication pair.

If this document is later paired with another destination, the pair must satisfy the Traceweave V2 requirements independently: pre-existing causal IDs, native destination identities, content identity, readback, and the appropriate verification state.
