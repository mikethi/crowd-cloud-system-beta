import unittest

from core.adaptive_placement import Peer, plan_placements


def peers(count, capacity=3):
    return [Peer(f"peer-{i:02d}", capacity) for i in range(count)]


class AdaptivePlacementTests(unittest.TestCase):
    def test_replica_tiers(self):
        cases = [
            (4, 1),
            (5, 1),
            (9, 1),
            (10, 2),
            (14, 2),
            (15, 3),
            (20, 3),
        ]
        for count, expected in cases:
            with self.subTest(count=count):
                plan = plan_placements(peers(count))
                self.assertEqual(plan.desired_replicas, expected)

    def test_ten_peers_spread_two_copies_of_each_shard(self):
        plan = plan_placements(peers(10, capacity=2))
        self.assertEqual(plan.under_replicated, ())
        self.assertEqual(plan.placement_count, 10)
        self.assertTrue(all(len(v) == 2 for v in plan.placements.values()))
        used = {peer for group in plan.placements.values() for peer in group}
        self.assertEqual(len(used), 10)

    def test_existing_placements_are_stable_when_peer_joins(self):
        initial = plan_placements(peers(5, capacity=3))
        expanded = plan_placements(peers(6, capacity=3), initial.placements)
        self.assertEqual(expanded.placements, initial.placements)
        self.assertEqual(expanded.additions, ())
        self.assertEqual(expanded.removals, ())

    def test_departed_peer_is_replaced(self):
        original_peers = peers(5, capacity=3)
        initial = plan_placements(original_peers)
        departed = original_peers[0].peer_id
        remaining = [p for p in original_peers if p.peer_id != departed]

        updated = plan_placements(remaining, initial.placements)
        self.assertTrue(any(departed == p for _, p in updated.removals))
        self.assertNotIn(departed, {
            p for group in updated.placements.values() for p in group
        })
        self.assertEqual(updated.under_replicated, ())

    def test_capacity_limits_are_respected(self):
        plan = plan_placements(peers(10, capacity=1))
        counts = {}
        for group in plan.placements.values():
            for peer_id in group:
                counts[peer_id] = counts.get(peer_id, 0) + 1
        self.assertTrue(all(count <= 1 for count in counts.values()))

    def test_insufficient_capacity_is_reported(self):
        plan = plan_placements(peers(2, capacity=1), max_replicas=2)
        self.assertTrue(plan.under_replicated)
        self.assertTrue(all(len(v) <= 1 for v in plan.placements.values()))

    def test_failure_domains_are_distinct_per_shard(self):
        group = [
            Peer("a", 5, failure_domain="rack-1"),
            Peer("b", 5, failure_domain="rack-1"),
            Peer("c", 5, failure_domain="rack-2"),
            Peer("d", 5, failure_domain="rack-3"),
            Peer("e", 5, failure_domain="rack-4"),
            Peer("f", 5, failure_domain="rack-5"),
            Peer("g", 5, failure_domain="rack-6"),
            Peer("h", 5, failure_domain="rack-7"),
            Peer("i", 5, failure_domain="rack-8"),
            Peer("j", 5, failure_domain="rack-9"),
        ]
        plan = plan_placements(group)
        domains = {p.peer_id: p.failure_domain for p in group}
        for shard_peers in plan.placements.values():
            selected_domains = [domains[p] for p in shard_peers]
            self.assertEqual(len(selected_domains), len(set(selected_domains)))

    def test_invalid_duplicate_peer_ids_rejected(self):
        with self.assertRaises(ValueError):
            plan_placements([Peer("same", 2), Peer("same", 2)])

    def test_repeated_planning_is_idempotent(self):
        group = peers(10, capacity=2)
        first = plan_placements(group)
        second = plan_placements(group, first.placements)
        self.assertEqual(first.placements, second.placements)
        self.assertEqual(second.additions, ())
        self.assertEqual(second.removals, ())


if __name__ == "__main__":
    unittest.main()
