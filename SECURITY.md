# Security Policy

## Status

Crowd-Cloud System is under development. The recorded checks do not establish production readiness or completion of an independent security assessment.

## Reporting a vulnerability

Do not publish access tokens, private keys, passwords, personal data, or exploitable production details in a public issue.

Use a private reporting channel available to the repository owner. If none is configured, contact the maintainer through an established private channel before disclosing sensitive details.

Include the affected commit, reproduction steps, expected and observed behavior, impact, prerequisites, and redacted logs. Never include real credentials or another participant's private data.

## Authentication and authorization

- Authenticate callers before protected operations.
- Authorize every wallet, participant, transaction, and resource lookup.
- Apply least privilege to service and database credentials.
- Rotate credentials and revoke compromised tokens.
- Never treat possession of a wallet identifier as authorization.

## Input validation

- Validate data at every trust boundary.
- Reject malformed structures and unsupported resource types.
- Enforce numeric bounds and finite-number checks.
- Validate timestamps and transaction identifiers.
- Fail closed when required validation cannot complete.

## Accounting integrity

- Calculate authoritative PPM values on the trusted side.
- Define units, normalization, rounding, and formula versions.
- Prevent duplicate and replayed contribution requests.
- Apply accounting and persistence updates atomically.
- Reconcile declared resources against independently verified activity.

## Resource isolation

If participant workloads are executed, isolate untrusted code from the main application and other participants. Enforce CPU, memory, storage, network, time, and concurrency limits.

## Storage and logging

- Restrict access to stored records.
- Use atomic writes or database transactions.
- Protect backups and define recovery procedures.
- Never log passwords, tokens, private keys, or unnecessary personal information.
- Define retention and deletion rules.

## API security

Before exposing an API, test authentication failures, authorization boundaries, malformed input, request-size limits, rate limiting, replay protection, error leakage, and relevant injection risks.

## Supply-chain security

Pin dependencies where practical, review updates, maintain a dependency manifest, and run suitable dependency and static-analysis tools. Protect CI credentials and review workflow permissions.

## Verification status

Recorded checks include syntax checks for selected modules, Git whitespace checks, a limited credential-pattern scan, and successful publication.

Earlier isolated validation tests reported 22/22 negative cases and 6/6 block-validation cases passing. They did not prove the tested strict validator was used by the running application.

These results are not a penetration test, a complete secret scan, or a security certification.

## Before production

Do not deploy as a public service until authentication, authorization, API contracts, accounting invariants, persistence, workload isolation, dependency scanning, concurrency, recovery, monitoring, and incident response have been implemented and tested.
