# Beta Implementation Roadmap

## Phase 0 — baseline

- Preserve the upstream repository and baseline commit.
- Run and record existing tests.
- Keep the original project unchanged.

## Phase 1 — transaction integrity

- Inspect wallet, transaction, block, and pseudocode contracts.
- Agree on transaction schema and accounting semantics.
- Add failing tests before implementation.
- Implement schema, identity/replay protection, and atomic accounting.
- Run the full regression suite.

## Phase 2 — code manifest and shards

- Define manifest schema and versioning.
- Select replication or erasure coding.
- Add corruption, incompleteness, and unauthorized-version tests.

## Phase 3 — reconstitution

- Define checkpoint and replay rules.
- Implement code and state recovery as separate verified steps.
- Test interruption, missing peers, duplicate replay, and conflicting snapshots.

## Phase 4 — consensus integration

- Specify finality and partition behavior.
- Gate execution on authoritative state.
- Test restart and recovery against the selected consensus protocol.

## Phase 5 — adversarial and operational qualification

- Test resource exhaustion and malformed peer inputs.
- Test backup/recovery and contributor withdrawal.
- Conduct independent security review before production claims.

Each phase needs explicit acceptance criteria and recorded test evidence.
