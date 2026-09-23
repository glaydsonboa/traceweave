# Header Contract Linter

## Purpose

Header Contract Linter checks whether source-file contract headers remain structurally complete and consistent with repository policy.

## Scope of version 0.1

Version 0.1 is a structural linter, not a semantic code-understanding engine. It should validate required field presence, ordering when required, duplicate fields, forbidden empty fields, declared path existence, allowed enum values, schema version, explicit unknown handling, and short-header versus full-header policy by path/type.

It should not claim that prose assertions about runtime behavior are true merely because they appear in a header.

## Mutation-prompt boundary

When a repository requires source headers, a mutation prompt or change contract
should explicitly require the executor to reconcile every applicable header in
the same change. The executor should update the header to describe the
post-change state or report why the policy does not apply.

The linter can prove that this structural obligation was represented and that
required fields are present. It cannot prove semantic truth from header prose.

## Example configuration

```yaml
version: "0.1"

rules:
  - match: "src/**/*.js"
    schema: "runtime-module"
  - match: "tests/**/*.test.js"
    schema: "test-short"

schemas:
  runtime-module:
    ordered_fields:
      - Name
      - Module ID
      - Responsibilities
      - Dependencies
      - Tests
      - Runtime status
      - Execution evidence
      - Related files

  test-short:
    ordered_fields:
      - "@file"
      - "@contract"
      - "@status"
      - "@provenance"
```

The linter should report deterministic structural errors and preserve unknown values rather than inventing semantic conclusions.
