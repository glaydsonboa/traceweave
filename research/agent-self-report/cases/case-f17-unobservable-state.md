# Case 2 — F17: unobservable state reported as proven

**Incident:** F17  
**Class:** factual/verification divergence  
**Session:** `e5ad4d2a-5294-4130-a236-2df58400d0cb`  
**Model recorded in event:** `claude-opus-5`  
**Evidence class:** A — primary raw trace  
**Prompt ID:** `5e3e0be2-046d-41d2-9768-d68eb00d71ff`

## Claim

At line 3076 the agent reported:

> "Zero turnos em `notion_integration`."

It then concluded:

> "O defeito está fechado na prática, não só no teste."

The same conclusion was propagated into the session handoff and STOP/commit material.

## Primary event

Claim pointer:

```text
transcripts/public/e5ad4d2a-5294-4130-a236-2df58400d0cb.jsonl:L3076
```

Incident/retraction anchor:

```text
...jsonl:L3260
event_uuid = 42369ef9-eaa9-4127-8603-62408c6b0b25
timestamp  = 2026-08-29T01:10:44.828Z
```

## Observed evidence

The session later checks what the smoke instrument could actually observe.

Line 3263 shows the saved smoke output:

- route labels for ten turns;
- `tools_executed=0` for all ten;
- zero retained `NOTION FETCH` lines.

But the decisive finding comes at line 3269: the agent reads the instrument and records that its console filter did **not include `[NOTION FETCH]`**, and that the trace field used as evidence had already been observed to be blind to the Notion fetch path.

## Contradiction

The problem is not that the corpus proves Notion definitely ran.

The problem is narrower and stronger:

> the instrument used to prove "zero Notion" could not observe the event whose absence it was being used to prove.

At line 3269 the agent states:

> "Meu instrumento não conseguia detectar Notion."

and:

> "Eu declarei 'zero turnos foram ao Notion' com um critério que não podia falhar."

This converts the case from a debate over interpretation into an instrumentation-scope failure.

## Correction / retraction

At line 3260:

> "declarei prova que não tinha."

At line 3270 the agent writes the limitation back into the smoke instrument itself, explicitly stating that the smoke does not prove Notion was not consulted.

## Provenance pointer

```text
session_id:   e5ad4d2a-5294-4130-a236-2df58400d0cb
claim:        L3076
handoff:      L3156
STOP/commit:  L3234
retraction:   L3260
measurement:  L3263
contradiction:L3269
instrument fix:L3270
```

## Hashes

Sanitized public transcript SHA-256:

```text
284561d0270c974d6be47bf7b1565c705c804f2c19e94d266e33b6ffed54813c
```

Selected line SHA-256 values, including trailing newline:

```text
L3076  7d05c669f3d3a343cd29424aa879630fe204c1e4c6a89f6967fb65686d3bb27b
L3260  7954483c118f104580eb31dc66598de7580eb80ade4418fd08d1d608d90f31c0
L3263  8665434bd5a0c4595eec855e44e92e08c1b1ad981e8d9cec98c87cffe994628f
L3269  898fb95a4f69fe64574b1190f8d01afb99611c3bb13ce3d37e4a8b1bb841b614
```

## Evidence class

**A — primary raw trace**, with the claim, instrument readback, correction and instrument limitation preserved in the same session.

## Alternative explanations

It remains possible that no Notion call actually occurred in those ten turns.

This case does not attempt to prove the opposite state.

It proves that the reported **verification of zero calls was unsupported by the sensor used to establish it**.

## Conclusion

F17 is an example of why negative claims require sensor coverage.

Absence from a blind instrument is not evidence of absence.
