"""Build90 characterization tests; these do not prescribe a migration policy."""
import hashlib
import json
import unittest

import main


class Build90HashSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wallet = main.Wallet("build90-test-wallet", is_master=True)
        cls.wallets = {cls.wallet.wallet_id: cls.wallet}

    def valid_tx(self):
        return self.wallet.create_ppm_transaction("enter", "hdd")

    def valid_block(self, tx=None):
        return {"transactions": [tx or self.valid_tx()], "header": ""}

    def test_canonical_hash_differs_from_legacy_hash_for_sample_block(self):
        block = self.valid_block()
        legacy = hashlib.sha256(str(block).encode("utf-8")).hexdigest()
        canonical = hashlib.sha256(
            json.dumps(
                block,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()

        self.assertNotEqual(
            legacy,
            canonical,
            "This is a characterization test, not proof that legacy hashes exist in storage.",
        )

    def test_canonical_hash_is_key_order_independent(self):
        tx = self.valid_tx()
        tx_a = dict(tx)
        tx_b = dict(reversed(list(tx.items())))
        block_a = {"transactions": [tx_a], "header": ""}
        block_b = {"header": "", "transactions": [tx_b]}

        self.assertEqual(
            main.process_block(block_a, self.wallets),
            main.process_block(block_b, self.wallets),
        )

    def test_extra_transaction_field_is_currently_accepted(self):
        tx = self.valid_tx()
        tx["unexpected_build90_field"] = "probe"
        self.assertTrue(main.validate_bit_transaction(tx, self.wallets))

    def test_transaction_has_no_explicit_nonce_or_id_field(self):
        tx = self.valid_tx()
        self.assertNotIn("nonce", tx)
        self.assertNotIn("transaction_id", tx)

    def test_repeated_identical_transaction_is_not_rejected_by_block_validation(self):
        tx = self.valid_tx()
        block = {"transactions": [tx, dict(tx)], "header": ""}
        self.assertTrue(
            main.validate_block(block, self.wallets),
            "Current behavior permits duplicate transactions within one block.",
        )

    def test_transaction_amount_is_not_tied_to_wallet_resource_delta(self):
        tx = self.valid_tx()
        tx["amount"] = 999
        self.assertTrue(
            main.validate_bit_transaction(tx, self.wallets),
            "Current validator checks amount positivity, not a resource-state delta.",
        )


if __name__ == "__main__":
    unittest.main()
