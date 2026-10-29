"""Canonical transaction shape and block-level identity checks.

Duplicate detection is scoped to one block. Durable replay protection
requires persisted finalized state.
"""
import uuid

TRANSACTION_FIELDS = frozenset({
    "transaction_id", "wallet_id", "direction", "resource_type",
    "amount", "ppm", "timestamp",
})


def valid_transaction_shape(tx):
    if not isinstance(tx, dict) or set(tx) != TRANSACTION_FIELDS:
        return False
    transaction_id = tx.get("transaction_id")
    if not isinstance(transaction_id, str):
        return False
    try:
        parsed = uuid.UUID(transaction_id)
    except (ValueError, AttributeError, TypeError):
        return False
    return str(parsed) == transaction_id


def block_has_unique_transaction_ids(transactions):
    seen = set()
    for tx in transactions:
        if not valid_transaction_shape(tx):
            return False
        transaction_id = tx["transaction_id"]
        if transaction_id in seen:
            return False
        seen.add(transaction_id)
    return True
