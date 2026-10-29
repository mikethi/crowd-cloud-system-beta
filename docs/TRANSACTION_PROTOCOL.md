# Transaction Protocol — Design and Qualification

Status: proposed; not yet implemented or approved as a protocol specification.

## Goals

1. Define an exact transaction schema.
2. Give transactions stable identities and define duplicate/replay handling.
3. Specify how transaction amounts correspond to wallet resource changes.
4. Keep transaction validation deterministic and consistent across validation,
   block processing, and pseudocode/reference implementations.

## Current verified baseline

The baseline commit is `d661275`. The current test suite includes tests that
document known gaps: extra transaction fields are accepted, repeated identical
transactions are not rejected by block validation, the amount is not tied to
the wallet resource delta, and transactions lack an explicit nonce or ID.

These are known limitations, not approved protocol behavior.

## Proposed validation requirements

- Reject missing required fields.
- Reject unexpected fields once the canonical schema is approved.
- Reject invalid types, booleans where numeric values are required, and
  non-finite numeric values.
- Use one canonical serialization and hashing contract.
- Define a stable transaction identity and duplicate detection scope.
- Validate all transactions before applying any wallet/resource mutation.
- Ensure invalid blocks cannot partially mutate state.
- Keep all implementations and reference pseudocode behavior aligned.

## Not yet specified

The protocol must explicitly choose the transaction fields, identity format,
nonce scope, replay window, sender/owner authority, resource units, debit/credit
semantics, rounding rules, and the point at which changes become final.

No production implementation should infer these choices from field names alone.
