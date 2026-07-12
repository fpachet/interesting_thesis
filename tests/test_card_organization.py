from __future__ import annotations

import re
import unittest
from collections import Counter
from pathlib import Path


class CardOrganizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.card_ids = set()
        for card in (cls.project_root / "cartes" / "inbox").glob("idea_*.md"):
            frontmatter = card.read_text(encoding="utf-8").split("---", 2)[1]
            match = re.search(r"^id:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
            if match is not None:
                cls.card_ids.add(match.group(1))

    def test_argument_index_assigns_every_card_exactly_once(self) -> None:
        index = (
            self.project_root / "cartes" / "indexes" / "by_argument.md"
        ).read_text(encoding="utf-8")
        indexed_ids = re.findall(r"^- `(idea_\d{4})` - ", index, re.MULTILINE)
        counts = Counter(indexed_ids)

        self.assertEqual(set(indexed_ids), self.card_ids)
        self.assertEqual(
            {card_id: count for card_id, count in counts.items() if count != 1},
            {},
        )

    def test_typed_relations_are_valid_and_unique(self) -> None:
        allowed_relations = {
            "specifies",
            "supports",
            "operationalizes",
            "illustrates",
            "limits",
            "objects_to",
            "contrasts_with",
            "bridges",
            "motivates",
        }
        relation_file = self.project_root / "cartes" / "relations.tsv"
        seen_edges: set[tuple[str, str, str]] = set()

        for line_number, line in enumerate(
            relation_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line or line.startswith("#"):
                continue

            fields = line.split("\t")
            self.assertEqual(len(fields), 4, f"line {line_number}")
            source, relation, target, note = fields
            edge = (source, relation, target)

            self.assertIn(source, self.card_ids, f"line {line_number}")
            self.assertIn(target, self.card_ids, f"line {line_number}")
            self.assertNotEqual(source, target, f"line {line_number}")
            self.assertIn(relation, allowed_relations, f"line {line_number}")
            self.assertTrue(note.strip(), f"line {line_number}")
            self.assertNotIn(edge, seen_edges, f"line {line_number}")
            seen_edges.add(edge)

        self.assertTrue(seen_edges)


if __name__ == "__main__":
    unittest.main()
