# Architecture and Component Responsibilities

## Overview

Crowd-Cloud System coordinates contributed computing resources and records Bitcoin-pegged accounting records.

## Core Components

### `models/pricing.py`
Implements authoritative Bitcoin Satoshi conversion rates for storage, CPU, and memory contributions with strict numeric validation.

### `models/wallet.py`
Manages wallet records and balances denominated in Satoshis.
