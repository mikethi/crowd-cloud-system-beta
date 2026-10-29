import unittest

from core.adaptive_placement import Peer, plan_placements


class PlacementRegressionTests(unittest.TestCase):
    def test_out_of_range_old_shard_index_is_not_actionable(self):
        peers = [Peer(f"p{i}", 5) for i in range(5)]
        current = {i: (f"p{i}",) for i in range(5)}
        current[99] = ("p0", "departed")

        with self.assertRaisesRegex(ValueError, "shard index out of range"):
            plan_placements(peers, current)

    def test_negative_old_shard_index_is_not_actionable(self):
        peers = [Peer(f"p{i}", 5) for i in range(5)]
        current = {i: (f"p{i}",) for i in range(5)}
        current[-1] = ("p0",)

        with self.assertRaisesRegex(ValueError, "shard index out of range"):
            plan_placements(peers, current)

    def test_changed_domains_do_not_leave_duplicate_domains_per_shard(self):
        old_peers = [
            Peer("a", 5, "rack-a"),
            Peer("b", 5, "rack-b"),
            Peer("c", 5, "rack-c"),
            Peer("d", 5, "rack-d"),
            Peer("e", 5, "rack-e"),
            Peer("f", 5, "rack-f"),
            Peer("g", 5, "rack-g"),
            Peer("h", 5, "rack-h"),
            Peer("i", 5, "rack-i"),
            Peer("j", 5, "rack-j"),
        ]
        old_plan = plan_placements(old_peers)

        changed_peers = [
            Peer(p.peer_id, p.capacity,
                 "shared-rack" if p.peer_id in {"a", "b"}
                 else p.failure_domain)
            for p in old_peers
        ]
        plan = plan_placements(changed_peers, old_plan.placements)
        domain_by_id = {p.peer_id: p.failure_domain for p in changed_peers}

        for shard, peer_ids in plan.placements.items():
            domains = [domain_by_id[peer_id] for peer_id in peer_ids]
            self.assertEqual(
                len(domains), len(set(domains)),
                f"shard {shard} has duplicate failure domains: {domains}",
            )

    def test_peer_id_whitespace_is_rejected(self):
        with self.assertRaises(ValueError):
            plan_placements([Peer("   ", 2)])

    def test_negative_shard_count_is_rejected(self):
        with self.assertRaises(ValueError):
            plan_placements([Peer("p0", 2)], shard_count=-1)


if __name__ == "__main__":
    unittest.main()
