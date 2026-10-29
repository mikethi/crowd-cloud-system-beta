# Reconstitution and Continuity

Status: design proposal.

## Recovery sequence

1. Discover reachable peers and available state/code records.
2. Obtain an authorized code manifest and consensus checkpoint.
3. Retrieve enough shard data under the selected coding scheme.
4. Verify shard identities, hashes, versions, and reconstruction metadata.
5. Reconstruct code and verify the result against the manifest.
6. Recover the checkpoint state and replay subsequent finalized transitions.
7. Reconcile pending transactions and prevent duplicate application.
8. Check execution compatibility and resource capacity.
9. Rejoin consensus and resume execution only when protocol conditions permit.

## Recovery invariants

- Recovery cannot authorize unapproved code.
- A peer cannot finalize conflicting histories merely because it restarted.
- Applying the same finalized transaction twice must not duplicate its effects.
- Incomplete or inconsistent recovery fails closed.
- Reconstructed state must match the protocol's authoritative history.
- Recovery operations must be bounded to resist resource-exhaustion attacks.

## Unresolved design choices

The project must decide whether code is stored as erasure-coded fragments,
replicated segments, or a hybrid. It must specify thresholds, failure domains,
checkpoint authorization, retention policy, and behavior during network
partitions.

Reconstitution improves recoverability; it cannot guarantee recovery if all
required data, resources, or communication paths are lost.
