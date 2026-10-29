import time
import uuid
import hashlib
import random
from typing import List, Optional, Dict
import json

from core.transaction_contract import (
    block_has_unique_transaction_ids,
    valid_transaction_shape,
)

GOOGLPLEX = 10**100

# ==================== WALLET CLASS ====================
class Wallet:
    def __init__(self, wallet_id: str, is_master: bool = False, parent: Optional['Wallet'] = None):
        self.wallet_id = wallet_id
        self.is_master = is_master
        self.master_count = 1.0
        self.children: List[Wallet] = []
        self.parent = parent
        self.creation_time = time.time()
        self.lifetime = 3600 * 24 * 30
        self.self_destruct_triggers: List[int] = []
        self.invited_wallets: dict = {}
        self.is_publicly_paid = False
        self.origin_hash = wallet_id
        self.cooldown_end = 0.0
        self.provence_chain = []
        self.fifo_work_owed = []

        self.hdd_share_bytes = 0.0
        self.cpu_cycles = 0.0
        self.memory_mb = 0.0
        self.shared_hdd: Dict[str, float] = {}
        self.shared_cpu: Dict[str, float] = {}
        self.shared_memory: Dict[str, float] = {}

    def share_resource(self, peer_id: str, resource_type: str, amount: float):
        if resource_type == "hdd":
            self.shared_hdd[peer_id] = amount
            self.hdd_share_bytes += amount
        elif resource_type == "cpu":
            self.shared_cpu[peer_id] = amount
            self.cpu_cycles += amount
        elif resource_type == "memory":
            self.shared_memory[peer_id] = amount
            self.memory_mb += amount

    def add_child(self, child_wallet):
        self.children.append(child_wallet)
        child_wallet.parent = self
        self.aggregate_resources()

    def aggregate_resources(self):
        total_hdd = self.hdd_share_bytes
        total_cpu = self.cpu_cycles
        total_mem = self.memory_mb
        for child in self.children:
            child.aggregate_resources()
            total_hdd += child.hdd_share_bytes
            total_cpu += child.cpu_cycles
            total_mem += child.memory_mb
        self.master_count = total_hdd + total_cpu + total_mem
        return total_hdd, total_cpu, total_mem

    def mark_publicly_paid(self):
        self.is_publicly_paid = True
        self.provence_chain.append({"time": time.time(), "action": "publicly_paid", "delta": 0, "shared_resources": {
            "hdd": self.hdd_share_bytes / GOOGLPLEX,
            "cpu": self.cpu_cycles / GOOGLPLEX,
            "memory": self.memory_mb / GOOGLPLEX
        }})

    def add_work_owed(self, amount, creditor):
        self.fifo_work_owed.append({"amount": amount, "creditor": creditor, "time": time.time()})

    def process_reciprocal_repayment(self):
        for owed in self.fifo_work_owed[:]:
            if time.time() > owed["time"] + 86400:
                repayment = owed["amount"] * 0.15
                owed["creditor"].master_count += repayment
                self.master_count -= repayment
                self.fifo_work_owed.remove(owed)

    def can_access(self, requester_id):
        if self.self_destruct_triggers and time.time() > max(self.self_destruct_triggers):
            return requester_id in self.invited_wallets and self.invited_wallets[requester_id]
        return True

    def self_destruct(self):
        self.self_destruct_triggers.append(time.time())

    def announce_to_dht(self, resource_type: str):
        print(f"[{self.wallet_id}] Announcing {resource_type} share to Kademlia DHT + BitTorrent")

    def discover_peers(self, resource_type: str):
        print(f"[{self.wallet_id}] Discovering peers with {resource_type} via DHT + BitTorrent")

    def create_ppm_transaction(self, direction: str, resource_type: str = "hdd"):
        """Create a transaction with a unique UUID identity."""
        ppm = self.calculate_real_time_ppm()
        tx = {
            "transaction_id": str(uuid.uuid4()),
            "wallet_id": self.wallet_id,
            "direction": direction,
            "resource_type": resource_type,
            "ppm": ppm,
            "amount": 1,
            "timestamp": time.time()
        }
        return tx

    def calculate_real_time_ppm(self):
        """Real-time PPM pricing: base + resource factor (HDD + CPU + Memory)"""
        base_ppm = self.master_count * 0.5
        resource_factor = (
            (self.hdd_share_bytes / GOOGLPLEX) +
            (self.cpu_cycles / GOOGLPLEX) +
            (self.memory_mb / GOOGLPLEX)
        )
        return base_ppm * resource_factor

# ==================== HELPERS ====================
def daily_work_recalculation(wallet, network_data):
    work_list = []
    for w in network_data["all_wallets"]:
        total_shared = w.hdd_share_bytes + w.cpu_cycles + w.memory_mb
        work_list.append((total_shared * 0.05, True))   # donate 5%
        work_list.append((total_shared * 0.90, False))  # keep 90%

    sorted_work = sorted(work_list, key=lambda x: x[0])
    percentile_start = int(len(sorted_work) * 0.05)
    percentile_end = int(len(sorted_work) * 0.95)
    band_work = sum(w[0] for w in sorted_work[percentile_start:percentile_end])

    total_res = wallet.hdd_share_bytes + wallet.cpu_cycles + wallet.memory_mb
    if total_res * 0.05 not in [w[0] for w in sorted_work[percentile_start:percentile_end + 1]]:
        wallet.master_count = band_work * 0.05

    wallet.process_reciprocal_repayment()


def validate_bit_transaction(tx: Dict, wallets: Dict[str, Wallet]) -> bool:
    """Validate required transaction fields against registered wallet state."""
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

    if tx["amount"] <= 0 or tx["timestamp"] <= 0 or tx["ppm"] < 0:
        return False

    try:
        expected_ppm = wallet.calculate_real_time_ppm()
    except (ArithmeticError, TypeError, ValueError, AttributeError, OverflowError):
        return False

    if (
        isinstance(expected_ppm, bool)
        or not isinstance(expected_ppm, (int, float))
        or not math.isfinite(expected_ppm)
        or expected_ppm < 0
    ):
        return False

    return tx["ppm"] == expected_ppm


def process_block(block: Dict, wallets: Dict[str, Wallet]):
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


def validate_block(block: Dict, wallets: Dict[str, Wallet]) -> bool:
    if not isinstance(block, dict):
        return False
    transactions = block.get("transactions")
    if not isinstance(transactions, list) or not transactions:
        return False
    if not block_has_unique_transaction_ids(transactions):
        return False

    for tx in transactions:
        if not isinstance(tx, dict) or not validate_bit_transaction(tx, wallets):
            return False
    return True


def on_max_retention_reached(data_hash):
    pass


def apply_publicly_paid_label(wallet):
    wallet.mark_publicly_paid()
    print(f"Publicly Paid label activated with shared resources: "
          f"HDD={wallet.hdd_share_bytes/GOOGLPLEX:.2f}GB, "
          f"CPU={wallet.cpu_cycles/GOOGLPLEX:.2f}Gcycles, "
          f"Memory={wallet.memory_mb/GOOGLPLEX:.2f}GB")


# ==================== DEMO ====================
def main():
    print("Crowd-Cloud System starting...")
    network_wallets = []

    root = Wallet("root_master")
    root.hdd_share_bytes = 100 * GOOGLPLEX
    root.cpu_cycles = 500 * GOOGLPLEX
    root.memory_mb = 200 * GOOGLPLEX

    peer1 = Wallet("peer1")
    peer2 = Wallet("peer2")
    root.add_child(peer1)
    root.add_child(peer2)

    root.share_resource("peer1", "hdd", 50 * GOOGLPLEX)
    root.share_resource("peer1", "cpu", 100 * GOOGLPLEX)
    root.share_resource("peer2", "memory", 50 * GOOGLPLEX)

    # Real-time PPM transaction (the fix!)
    root_tx = root.create_ppm_transaction("enter", "hdd")
    print(f"Real-time PPM transaction created: {root_tx}")

    daily_work_recalculation(root, {"all_wallets": [root, peer1, peer2]})

    root.announce_to_dht("hdd")
    root.discover_peers("cpu")

    on_max_retention_reached("novel_data_hash")
    apply_publicly_paid_label(root)

    block = {"transactions": [root_tx], "header": ""}
    wallet_index = {w.wallet_id: w for w in [root, peer1, peer2]}
    hash_val = process_block(block, wallet_index)
    print(f"Block mined: {hash_val}")

    print(f"Shared HDD: {root.hdd_share_bytes / GOOGLPLEX:.2f} GB")
    print(f"Shared CPU: {root.cpu_cycles / GOOGLPLEX:.2f} Gcycles")
    print(f"Shared Memory: {root.memory_mb / GOOGLPLEX:.2f} GB")


if __name__ == "__main__":
    main()
