# Case 1 — unsupported source attribution

**Incident:** F09  
**Class:** factual/source-attribution divergence  
**Session:** `fa9c0182-f720-414b-9fe0-7a1525e74c96`  
**Model recorded in event:** `claude-opus-5`  
**Evidence class:** A — primary raw trace  
**Prompt ID:** `a51d84c6-2acf-4c1f-ac16-9e903630c335`

## Claim

At public transcript line 4733, the agent stated that explicitly anchoring citations in the prompt reduced hallucinated citations by **61%**, and linked that quantitative claim to a FutureAGI page.

It then used the claim to support an architectural recommendation.

## Primary event

```text
transcripts/public/fa9c0182-f720-414b-9fe0-7a1525e74c96.jsonl:L4733
```

The later incident anchor is:

```text
...jsonl:L4781
event_uuid = 293f3ec3-4133-49bc-9529-8ab37790b0c3
timestamp  = 2026-08-24T17:00:57.813Z
```

## Observed evidence

The source was subsequently fetched directly.

At line 4767, the tool result reports that the page did **not** contain:

- the number 61;
- a 61% reduction figure;
- the claimed Perplexity two-stage pipeline.

Pointer:

```text
...jsonl:L4767
```

## Contradiction

The quantitative claim had been presented with a source URL, but the cited source did not contain the attributed statistic or mechanism.

The agent had already narrowed the failure at line 4749:

> "Citei um número que nunca li na origem."

After the direct fetch, line 4781 records the stronger correction:

> "Eu inventei uma atribuição."

The research classification does **not** treat that sentence as proof of subjective intent. The promotable fact is the source mismatch.

## Correction / retraction

At line 4781 the agent withdraws both the number and the recommendation that relied on that evidence.

## Provenance pointer

```text
session_id: fa9c0182-f720-414b-9fe0-7a1525e74c96
claim:       L4733
admission:   L4749
source fetch:L4767
confirmation:L4770
retraction:  L4781
```

## Hashes

Sanitized public transcript SHA-256:

```text
08dbde0e18b2e3fcf4142d7a363cdcb729c59580acdd7aa66fd527c0a3ca9823
```

Selected line SHA-256 values, including trailing newline:

```text
L4749  f208ec8a66e8349baee0ced3c4c0066e306100eb2d7094b4049a24b12adc4ec2
L4767  496b6bc854d0a34ba1cd278efb517da767c0072ed51e896a68b853c025f7f5d0
L4781  8bcf797ab62102a3017dfaeb23cf24ef10ec25be069e65991b166bb7f6dbc50c
```

## Evidence class

**A — primary raw trace**, with direct tool-result contradiction inside the same session.

## Alternative explanations

A search intermediary may have generated or misattributed the 61% number. This case does not establish where the number first originated.

That narrower explanation does not remove the demonstrated issue: the agent attached the statistic to a source it had not verified, presented it as supporting evidence, and direct inspection showed the source did not contain it.

## Conclusion

This case demonstrates a **provenance failure**: second-hand material was elevated into source-backed evidence without verifying the cited source.

It does not require a claim about intent.
