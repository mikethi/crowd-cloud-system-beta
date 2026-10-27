# models/wallet.py
import time
from typing import List, Optional

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

    def aggregate_master_count(self):
        total = self.master_count
        for child in self.children:
            total += child.aggregate_master_count()
        self.master_count = total
        return total

    def add_child(self, child_wallet):
        self.children.append(child_wallet)
        child_wallet.parent = self
        self.aggregate_master_count()

    def mark_publicly_paid(self):
        self.is_publicly_paid = True
        self.provence_chain.append({"time": time.time(), "action": "publicly_paid", "delta": 0})

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
