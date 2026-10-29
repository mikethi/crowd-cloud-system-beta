# Crowd-Cloud System

Crowd-Cloud System is a development-stage project exploring coordination of computing resources contributed by multiple participants.

Intended resource categories include storage, CPU capacity, and memory. The repository contains wallet-related logic, **Bitcoin-pegged satoshi accounting** via `models/pricing.py`, **decentralized chain-sharding & live code reconstitution** via `core/chain_shards.py`, transaction and block-processing logic, and storage-related functionality.

**Status:** Development and verification in progress. This documentation does not claim production readiness.

Repository: https://github.com/mikethi/crowd-cloud-system

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Proposed API integration](docs/API.md)
- [Testing and verification](docs/TESTING.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Documentation index](docs/README.md)

## Decentralized Sharding & Live Reconstitution

The system splits core application code into cryptographic shards stored directly on the simulated chain state. Once the redundancy threshold is met, the code is dynamically verified and reconstituted for live execution.

## Repository layout

```text
crowd-cloud-system/
├── main.py
├── models/
│   ├── wallet.py
│   └── pricing.py
├── core/
│   ├── pseudocode.py
│   └── chain_shards.py
├── data/storage.py
├── docs/
│   ├── README.md
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── TESTING.md
├── SECURITY.md
├── CONTRIBUTING.md
└── README.md
```
