# Contributions to simonw/claude-code-transcripts

[claude-code-transcripts](https://github.com/simonw/claude-code-transcripts) turns Claude Code session files into HTML transcripts. Traceweave keeps a record of human direction across AI coding sessions, so a transcript that drops or distorts what the human typed matters here. These are the problems we found and the fixes we sent upstream. The code lives here, and the upstream pull requests deliver it.

| Upstream issue | Problem | Pull request | Code here |
|---|---|---|---|
| [#98](https://github.com/simonw/claude-code-transcripts/issues/98) | Prompts typed while Claude is working are missing from the transcript | [#118](https://github.com/simonw/claude-code-transcripts/pull/118) | [`queued-prompts/`](queued-prompts/) |
| [#35](https://github.com/simonw/claude-code-transcripts/issues/35) | User prompts are rendered as Markdown, so a pasted `# comment` becomes a heading | [#119](https://github.com/simonw/claude-code-transcripts/pull/119) | [`plain-text-prompts/`](plain-text-prompts/) |

Both pull requests are open and waiting for the maintainer. Both patches apply cleanly to upstream `main` at `316fd093`. The upstream suite passes with each one: 123 tests, formatted with Black.

## How the work was done

Each fix followed the upstream `AGENTS.md`: first a test that fails, then the change, then the full suite.

The pull requests were written with AI assistance (Claude Code) under human direction, and they say so.

## Correction

When #98 was first answered, the upstream comment said that without the fix, 10 of 62 queued prompts were missing. That count matched text fragments rather than whole prompts, so it undercounted.

Measured again with exact matching (see [`queued-prompts/`](queued-prompts/)), on the same sessions and up to the same moment:

- 63 prompts were queued.
- Without the fix, 26 are missing.
- With the fix, 2 are missing. One was delivered with more text than was queued. The other has no delivery record that we could find.

The upstream comment and pull request are corrected to match.
