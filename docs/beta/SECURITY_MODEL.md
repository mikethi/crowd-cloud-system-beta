# Beta Security Model

Status: initial threat model; not a security audit.

## Assets

- Authoritative chain history and finalized state.
- Approved code manifests and reconstructed executable code.
- Contributor accounts and resource accounting.
- Transaction identity, authorization, and replay protection.
- Consensus safety and peer membership.
- Shard availability, integrity, and recovery metadata.

## Threats

- Malicious or corrupted code shards.
- Unauthorized manifest or protocol changes.
- Duplicate transactions and replay.
- Forged resource contributions or inconsistent accounting.
- Conflicting histories during network partitions.
- Partial state mutation following failed validation.
- Malicious peers, malformed payloads, and resource exhaustion.
- A compromised execution peer claiming unverified results.

## Required controls

- Canonical hashing and strict schema validation.
- Explicit transaction identity and replay rules.
- Authorized code-version changes.
- Shard integrity checks and final reconstructed-code verification.
- Authenticated checkpoints and deterministic state replay.
- Validate-before-apply and atomic state transitions.
- Consensus-defined finality and partition recovery.
- Resource quotas, bounded inputs, and recovery limits.
- Independent verification by peers where the consensus design requires it.

## Limits

Cryptographic integrity alone does not prove code is benign. Replication alone
does not guarantee availability. A running process is not proof of consensus.
Production readiness requires protocol analysis, adversarial tests, operational
recovery testing, and independent security review.
