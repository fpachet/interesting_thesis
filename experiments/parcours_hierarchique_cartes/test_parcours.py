from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import parcours


class HierarchicalRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = parcours.build_model(parcours.PROJECT_ROOT, parcours.DEFAULT_CONFIG)

    def test_core_index_and_metadata_agree(self) -> None:
        indexed = [card_id for _, ids in self.model.core_sections for card_id in ids]
        metadata = [
            card_id
            for card_id, card in self.model.cards.items()
            if card.architecture == "core"
        ]
        self.assertEqual(set(indexed), set(metadata))
        self.assertEqual(len(indexed), len(set(indexed)))

    def test_core_route_is_complete_and_respects_chapter_order(self) -> None:
        route, _ = parcours.exact_core_route(self.model)
        expected = {card_id for _, ids in self.model.core_sections for card_id in ids}
        self.assertEqual(set(route), expected)
        self.assertEqual(len(route), len(expected))
        section_of = {
            card_id: section_index
            for section_index, (_, ids) in enumerate(self.model.core_sections)
            for card_id in ids
        }
        section_sequence = [section_of[card_id] for card_id in route]
        self.assertEqual(section_sequence, sorted(section_sequence))

    def test_every_non_core_card_gets_one_primary_anchor(self) -> None:
        route, _ = parcours.exact_core_route(self.model)
        primary, alternatives = parcours.assign_to_core(self.model, route)
        non_core = set(self.model.cards) - set(route)
        self.assertEqual(set(primary), non_core)
        self.assertEqual(set(alternatives), non_core)
        self.assertTrue(all(anchor in route for anchor in primary.values()))

    def test_graph_distance_rewards_direct_editorial_links(self) -> None:
        direct = next(iter(self.model.local_links))
        source, target = tuple(direct)
        self.assertEqual(
            self.model.graph_distances[parcours.ordered_pair(source, target)],
            0.0,
        )

    def test_generation_stays_inside_requested_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            result = parcours.generate(parcours.PROJECT_ROOT, parcours.DEFAULT_CONFIG, output)
            self.assertEqual(result["summary"]["card_count"], len(self.model.cards))
            self.assertTrue((output / "parcours.md").is_file())
            self.assertTrue((output / "parcours.json").is_file())
            self.assertTrue((output / "distances.tsv").is_file())

    def test_diagnostics_cover_anchor_loads(self) -> None:
        result = parcours.build_result(self.model)
        loads = result["diagnostics"]["anchor_loads"]
        self.assertEqual(sum(loads.values()), len(self.model.cards) - len(parcours.core_ids(self.model)))


if __name__ == "__main__":
    unittest.main()
