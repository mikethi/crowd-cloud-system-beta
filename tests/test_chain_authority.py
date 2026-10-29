"""Tests for the provider-neutral chain-authority contract.

These tests exercise a simulation interface only. They do not prove real
blockchain consensus, finality, authentication, persistence, or networking.
"""

import unittest

from core.chain_authority import (
    AuthorityConflict,
    AuthoritySnapshot,
    AuthorityStatus,
    AuthorityUnavailable,
    ChainDecision,
    DecisionNotFinalized,
    FinalizedDecisionConsumer,
    InMemoryAuthorityDouble,
    require_finalized,
)


def decision(identifier, sequence, status=AuthorityStatus.FINALIZED):
    return ChainDecision(
        decision_id=identifier,
        status=status,
        sequence=sequence,
        code_hash=None,
        policy_ref=None,
    )


class ChainAuthorityContractTests(unittest.TestCase):
    def test_pending_snapshot_cannot_authorize_work(self):
        snapshot = AuthoritySnapshot(
            status=AuthorityStatus.PENDING,
            detail="simulation pending",
        )
        with self.assertRaises(DecisionNotFinalized):
            require_finalized(snapshot)

    def test_unknown_snapshot_fails_closed(self):
        snapshot = AuthoritySnapshot(status=AuthorityStatus.UNKNOWN)
        with self.assertRaises(DecisionNotFinalized):
            require_finalized(snapshot)

    def test_unavailable_snapshot_fails_closed(self):
        snapshot = AuthoritySnapshot(
            status=AuthorityStatus.UNAVAILABLE,
            detail="provider unavailable",
        )
        with self.assertRaises(AuthorityUnavailable):
            require_finalized(snapshot)

    def test_conflicting_snapshot_fails_closed(self):
        snapshot = AuthoritySnapshot(
            status=AuthorityStatus.CONFLICTING,
            detail="conflicting history",
        )
        with self.assertRaises(AuthorityConflict):
            require_finalized(snapshot)

    def test_finalized_decisions_are_returned_in_order(self):
        first = decision("decision-a", 1)
        second = decision("decision-b", 2)
        snapshot = AuthoritySnapshot(
            status=AuthorityStatus.FINALIZED,
            decisions=(first, second),
        )
        self.assertEqual(require_finalized(snapshot), (first, second))

    def test_repeated_delivery_is_idempotent_in_memory(self):
        snapshot = AuthoritySnapshot(
            status=AuthorityStatus.FINALIZED,
            decisions=(decision("decision-a", 1),),
        )
        consumer = FinalizedDecisionConsumer()
        self.assertEqual(consumer.consume(snapshot), ("decision-a",))
        self.assertEqual(consumer.consume(snapshot), ())
        self.assertEqual(consumer.consumed_ids, frozenset({"decision-a"}))

    def test_double_defaults_to_unknown(self):
        double = InMemoryAuthorityDouble()
        self.assertEqual(
            double.read_authority().status,
            AuthorityStatus.UNKNOWN,
        )

    def test_double_can_report_unavailable(self):
        double = InMemoryAuthorityDouble()
        double.set_snapshot(
            AuthoritySnapshot(status=AuthorityStatus.UNAVAILABLE)
        )
        with self.assertRaises(AuthorityUnavailable):
            require_finalized(double.read_authority())

    def test_rejects_non_finalized_decision_in_finalized_snapshot(self):
        pending = decision("decision-pending", 1, AuthorityStatus.PENDING)
        with self.assertRaises(ValueError):
            AuthoritySnapshot(
                status=AuthorityStatus.FINALIZED,
                decisions=(pending,),
            )

    def test_rejects_duplicate_decision_ids(self):
        first = decision("same-id", 1)
        second = decision("same-id", 2)
        with self.assertRaises(ValueError):
            AuthoritySnapshot(
                status=AuthorityStatus.FINALIZED,
                decisions=(first, second),
            )

    def test_rejects_out_of_order_sequences(self):
        with self.assertRaises(ValueError):
            AuthoritySnapshot(
                status=AuthorityStatus.FINALIZED,
                decisions=(
                    decision("later", 2),
                    decision("earlier", 1),
                ),
            )

    def test_rejects_boolean_sequence(self):
        with self.assertRaises(ValueError):
            ChainDecision(
                decision_id="bad-sequence",
                status=AuthorityStatus.FINALIZED,
                sequence=True,
            )


if __name__ == "__main__":
    unittest.main()
