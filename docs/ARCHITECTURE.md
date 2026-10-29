# Architecture and Component Responsibilities

## Overview

Crowd-Cloud System explores coordinating contributed computing resources and recording contribution-related accounting information.

This document combines current source-file responsibilities with recommended separation of concerns. Proposed components must not be assumed to exist until implemented and tested.

## Current repository components

### `main.py`
Application entry point and orchestration. Runtime integration and behavior require automated tests.

### `models/wallet.py`
Wallet-associated records, resource-sharing logic, and PPM calculation in the fuller workspace implementation. This layer should maintain consistent accounting state but cannot independently prove resources were delivered.

### `core/pseudocode.py`
Transaction validation and block-processing logic. An earlier version had a permissive validator. Verify that strict validation is invoked by the real application path and that failures prevent persistence and accounting updates.

### `data/storage.py`
Storage-related implementation. The repository's `.gitignore` currently ignores `data/*`, so this file may not be tracked.

## Recommended logical layers

1. API/transport: parse requests and return documented responses.
2. Authentication: identify callers.
3. Authorization: enforce access to participants, wallets, and records.
4. Application services: coordinate contribution workflows.
5. Domain logic: enforce resource and accounting invariants.
6. Verification agents: measure delivered resources or completed work.
7. Persistence: save records atomically and consistently.
8. Audit and observability: record relevant events without exposing secrets.

The same domain validation should be used regardless of whether a request comes from an API or an internal application call.

## Intended contribution flow

1. Authenticate and authorize the participant.
2. Validate the requested resource and unit.
3. Verify resource availability or completed work.
4. Create a unique contribution record.
5. Calculate PPM using a versioned formula.
6. Validate the transaction.
7. Persist the contribution and accounting update atomically.
8. Record an audit event.
9. Reconcile accounting against verified activity.

## Transaction and block integrity

Define a canonical schema and stable serialization format before using transaction hashes as identifiers.

A hash of `str(block)` is not a canonical serialization specification. Hashing alone does not establish transaction validity, participant identity, consensus, or immutability.

## Resource types

### Storage
Define capacity units, allocation and release behavior, quotas, and verification.

### CPU
Define the workload metric, execution limits, and how completed work is measured.

### Memory
Distinguish reserved capacity from actual consumption and define the accounting metric.

Do not treat bytes, CPU cycles, and megabytes as interchangeable units without explicit normalization.

## PPM accounting

Document the formula, constants, weights, bounds, precision, rounding, and formula version. Calculate authoritative PPM values from trusted, validated measurements.

## Failure handling

A production design should define atomicity, retries, idempotency, duplicate detection, rollback behavior, and recovery after process or storage failures.

## Current limitations

The recorded checks do not establish end-to-end correctness, a production API, distributed consensus, secure workload isolation, or production readiness. See [TESTING.md](TESTING.md) and [`../SECURITY.md`](../SECURITY.md).
