# Public Demo Plan — Prove Continuity Without Multi-Agent Orchestration

## Goal

Demonstrate that a second engineering session can recover the last verified technical boundary and detect drift without trusting conversational memory.

## Constraints

Use one repository, one user, one CLI or no AI at all, no cloud service, no project-specific dependency, and a reproducible clean public repository. The main proof should fit in roughly one minute.

## Demo — Continuity Guard

Session A:

```bash
git init demo
cd demo
echo "v1" > app.txt
git add app.txt
git commit -m "initial"

traceweave stop \
  --summary "Initial implementation complete" \
  --executor "human" \
  --open "Add validation"
```

Between sessions:

```bash
echo "v2" >> app.txt
git add app.txt
git commit -m "change after checkpoint"
```

Session B:

```bash
traceweave resume
```

Expected visual:

```text
last verified HEAD: abc123
current HEAD:       def456
drift:              yes

completed:
✓ initial implementation complete

open:
○ add validation

tests:
? not observed after checkpoint
```

## What the demo proves

The proof is not agent transfer. It is that session A leaves an inspectable evidence boundary and session B reconstructs that boundary correctly after repository state changes.

Use a neutral, reproducible repository as the proof target. Keep the demo deterministic and make unknown evidence visible rather than filling gaps with narrative assumptions.
