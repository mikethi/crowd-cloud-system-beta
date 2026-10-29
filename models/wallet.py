# models/wallet.py
import time
import uuid
from typing import List, Optional

GOOGLPLEX = 10**100

class Wallet:

    def aggregate_master_count(self):
        total = self.master_count
        for child in self.children:
            total += child.aggregate_master_count()
        self.master_count = total
        return total









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

        # Resource sharing
        self.hdd_share_bytes = 0.0
        self.cpu_cycles = 0.0
        self.memory_mb = 0.0
        self.shared_hdd: Dict[str, float] = {}
        self.shared_cpu: Dict[str, float] = {}
        self.shared_memory: Dict[str, float] = {}

    def share_resource(self, peer_wallet_id: str, resource_type: str, amount: float):
        """Record one positive contribution per peer and resource type."""
        import math

        resource_maps = {
            "hdd": (self.shared_hdd, "hdd_share_bytes"),
            "cpu": (self.shared_cpu, "cpu_cycles"),
            "memory": (self.shared_memory, "memory_mb"),
        }
        if resource_type not in resource_maps:
            raise ValueError(f"Unsupported resource type: {resource_type!r}")
        if not isinstance(peer_wallet_id, str) or not peer_wallet_id:
            raise ValueError("peer_wallet_id must be a non-empty string")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("amount must be a finite positive number")
        if isinstance(amount, float) and not math.isfinite(amount):
            raise ValueError("amount must be finite")
        if amount <= 0:
            raise ValueError("amount must be greater than zero")

        peer_map, total_attribute = resource_maps[resource_type]
        if peer_wallet_id in peer_map:
            raise ValueError(
                f"Duplicate {resource_type} contribution from {peer_wallet_id!r}"
            )

        # Mutate state only after all validation has succeeded.
        peer_map[peer_wallet_id] = amount
        setattr(self, total_attribute, getattr(self, total_attribute) + amount)


    def add_child(self, child_wallet):
        self.children.append(child_wallet)
        child_wallet.parent = self
        self.aggregate_resources()

    def aggregate_resources(self):
        """Return this wallet's recursively aggregated resource totals."""
        total_hdd = self.hdd_share_bytes
        total_cpu = self.cpu_cycles
        total_mem = self.memory_mb

        for child in self.children:
            child_hdd, child_cpu, child_mem = child.aggregate_resources()
            total_hdd += child_hdd
            total_cpu += child_cpu
            total_mem += child_mem

        # Preserve direct contribution fields; only the aggregate count is rolled up.
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

    # === New: Self-destruct + DHT/BitTorrent stubs ===
    def self_destruct(self):
        self.self_destruct_triggers.append(time.time())

    def announce_to_dht(self, resource_type: str):
        print(f"[{self.wallet_id}] Announcing {resource_type} share to Kademlia DHT + BitTorrent")

    def discover_peers(self, resource_type: str):
        print(f"[{self.wallet_id}] Discovering peers with {resource_type} via DHT + BitTorrent")





    def create_ppm_transaction(self, direction: str, resource_type: str = "hdd"):
        """Create a transaction tied to this wallet's registered identity."""
        import math
        import time

        if direction not in ("enter", "exit"):
            raise ValueError("direction must be 'enter' or 'exit'")
        if resource_type not in ("hdd", "cpu", "memory"):
            raise ValueError("unsupported resource_type")

        ppm = self.calculate_real_time_ppm()
        if isinstance(ppm, bool) or not isinstance(ppm, (int, float)):
            raise ValueError("calculated PPM must be numeric")
        if not math.isfinite(ppm) or ppm < 0:
            raise ValueError("calculated PPM must be finite and nonnegative")

        return {
            "transaction_id": str(uuid.uuid4()),
            "wallet_id": self.wallet_id,
            "direction": direction,
            "resource_type": resource_type,
            "ppm": ppm,
            "amount": 1,
            "timestamp": time.time(),
        }



    def calculate_real_time_ppm(self):
        """Real-time PPM pricing: base + resource factor (HDD + CPU + Memory)"""
        base_ppm = self.master_count * 0.5
        resource_factor = (
            (self.hdd_share_bytes / GOOGLPLEX) +
            (self.cpu_cycles / GOOGLPLEX) +
            (self.memory_mb / GOOGLPLEX)
        )
        return base_ppm * resource_factor
