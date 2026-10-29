# Open Beta Decisions

These decisions must be resolved before the corresponding implementation is
considered complete. Do not silently invent protocol semantics.

## Code and shards

- Are shards erasure-coded fragments, replicated code segments, or hybrid?
- What reconstruction threshold and failure-domain policy apply?
- Who may authorize a code manifest or version upgrade?
- Which execution environments and deterministic runtime rules are supported?

## Consensus and recovery

- What consensus/finality protocol is authoritative?
- How are membership and peer identity established?
- What happens when the network partitions?
- How are checkpoints authenticated and reconciled?
- Which pending transactions survive a restart?

## Resource economics

- Which resources are measured, and in what units?
- How is contributed capacity verified?
- How are credits earned, reserved, spent, and reconciled?
- What prevents overcommitment and resource-exhaustion attacks?
- How may a contributor withdraw without corrupting active state?

## Transaction semantics

- What fields define each transaction type?
- What authorizes a wallet or resource change?
- What is the transaction ID/nonce scope?
- How are fees, rounding, and insufficient resources handled?

## Governance and upgrades

- Who can propose an upgrade?
- What consensus threshold accepts it?
- How are incompatible upgrades and rollbacks handled?
- What is the emergency response when a release is unsafe?
