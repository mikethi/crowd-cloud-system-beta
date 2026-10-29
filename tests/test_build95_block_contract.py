"""Build95: regression tests for validation/hash-only block processing."""

import copy
import unittest

import main
import core.pseudocode as pseudocode


def wallet_state(wallet):
    """Snapshot ordinary in-memory wallet fields for mutation assertions."""
    return copy.deepcopy(vars(wallet))


class BlockContractTests(unittest.TestCase):
    def setUp(self):
        self.wallet = main.Wallet("build95-contract-wallet")
        self.wallets = {self.wallet.wallet_id: self.wallet}
        self.tx = self.wallet.create_ppm_transaction("enter", "hdd")

    def block(self, transactions=None):
        return {"transactions": copy.deepcopy(
            [self.tx] if transactions is None else transactions
        )}

    def test_valid_process_block_returns_stable_hash_without_mutation(self):
        block = self.block()
        before = wallet_state(self.wallet)

        first_hash = main.process_block(block, self.wallets)
        second_hash = main.process_block(block, self.wallets)

        self.assertIsInstance(first_hash, str)
        self.assertEqual(len(first_hash), 64)
        self.assertEqual(first_hash, second_hash)
        self.assertEqual(wallet_state(self.wallet), before)

    def test_invalid_block_fails_without_wallet_mutation(self):
        bad_tx = copy.deepcopy(self.tx)
        bad_tx["amount"] = 0
        block = self.block([self.tx, bad_tx])
        before = wallet_state(self.wallet)

        with self.assertRaisesRegex(ValueError, "^Invalid block$"):
            main.process_block(block, self.wallets)

        self.assertEqual(wallet_state(self.wallet), before)

    def test_block_validation_does_not_mutate_wallet(self):
        before = wallet_state(self.wallet)

        self.assertTrue(main.validate_block(self.block(), self.wallets))

        self.assertEqual(wallet_state(self.wallet), before)

    def test_transaction_validation_does_not_mutate_wallet(self):
        before = wallet_state(self.wallet)

        self.assertTrue(main.validate_bit_transaction(self.tx, self.wallets))

        self.assertEqual(wallet_state(self.wallet), before)

    def test_main_and_pseudocode_agree_on_valid_transaction(self):
        main_result = main.validate_bit_transaction(self.tx, self.wallets)
        pseudo_result = pseudocode.validate_bit_transaction(
            copy.deepcopy(self.tx), self.wallets
        )

        self.assertEqual(main_result, pseudo_result)
        self.assertTrue(main_result)

    def test_main_and_pseudocode_agree_on_invalid_amount(self):
        bad_tx = copy.deepcopy(self.tx)
        bad_tx["amount"] = 0

        main_result = main.validate_bit_transaction(bad_tx, self.wallets)
        pseudo_result = pseudocode.validate_bit_transaction(
            copy.deepcopy(bad_tx), self.wallets
        )

        self.assertEqual(main_result, pseudo_result)
        self.assertFalse(main_result)

    def test_main_and_pseudocode_agree_on_block_validity(self):
        valid_block = self.block()
        bad_tx = copy.deepcopy(self.tx)
        bad_tx["amount"] = 0
        invalid_block = self.block([bad_tx])

        self.assertEqual(
            main.validate_block(valid_block, self.wallets),
            pseudocode.validate_block(valid_block, self.wallets),
        )
        self.assertEqual(
            main.validate_block(invalid_block, self.wallets),
            pseudocode.validate_block(invalid_block, self.wallets),
        )
        self.assertTrue(main.validate_block(valid_block, self.wallets))
        self.assertFalse(main.validate_block(invalid_block, self.wallets))


if __name__ == "__main__":
    unittest.main()
