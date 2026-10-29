# Features and Roadmap

## Present in baseline `d661275`

- Adaptive placement module and placement regression tests.
- Chain authority contracts for finalized decisions and fail-closed handling.
- Canonical block hashing and transaction validation tests.
- Tests for validation without wallet mutation.
- Serialization parity tests.

## Transaction-integrity work planned

### 1. Strict transaction schema

Define allowed fields and exact types. Reject unknown fields after the schema
is agreed and compatibility implications are reviewed.

### 2. Identity and replay protection

Introduce an approved transaction ID or nonce scheme, duplicate detection, and
explicit replay rules. Define whether uniqueness is per sender, block, epoch,
or entire chain.

### 3. Resource-accounting consistency

Specify the mapping between transaction amounts and resource deltas. Define
units, direction, rounding, authorization, and insufficient-balance behavior.
Apply state changes atomically only after complete validation.

### 4. Regression coverage

Add tests for schema violations, duplicates, replay attempts, invalid resource
deltas, insufficient resources, atomic failure, and parity between validation
and block processing. Retain all existing tests as a regression baseline.

## Status

The four items above are requirements and planned work. This document does not
claim they are implemented by the baseline commit.
