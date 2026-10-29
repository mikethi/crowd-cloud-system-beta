# core/pseudocode.py
import time
import hashlib
import random

from core.transaction_contract import (
    block_has_unique_transaction_ids,
    valid_transaction_shape,
)

GOOGLPLEX = 10**100
DUPLICATE_SMOOTH = 0.1
MAX_DUPLICATE_COST = 50.0
MIN_DUPLICATE_COST = 0.1

def daily_work_recalculation(wallet, network_data):
    work_list = []
    for w in network_data["all_wallets"]:
        work_list.append((w.master_count * 0.05, True))
        work_list.append((w.master_count * 0.90, False))
    work_list.append((wallet.master_count * 0.05, True))

    sorted_work = sorted(work_list, key=lambda x: x[0])
    total_work = sum(w[0] for w in work_list)
    percentile_start = int(len(sorted_work) * 0.05)
    percentile_end = int(len(sorted_work) * 0.95)
    band_work = sum(w[0] for w in sorted_work[percentile_start:percentile_end])

    if wallet.master_count * 0.05 not in [w[0] for w in sorted_work[percentile_start:percentile_end + 1]]:
        wallet.master_count = band_work * 0.05

    wallet.process_reciprocal_repayment()




def on_max_retention_reached(data_hash):
    pass

def apply_publicly_paid_label(wallet):
    wallet.mark_publicly_paid()

# === NEW: Resource sharing & PPM ===
def calculate_resource_ppm(wallet, hdd_share, cpu_cycles, mem_mb):
    """PPM now includes resource contributions (storage + cycles + memory)"""
    base_ppm = wallet.master_count * 0.5
    resource_factor = (hdd_share / GOOGLPLEX) + (cpu_cycles / GOOGLPLEX) + (mem_mb / GOOGLPLEX)
    return base_ppm * resource_factor

def daily_work_recalculation(wallet, network_data):
    """5% donation mode + resource sharing + 15% repayment"""
    # Collect shared resources for percentile calculation
    work_list = []
    for w in network_data["all_wallets"]:
        total_shared = w.hdd_share_bytes + w.cpu_cycles + w.memory_mb
        work_list.append((total_shared * 0.05, True))      # 5% donation
        work_list.append((total_shared * 0.90, False))     # 90% network covered

    sorted_work = sorted(work_list, key=lambda x: x[0])
    percentile_start = int(len(sorted_work) * 0.05)
    percentile_end = int(len(sorted_work) * 0.95)
    band_work = sum(w[0] for w in sorted_work[percentile_start:percentile_end])

    if wallet.hdd_share_bytes + wallet.cpu_cycles + wallet.memory_mb * 0.05 not in [w[0] for w in sorted_work[percentile_start:percentile_end + 1]]:
        wallet.master_count = band_work * 0.05

    wallet.process_reciprocal_repayment()




def on_max_retention_reached(data_hash):
    pass

def apply_publicly_paid_label(wallet):
    wallet.mark_publicly_paid()

GOOGLPLEX = 10**100

def calculate_resource_ppm(wallet, hdd_share, cpu_cycles, mem_mb):
    base_ppm = wallet.master_count * 0.5
    resource_factor = (hdd_share / GOOGLPLEX) + (cpu_cycles / GOOGLPLEX) + (mem_mb / GOOGLPLEX)
    return base_ppm * resource_factor

def daily_work_recalculation(wallet, network_data):
    work_list = []
    for w in network_data["all_wallets"]:
        total_shared = w.hdd_share_bytes + w.cpu_cycles + w.memory_mb
        work_list.append((total_shared * 0.05, True))
        work_list.append((total_shared * 0.90, False))

    sorted_work = sorted(work_list, key=lambda x: x[0])
    percentile_start = int(len(sorted_work) * 0.05)
    percentile_end = int(len(sorted_work) * 0.95)
    band_work = sum(w[0] for w in sorted_work[percentile_start:percentile_end])

    total_res = wallet.hdd_share_bytes + wallet.cpu_cycles + wallet.memory_mb
    if total_res * 0.05 not in [w[0] for w in sorted_work[percentile_start:percentile_end + 1]]:
        wallet.master_count = band_work * 0.05

    wallet.process_reciprocal_repayment()




def on_max_retention_reached(data_hash):
    pass

def apply_publicly_paid_label(wallet):
    wallet.mark_publicly_paid()
    print(f"Publicly Paid label activated with shared resources: HDD={wallet.hdd_share_bytes/GOOGLPLEX:.2f}GB, CPU={wallet.cpu_cycles/GOOGLPLEX:.2f}Gcycles, Memory={wallet.memory_mb/GOOGLPLEX:.2f}GB")

# === New: Auto-replication + DHT stubs ===
def auto_replicate_data(wallet, data_hash):
    """6x replication using shared resources"""
    print(f"[{wallet.wallet_id}] Auto-replicating data {data_hash} 6x using shared HDD/CPU")
    # DHT announce + BitTorrent seed + resource check


def validate_bit_transaction(tx, wallets=None):
    """Validate a transaction against authoritative registered wallet state."""
    import math

    if not valid_transaction_shape(tx) or not isinstance(wallets, dict):
        return False

    wallet_id = tx.get("wallet_id")
    if not isinstance(wallet_id, str) or not wallet_id:
        return False
    wallet = wallets.get(wallet_id)
    if wallet is None or getattr(wallet, "wallet_id", None) != wallet_id:
        return False

    if tx.get("direction") not in ("enter", "exit"):
        return False
    if tx.get("resource_type") not in ("hdd", "cpu", "memory"):
        return False

    for key in ("amount", "ppm", "timestamp"):
        value = tx.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False
        if not math.isfinite(value):
            return False

    if tx["amount"] <= 0 or tx["ppm"] < 0 or tx["timestamp"] <= 0:
        return False

    try:
        expected_ppm = wallet.calculate_real_time_ppm()
    except (ArithmeticError, TypeError, ValueError, AttributeError):
        return False

    if (
        isinstance(expected_ppm, bool)
        or not isinstance(expected_ppm, (int, float))
        or not math.isfinite(expected_ppm)
        or expected_ppm < 0
    ):
        return False

    # PPM is derived from the currently registered wallet state.
    # Require a strict numeric match at the precision represented by
    # the transaction; a broad relative tolerance hides small absolute
    # edits when expected_ppm is extremely large.
    return tx["ppm"] == expected_ppm



def process_block(block, wallets=None):
    """Validate and deterministically hash a block; this is not mining."""
    import hashlib
    import json

    if not validate_block(block, wallets):
        raise ValueError("Invalid block")

    try:
        encoded = json.dumps(
            block,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Block is not deterministically JSON-serializable"
        ) from exc

    return hashlib.sha256(encoded).hexdigest()



def validate_block(block, wallets=None):
    """Reject malformed or empty blocks and validate each transaction."""
    if not isinstance(block, dict) or not isinstance(wallets, dict):
        return False

    transactions = block.get("transactions")
    if not isinstance(transactions, list) or not transactions:
        return False
    if not block_has_unique_transaction_ids(transactions):
        return False

    return all(
        validate_bit_transaction(tx, wallets)
        for tx in transactions
    )


def apply_publicly_paid_label(wallet):
    wallet.mark_publicly_paid()
    print(f"Publicly Paid label activated with shared resources: "
          f"HDD={wallet.hdd_share_bytes/GOOGLPLEX:.2f}GB, "
          f"CPU={wallet.cpu_cycles/GOOGLPLEX:.2f}Gcycles, "
          f"Memory={wallet.memory_mb/GOOGLPLEX:.2f}GB")
