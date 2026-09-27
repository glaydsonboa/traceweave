# Security Policy

## Supported versions

Traceweave is experimental and evolving. There is currently no tagged release. Security fixes are applied to the current `main` branch. Older commits, research snapshots, and superseded examples are preserved for provenance but are not maintained as supported release lines.

| Version | Supported |
| --- | --- |
| Current `main` | Yes |
| Older snapshots or releases | No |

## Reporting a vulnerability

Please do not disclose a suspected vulnerability in a public issue, pull request, discussion, transcript, or evidence bundle.

Use GitHub's private vulnerability reporting for this repository when the **Report a vulnerability** option is available on the Security tab. Include:

- the affected version or exact commit;
- the smallest reproducible sequence;
- the observed security impact;
- affected files, tools, or MCP scopes;
- sanitized logs or proof-of-concept material;
- any known preconditions or limitations.

If private vulnerability reporting is not available, ask the repository owner for a private reporting channel before sending details. Do not send vulnerability details through a public GitHub surface.

Preferred language: English.

Good-faith reports that follow this policy will not lead to enforcement action against the reporter.

You should receive an acknowledgement after the report reaches a private channel. Validation time depends on reproducibility and impact. Confirmed fixes will be coordinated before public disclosure, and the reporter will be credited unless anonymity is requested.

## Relevant security boundaries

Reports are especially useful when they concern:

- repository path traversal or access to `.git` internals through the MCP server;
- bypass of `read`, `write`, or `publish` scopes;
- Git argument or remote-target injection;
- unintended staging, commit, push, or overwrite behavior;
- credential, token, private-path, transcript, or personal-data exposure;
- a network or filesystem action that contradicts a documented safety boundary;
- dependency vulnerabilities with a concrete effect on Traceweave.

Protocol disagreements, unsupported evidence claims, and reproducibility challenges that do not create a security impact belong in the public issue templates instead.

## Disclosure and evidence handling

Traceweave's evidence rules also apply to security work:

- preserve the original report privately;
- distinguish observed impact from inference;
- do not publish secrets or exploit details before a fix is available;
- identify exact revisions and test results;
- correct public statements forward if later evidence changes the verdict.

This policy does not promise that a report is valid merely because it was submitted. It promises that security claims will be evaluated against reproducible evidence and handled without unnecessary public exposure.
