# Security Model and Review Checklist

Status: initial security notes; not a security audit or production-readiness claim.

## Assets to protect

- Wallet balances and resource contributions.
- Transaction and block integrity.
- Chain-authority decisions and finality.
- Placement metadata and replica/failure-domain assumptions.
- Deterministic state across nodes.

## Threats requiring explicit controls

- Duplicate transaction submission and replay.
- Unexpected transaction fields or ambiguous serialization.
- Non-finite numbers, booleans accepted as numbers, and invalid numeric ranges.
- Amounts that do not match the actual resource delta.
- Unauthorized wallet/resource changes.
- Partial state mutation when a block is rejected.
- Conflicting or unavailable authority snapshots.
- Divergent validation behavior between implementations.
- Malicious or malformed peer input and resource-exhaustion attempts.

## Required transaction safeguards

- Strict schema validation with bounded input sizes.
- Canonical serialization and hashing.
- Explicit transaction identity and replay policy.
- Authorization checks tied to the transaction origin.
- Resource accounting with documented units and deterministic arithmetic.
- Validate-before-apply and atomic state transitions.
- Duplicate detection at the protocol-defined scope.
- Consistent validation in all block-processing paths.
- Regression tests for invalid inputs and failure atomicity.

## Operational safeguards

- Never treat passing unit tests as proof of production security.
- Keep secrets and credentials out of logs and repository history.
- Review dependency updates and pin production dependencies appropriately.
- Log rejected transaction reasons without exposing secrets.
- Define backup, recovery, incident response, and audit-log retention.
- Do not claim consensus safety without testing the actual distributed protocol.

## Outstanding security questions

See `OPEN_QUESTIONS.md`. Until these are resolved, transaction integrity is
not qualified for production use.
