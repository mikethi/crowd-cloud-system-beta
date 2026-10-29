# Transaction Integrity

Status: planned work, not yet implemented by this document.

## Required workstreams

### 1. Strict schema

Define required and permitted fields, types, numeric bounds, schema version,
and canonical serialization. Reject unknown fields under the approved version.

### 2. Identity and replay

Define transaction identity, sender authorization, nonce scope, duplicate
detection, retry behavior, and handling across blocks and recovery.

### 3. Resource accounting

Specify how each transaction maps to resource debits and credits. Define units,
rounding, fees, insufficient-resource behavior, and authorization. Credits
must not be treated as evidence of physical resource delivery.

### 4. Regression coverage

Test malformed fields, duplicate IDs, replay, amount/resource mismatches,
insufficient resources, atomic failure, recovery replay, and parity between
validation and block-processing paths.

## State-transition rule

Validate the entire proposed transition before applying mutations. Commit
effects atomically under the system's authoritative consensus rules.
