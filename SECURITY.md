# Security Policy

## Decentralized Code Integrity

Code fragments stored on-chain via `core/chain_shards.py` are cryptographically checksummed using SHA-256. Reconstitution requires meeting a strict redundancy threshold and passing integrity verification before live execution.
