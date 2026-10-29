# Crowd-Cloud Beta Architecture

Status: proposed architecture. This document is not proof that the design
has been implemented or validated.

## Core model

Crowd-Cloud is intended to be a resource-funded, peer-coordinated execution
system. The chain represents the authoritative history of accepted state
transitions. Live execution proposes changes; the consensus protocol determines
which changes become authoritative.

Pooled resources support code storage, state retention, verification,
reconstitution, and live computation.

## Logical components

1. Resource pool: tracks contributed and available CPU, memory, storage,
   network capacity, and any protocol-defined resource credits.
2. Code registry: identifies approved code versions and their manifests.
3. Shard storage: retains cryptographically verifiable code fragments and
   the metadata required to reconstruct them.
4. State history: records accepted transitions, transaction identities,
   execution versions, and consensus evidence.
5. Consensus: determines authoritative ordering and finality.
6. Reconstitution: recovers verified code and state after interruption.
7. Execution engine: evaluates accepted protocol rules and proposes
   deterministic state transitions.
8. Accounting: tracks contributions, allocations, consumption, and balances.

These are logical boundaries. They need not be separate services or processes.

## Governing invariant

Execution may stop and restart. A restarted peer must not invent a new history
or unilaterally choose its local state as authoritative. It must recover
verified data and follow consensus.

## Separation of concerns

- Code availability is not code authorization.
- A valid code hash is not proof that the code is safe.
- Resource credits are not proof that resources were delivered.
- A local execution result is not final until accepted under consensus.
- A snapshot accelerates recovery but must be authenticated and reconciled
  against authoritative history.
