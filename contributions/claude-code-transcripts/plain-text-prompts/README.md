# User prompts shown as typed

Upstream issue [#35](https://github.com/simonw/claude-code-transcripts/issues/35) · pull request [#119](https://github.com/simonw/claude-code-transcripts/pull/119)

## The problem

User prompts were rendered as Markdown. Paste a few lines of config or code and a `# comment` becomes a heading, and `*value*` turns into emphasis. The transcript no longer shows what the human actually typed.

## The fix

[`user-prompts-plain-text.patch`](user-prompts-plain-text.patch) renders user prompts as escaped plain text, keeping line breaks and whitespace (`white-space: pre-wrap`). It covers:

- string content and the newer array format (`[{"type": "text", ...}]`) on transcript pages;
- the prompt previews on the index page, in both `generate_html` and `generate_html_from_session_data`.

Assistant text and thinking are still rendered as Markdown.

One trade-off, stated in the pull request: session continuation summaries arrive as user messages, so they are shown as plain text too.

## Verification

- A new test fails before the change and passes after.
- The four HTML snapshots change only by the new `user-text` class.
- Upstream suite: 123 tests pass.
