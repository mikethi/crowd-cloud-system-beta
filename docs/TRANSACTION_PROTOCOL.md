# Transaction Protocol — Design and Qualification

Status: partially implemented; this document records verified behavior and
remaining protocol decisions. It is not an approved production specification.

## Goals

1. Define an exact transaction schema.
2. Give transactions stable identities and define duplicate handling.
3. Specify how transaction amounts correspond to wallet resource changes.
4. Keep validation, block processing, and reference pseudocode consistent.

## Current verified baseline

Commit `b079db2` adds a shared transaction contract used by block-processing
and reference-pseudocode paths.

Each transaction must contain exactly these fields:

- `transaction_id`
- `wallet_id`
- `direction`
- `resource_type`
- `amount`
- `ppm`
- `timestamp`

`transaction_id` must be a canonical UUID string. Missing or unexpected fields
are rejected, and duplicate transaction IDs within a single block are rejected.

Both processing paths serialize the complete block using sorted JSON keys,
compact separators, UTF-8 encoding, `ensure_ascii=False`, and `allow_nan=False`,
then calculate a SHA-256 hash of those bytes. Tests cover schema validation,
identity changes affecting the block hash, duplicate rejection, and consistency
between the processing paths.

## Guarantees and limitations

- Duplicate detection is scoped to an individual block; durable replay
  protection across finalized blocks is not implemented.
- The transaction `amount` is not yet bound to a corresponding wallet resource
  delta.
- A canonical UUID format does not, by itself, establish transaction ownership,
  authorization, or replay protection.
- Passing tests establishes only the tested behavior, not production readiness.

## Remaining protocol decisions

The protocol still needs to specify nonce or replay scope, sender/owner authority,
resource units, debit/credit semantics, rounding, finality, and how transaction
amounts relate to resource changes. State-mutation atomicity and validation
ordering also require explicit verification before production claims are made.

Do not infer these guarantees from field names or successful unit tests alone.
