# Command target guard

A `PreToolUse` hook that refuses material actions outside the single operational branch
(`canonical/worion` in the source repository). Measured on 25/09/2026, it had three defects and one missing exit.

## Defects

1. **Only the first `git -C` counted.** `git -C <canonical> status; <anything elsewhere>` passed: the guard
   checked the first target and ignored the rest of the command.
2. **`git -c` was read as `git -C`.** The pattern was case-insensitive, so
   `git -c user.name="…" -C <canonical> commit` failed with "target path must be absolute".
3. **Heredoc bodies were read as commands.** Once every segment was checked, a heredoc containing the text
   `git -C "${canonical}"` was denied — the new guard, already live, blocked the author's own command.

## What the guard checks now

- The command is split on `;`, `&&`, `||`, `|` and newlines, respecting quotes and backticks; heredoc bodies
  are removed first (they are data).
- Every `git -C <path>` segment is checked at its path; every other segment at the effective directory
  (the event `cwd`, or the last absolute `cd` / `Set-Location`).
- `-C` is case-sensitive; any number of `-c key=value` options may precede it.

## The missing exit

Cloud sessions start on a generated branch (`claude/*`). The guard denied everything there, including
`git checkout canonical/worion` — the only way out — and even tools that write nothing (`ToolSearch`,
asking the human). Now allowed outside the canonical branch:

- `git checkout canonical/worion` / `git switch canonical/worion`, exact, not chained, without `--` or `-b`;
- tools without writes: `Read`, `Grep`, `Glob`, `ToolSearch`, `AskUserQuestion`, `WebSearch`, `WebFetch`.

## Known gap

A `cd` with a redirection (`cd /other 2>/dev/null; …`) is not recognised as a directory change, so the
following segments are checked against the event `cwd`. Found while preparing this page; not fixed yet.

## Evidence

Source repository `leedermix-arch/worion-desktop`: commits `5731ebdb` (targets, `-c`/`-C`, heredoc),
`aae92efa` (exit and non-writing tools). Tests 11/11; mutations "only the first `-C`" (4 failures) and
"no exit" (1 failure).
