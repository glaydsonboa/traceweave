---
document_role: paired-governance-publication
status: reference-template
authority: <user name>
prompt_id: PROJECT-PROMPT-YYYYMMDD-HHMMSS-<slug>
notion_id: PROV-NOTION-YYYYMMDD-HHMMSS-<slug>
github_id: PROV-GITHUB-YYYYMMDD-HHMMSS-<slug>
pair_key: YYYYMMDD-HHMMSS-<slug>
---

# Operational Law — Dual Provenance and Source Headers

## Purpose

This document defines two independent evidence layers and a source-header rule for governed engineering work. It is a generic public derivative of an operational governance contract; project-specific identities, paths, dates, commits, model names, machine details, and private repository references have been replaced with neutral placeholders.

## Decision

A governed system recognizes two independent layers:

1. **Protected source-evidence mirror.** A completed native transcript, JSONL stream, log bundle, or equivalent primary artifact is preserved in the operational evidence root and copied, with SHA-256 verification and overwrite protection, to a separately controlled custody location.
2. **Paired GitHub ↔ Notion publication.** A curated update receives a `NOTION_ID`, `GITHUB_ID`, and shared `PAIR_KEY`. The pair is confirmed only after both destinations are written and independently read back. A byte-identity claim requires the downloadable Notion artifact and the GitHub blob to have identical bytes and identical SHA-256 values.

The protected mirror preserves the source. The GitHub/Notion pair correlates an external publication. One does not replace the other.

Published source code remains a real downloadable artifact. Python (`.py`), JavaScript (`.js`), configuration, tests, or other source files must not exist only as rendered code blocks. GitHub preserves the native file. When Notion is part of the pair, Notion receives a downloadable attachment and readback must prove the attachment can be retrieved. A rendered block is a convenience for reading and copying; it is not the evidentiary artifact.

## Source-header law

Every prompt that authorizes modification of code, scripts, tests, or configuration governed by a source-header convention must explicitly require the executor to rewrite or reconcile the header of every touched file in the same causal change.

The executor must:

- describe the actual post-change state;
- follow the project's current header contract, for example `docs/MODULE_HEADER.md`;
- never invent authorship, IDs, responsibilities, provenance, or genealogy;
- identify, at closure, any touched files to which the convention does not apply and explain why.

A mutation prompt that omits a required header instruction is `PROMPT_INCOMPLETE`. A patch that leaves a semantically stale header is also incomplete.

This rule does not authorize retroactive provenance fabrication. Updating a current descriptive header is different from inventing an ID that did not exist historically.

## Session lifecycle evidence

`START`, `RESUME`, and `STOP` remain separate responsibilities.

A previous session proving one lifecycle cutoff does not promote future sessions. Every session must independently preserve its own:

- source artifact or transcript;
- lifecycle evidence;
- commit when applicable;
- push when applicable;
- remote readback;
- unresolved limitations.

The correct logic is link-by-link:

```text
START: <state>
RESUME: <state>
STOP: <state>
OVERALL: weakest material state still open
```

Two confirmed links do not transform a third missing or partial link into a confirmed chain.

## Generic contract surfaces

A project implementing this law may maintain sources such as:

- `contracts/OPERATIONAL_TEAM_CONTRACT_V2.md`;
- `contracts/PROMPT_PROVENANCE_EXECUTION_CONTRACT_V2.md`;
- `contracts/START_RESUME_STOP_CONTRACT_V2.md`;
- `.agent/skills/cross-project-governance/SKILL.md`;
- `docs/MODULE_HEADER.md`;
- `docs/continuity/STOP_RESUME_HOOKS.md`;
- `scripts/session-start-hook.js`;
- adapter contracts for each supported executor.

These names are illustrative. The governing requirement is the contract function, not the literal path.

## Graph or indexer limitation

A repository graph, code index, dependency map, or generated architecture index is evidence only within its measured scope and build point.

Before using such an instrument as evidence:

1. identify its `built_at_commit` or equivalent cutoff;
2. compare that cutoff with the current HEAD;
3. confirm that the instrument indexes the contract, skill, script, or path being discussed;
4. classify stale or out-of-scope output as a limitation.

A stale or incomplete graph can prove the limit of the instrument. It cannot prove the positive operational chain that it does not observe.

## Publication state

The logical pair should be generated before the first external materialization:

```text
PAIR_KEY=YYYYMMDD-HHMMSS-<slug>
GITHUB_ID=PROV-GITHUB-YYYYMMDD-HHMMSS-<slug>
NOTION_ID=PROV-NOTION-YYYYMMDD-HHMMSS-<slug>
```

The state remains `PARTIAL` until both destinations are written and read back under their native identities.

Final confirmation must record, as applicable:

- GitHub commit SHA;
- Git blob SHA or repository-native content identity;
- Notion page ID and attachment/file identity;
- SHA-256 observed from each destination;
- byte count observed from each destination;
- readback method;
- pair verdict;
- limitations.

## Core rule

```text
protected custody
≠ paired publication

logical IDs
≠ publication receipt

rendered similarity
≠ byte identity

header presence
≠ runtime proof
```

The purpose of this law is not to make documentation look complete. It is to keep preservation, publication, mutation metadata, lifecycle evidence, and readback as independently testable claims.
