# Open Protocol Decisions

These decisions require an explicit project-owner answer or an existing,
authoritative specification. Do not silently choose defaults in implementation.

## Transaction schema

- What exact fields are required and allowed?
- What are the canonical types and bounds for each field?
- Are unknown fields rejected immediately, or is a versioned migration needed?
- Which schema/version identifier is part of the signed or hashed payload?

## Identity and replay

- Is transaction identity a supplied ID, a sender-scoped nonce, or a hash?
- What authenticates the sender or wallet owner?
- Is uniqueness enforced per sender, block, epoch, or entire chain?
- How are retries, reorgs, and already-finalized transactions handled?
- Is the same transaction allowed to appear in separate candidate blocks?

## Resource accounting

- Which resource types are spendable, and what are their units?
- Does a positive amount mean debit, credit, contribution, or transfer?
- Which wallet/resource field must change for each transaction type?
- How are fees, PPM, rounding, precision, and conversion handled?
- What prevents spending more than the available resource balance?
- Is resource state derived from finalized transactions or directly mutated?

## State transitions and authority

- What is the authoritative finality source?
- When may validated transactions mutate state?
- What is the rollback/recovery rule if persistence fails?
- Must validation be deterministic across all supported runtimes?

## Release and compatibility

- Which existing clients or stored blocks must remain compatible?
- Is a protocol version bump required?
- What test vectors or known-good blocks define compatibility?
