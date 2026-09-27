# Contributing to Traceweave

Thank you for helping improve Traceweave. The project is about verifiable engineering continuity: claims about sessions, tests, Git state, provenance, and publication must stay inspectable and no stronger than the evidence behind them.

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before participating. Its error classes (E01–E09) apply to all content.

## Before you start

- Check existing [issues](https://github.com/glaydsonboa/traceweave/issues) and [pull requests](https://github.com/glaydsonboa/traceweave/pulls) to avoid duplicating active work.
- Keep the change narrow. Separate unrelated fixes into separate pull requests.
- For protocol or behavioral changes, describe the problem and its evidence boundary before implementing a solution.
- Never include credentials, private transcripts, personal data, local machine paths, or unpublished source material.

## Development setup

Traceweave requires Python 3.11 or newer.

```bash
git clone https://github.com/glaydsonboa/traceweave.git
cd traceweave
python -m venv .venv
# activate the virtual environment, then:
pip install -e ".[test]"
```

Run the Python test suites:

```bash
python -m unittest discover -s tests
pytest
```

The JavaScript utilities use the Node.js built-in test runner:

```bash
node --test tools/generate-ids.test.js tools/mailbox-watch.test.js
```

## Contribution principles

These rules run through the protocol, implementation, documentation, and research material:

1. Evidence beats memory.
2. Unknown is a valid state.
3. Executed, observed, and narrated state stay separate until evidence links them.
4. Git claims must identify the exact revision they describe.
5. Tests count as facts only when their command and observed result are reported.
6. A logical ID is not a publication receipt; destination-native identity and readback remain separate evidence.
7. Corrections move forward. Do not rewrite published history merely to hide an earlier error.
8. Limits and alternative explanations should be explicit.

## Use of AI

AI assistance is welcome, under the same evidence rules as everything else here:

- The human who submits the pull request is the author and the responsible party. If you cannot explain a change line by line, do not submit it.
- Disclose AI assistance in the pull request description: which tool, which parts it touched, and how much of the result is generated (for example, `Assisted-by: <tool>/<model>`).
- AI-generated code passes the same tests as any other code, with results actually observed and reported.
- Do not open issues, pull requests, comments, or reviews through an unsupervised agent.
- Do not send credentials, private transcripts, or unpublished material to third-party AI systems.
- "Vibe-coded" pull requests — accepted on behavior alone, without review, tests, or understanding — will be rejected.

## Code changes

- Preserve the local-first, deterministic, and conservative design.
- Do not add network, model, daemon, or cloud dependencies to the core protocol without a clearly justified boundary.
- Keep read-only inspection separate from mutation and publication capabilities.
- Add or update tests for behavior changes, including failure paths and explicit unknown states.
- Avoid broad refactors in the same pull request as a behavioral fix.
- Update documentation when a public command, schema, or protocol rule changes.

## Documentation and research contributions

Documentation should distinguish what a source proves from what is inferred.

For evidence-backed research or case material:

- identify the concrete claim under review;
- point to the strongest available primary source;
- explain the observation method and its visibility limits;
- separate source material from derived analysis;
- record plausible narrower explanations where the evidence permits them;
- avoid claims about intent unless intent is directly evidenced and relevant;
- sanitize secrets and personal data structurally, not only through visual review;
- include hashes, native identifiers, or reproducible commands when they materially support the claim.

A self-report proves what an agent reported. It does not, by itself, prove that the reported action occurred.

## Pull requests

A pull request should include:

- the problem and bounded scope;
- the files and behavior changed;
- the evidence supporting the change;
- the exact tests run and their observed results;
- known limitations, unverified claims, and follow-up work;
- documentation impact, if any.

Keep commits reviewable and avoid force-pushing to erase a mistake already under review. Maintainers may ask for a follow-up commit when preserving the correction history is useful evidence.

By submitting a contribution, you agree that it is provided under the repository's [Apache License 2.0](LICENSE).
