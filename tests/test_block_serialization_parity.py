import unittest

import main
from core import pseudocode


class BlockSerializationParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wallet = main.Wallet("build88-parity-wallet", is_master=True)
        cls.wallets = {cls.wallet.wallet_id: cls.wallet}

    def valid_transaction(self):
        return self.wallet.create_ppm_transaction("enter", "hdd")

    def assert_both_reject_serialization(self, extra_value):
        block = {
            "transactions": [self.valid_transaction()],
            "extra": extra_value,
        }

        for name, implementation in (
            ("main", main),
            ("pseudocode", pseudocode),
        ):
            with self.subTest(implementation=name):
                with self.assertRaisesRegex(
                    ValueError,
                    "^Block is not deterministically JSON-serializable$",
                ):
                    implementation.process_block(block, self.wallets)

    def test_nan_is_rejected_with_same_error(self):
        self.assert_both_reject_serialization(float("nan"))

    def test_positive_infinity_is_rejected_with_same_error(self):
        self.assert_both_reject_serialization(float("inf"))

    def test_set_is_rejected_with_same_error(self):
        self.assert_both_reject_serialization({1, 2})

    def test_valid_block_hashes_still_match(self):
        block = {"transactions": [self.valid_transaction()]}
        self.assertEqual(
            main.process_block(block, self.wallets),
            pseudocode.process_block(block, self.wallets),
        )


if __name__ == "__main__":
    unittest.main()
