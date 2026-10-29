# Contributing

Thank you for helping improve Crowd-Cloud System.

## Before making a change

1. Read `README.md`, `SECURITY.md`, and relevant design documents.
2. Inspect the current branch and working tree.
3. Confirm expected behavior and assumptions.
4. Avoid modifying unrelated files.

```bash
git status --short
git log -5 --oneline
git diff
```

## Branching

Use a separate branch for significant changes:
```bash
git switch -c feature/short-description
```

## Code quality

- Keep business logic separate from transport and persistence layers.
- Validate untrusted input.
- Define units and bounds for accounting values.
- Reject non-finite numeric values.
- Avoid duplicate accounting operations.
- Use stable transaction schemas.
- Do not log credentials or private participant data.
- Document externally visible behavior and configuration changes.

## Tests

Include tests for normal operation, boundaries, malformed inputs, and failures.

```bash
python3 -m compileall -q main.py models core
git diff --check
```

These commands are not substitutes for unit and integration tests. Run the actual test suite once its dependencies and invocation are documented.

For accounting changes, test negative and very large values, NaN, infinity, unit mismatches, duplicate requests, rounding, and persistence failures.

For API changes, test authentication, authorization, malformed requests, idempotency, rate limiting, and error handling.

## Pull requests

Describe the problem, intended behavior, implementation, tests actually run, security and numerical considerations, documentation updates, and known limitations.

Do not claim tests passed if they were not run. Do not include credentials, private keys, real user data, or production database files.

## Generated and ignored files

Review `.gitignore` before adding generated files or data. The current rule `data/*` ignores files under `data/`. Do not force-add ignored files without reviewing their contents and the intended repository policy.

## Security issues

Follow the private reporting guidance in `SECURITY.md`. Do not publish exploitable details or secrets in a public issue.
