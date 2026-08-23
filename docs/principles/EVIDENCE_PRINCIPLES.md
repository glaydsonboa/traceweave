# Traceweave Evidence Principles

## 1. Evidence before conclusion

A claim becomes stronger only when the supporting evidence becomes stronger.

## 2. Unknown is not false

Absence of proof does not establish the opposite claim.

## 3. Missing evidence is not a fact

If an artifact, test or runtime observation cannot be found, record the absence as an observation about evidence availability.

Do not automatically claim the underlying event never happened.

## 4. Graphs navigate; source evidence confirms

Derived structural representations are valuable navigators.

When a graph and source/runtime disagree, the disagreement is a reason to investigate, not a reason to force one source to fit the other.

## 5. Runtime outranks stale narrative

A current runtime observation can supersede an old report about behavior.

A report remains useful provenance, but it is not stronger than contradictory current evidence.

## 6. A commit is not delivery proof

A commit proves that a repository object exists.

It does not automatically prove:

- push succeeded;
- deployment succeeded;
- the user saw the change;
- runtime accepted the change.

## 7. Checkpoint is not completion

A checkpoint can be `partial`, `blocked` or complete for a limited boundary.

It must not be interpreted as project completion unless that claim is separately supported.

## 8. Inference must remain labeled

Recommended evidence states:

- confirmed;
- derived;
- inferred;
- unknown;
- superseded.

Do not silently promote an inference to a fact.

## 9. Failure is evidence

A failed test is a valid result.

A blocked execution is a valid state.

A `not_run` test is more truthful than an invented pass.

## 10. Provenance is part of the technical record

The identity of the requester, author, prompt generator, executor and verifier can materially change the meaning of a technical artifact.

Preserve those roles when known.

## 11. Security does not justify fabrication

Redact or generalize sensitive values.

Do not replace them with invented evidence.

## 12. Reconciliation is mandatory

Evidence that changes the state of a problem should also change the backlog/state representation.

Otherwise solved work is repeatedly rediscovered.

## 13. Divergence is information

When two evidence surfaces disagree, that divergence can reveal:

- stale indexes;
- indirect dependencies;
- missing instrumentation;
- incomplete reports;
- incorrect causal assumptions.

Treat disagreement as a search target.

## 14. Public claims require public evidence

Do not make a strong public technical claim if the only support is private and cannot be safely described.

Either publish adequate sanitized evidence or weaken the claim.
