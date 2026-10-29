# Crowd-Cloud System

Crowd-Cloud System is a development-stage project exploring coordination of computing resources contributed by multiple participants.

Intended resource categories include storage, CPU capacity, and memory. The repository contains wallet-related logic, **Bitcoin-pegged satoshi accounting** via `models/pricing.py`, transaction and block-processing logic, and storage-related functionality.

**Status:** Development and verification in progress. This documentation does not claim production readiness.

Repository: https://github.com/mikethi/crowd-cloud-system

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Proposed API integration](docs/API.md)
- [Testing and verification](docs/TESTING.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Documentation index](docs/README.md)

## Bitcoin Pegged Accounting

Contributions are valued in Bitcoin Satoshis on the trusted server side using `models/pricing.py`:
- Storage bytes -> Satoshis
- CPU cycles -> Satoshis
- Memory megabytes -> Satoshis

All inputs undergo strict finite-number and non-negative boundary validation.

## Repository layout

```text
crowd-cloud-system/
├── main.py
├── models/
│   ├── wallet.py
│   └── pricing.py
├── core/pseudocode.py
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
