import hashlib
import json
import math
import unittest
import uuid

import main


class MainTransactionRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wallet = main.Wallet("build84-test-wallet")
        cls.wallets = {cls.wallet.wallet_id: cls.wallet}
        cls.ppm = cls.wallet.calculate_real_time_ppm()
        cls.tx = {
            "transaction_id": str(uuid.uuid4()),
            "wallet_id": cls.wallet.wallet_id,
            "direction": "enter",
            "resource_type": "hdd",
            "amount": 1.0,
            "ppm": cls.ppm,
            "timestamp": 1700000000.0,
        }

    def validate(self, changes=None, remove=()):
        tx = dict(self.tx)
        tx.update(changes or {})
        for key in remove:
            tx.pop(key, None)
        return main.validate_bit_transaction(tx, self.wallets)

    def test_valid_transaction_is_accepted(self):
        self.assertTrue(self.validate())

    def test_amount_is_required(self):
        self.assertFalse(self.validate(remove=("amount",)))

    def test_amount_must_be_positive(self):
        for value in (0, -1, True, "1", float("nan"), float("inf")):
            with self.subTest(value=value):
                self.assertFalse(self.validate({"amount": value}))

    def test_timestamp_is_required(self):
        self.assertFalse(self.validate(remove=("timestamp",)))

    def test_timestamp_must_be_positive_finite_number(self):
        for value in (0, -1, True, "1700000000",
                      float("nan"), float("inf")):
            with self.subTest(value=value):
                self.assertFalse(self.validate({"timestamp": value}))

    def test_ppm_must_be_numeric_not_boolean_or_nonfinite(self):
        for value in (True, "1", float("nan"), float("inf"), -1):
            with self.subTest(value=value):
                self.assertFalse(self.validate({"ppm": value}))

    def test_ppm_mismatch_is_not_accepted_with_tolerance(self):
        # Choose a representable offset above the previous absolute tolerance.
        self.assertFalse(self.validate({"ppm": self.ppm + 0.02}))

    def test_hash_is_stable_when_top_level_keys_are_reordered(self):
        a = {"transactions": [dict(self.tx)], "header": ""}
        b = {"header": "", "transactions": [dict(self.tx)]}
        self.assertEqual(
            main.process_block(a, self.wallets),
            main.process_block(b, self.wallets),
        )

    def test_hash_is_stable_when_nested_transaction_keys_are_reordered(self):
        tx_a = dict(self.tx)
        tx_b = dict(reversed(list(self.tx.items())))
        a = {"transactions": [tx_a], "header": ""}
        b = {"header": "", "transactions": [tx_b]}
        self.assertEqual(
            main.process_block(a, self.wallets),
            main.process_block(b, self.wallets),
        )

    def test_hash_matches_canonical_json_reference(self):
        block = {"transactions": [dict(self.tx)], "header": ""}
        expected = hashlib.sha256(
            json.dumps(
                block,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(main.process_block(block, self.wallets), expected)


if __name__ == "__main__":
    unittest.main()
