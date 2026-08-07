from __future__ import annotations

import re
import unittest
from pathlib import Path


class CardMetadataTests(unittest.TestCase):
    def test_every_card_uses_accented_french_sections(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        cards = sorted((project_root / "cartes" / "inbox").glob("idea_*.md"))

        for card in cards:
            text = card.read_text(encoding="utf-8")
            self.assertEqual(text.count("## Idée"), 1, card.name)
            self.assertEqual(text.count("## Intérêt pour la thèse"), 1, card.name)
            self.assertNotIn("## Idee", text, card.name)
            self.assertNotIn("## Interet pour la these", text, card.name)

    def test_every_card_has_one_valid_level_and_unique_id(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        cards = sorted((project_root / "cartes" / "inbox").glob("idea_*.md"))
        valid_levels = {"conceptual", "scientific", "articulation"}
        seen_ids: set[str] = set()

        self.assertTrue(cards)
        for card in cards:
            text = card.read_text(encoding="utf-8")
            frontmatter = text.split("---", 2)[1]
            card_ids = re.findall(r"^id:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
            levels = re.findall(r"^level:\s*(\S+)\s*$", frontmatter, re.MULTILINE)

            self.assertEqual(len(card_ids), 1, card.name)
            self.assertNotIn(card_ids[0], seen_ids, card.name)
            seen_ids.add(card_ids[0])
            self.assertEqual(len(levels), 1, card.name)
            self.assertIn(levels[0], valid_levels, card.name)

    def test_every_local_source_exists(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        cards = sorted((project_root / "cartes" / "inbox").glob("idea_*.md"))

        for card in cards:
            text = card.read_text(encoding="utf-8")
            frontmatter = text.split("---", 2)[1]
            source_block = re.search(
                r"^sources:\s*$\n(?P<items>(?:^  - .*$\n?)+)",
                frontmatter,
                re.MULTILINE,
            )
            self.assertIsNotNone(source_block, card.name)
            sources = re.findall(r'^  - "([^"]+)"\s*$', source_block["items"], re.MULTILINE)
            self.assertTrue(sources, card.name)
            for source in sources:
                self.assertTrue((project_root / source).exists(), f"{card.name}: {source}")

    def test_architectural_statuses_are_valid_and_core_index_matches_metadata(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        cards = sorted((project_root / "cartes" / "inbox").glob("idea_*.md"))
        valid_statuses = {"core", "derived", "test", "case", "objection", "speculative"}
        metadata_core: set[str] = set()

        for card in cards:
            frontmatter = card.read_text(encoding="utf-8").split("---", 2)[1]
            card_id = re.search(r"^id:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
            statuses = re.findall(
                r"^architecture:\s*(\S+)\s*$", frontmatter, re.MULTILINE
            )
            self.assertLessEqual(len(statuses), 1, card.name)
            if not statuses:
                continue
            self.assertIn(statuses[0], valid_statuses, card.name)
            if statuses[0] == "core":
                self.assertIsNotNone(card_id, card.name)
                metadata_core.add(card_id.group(1))

        architecture_index = (
            project_root / "cartes" / "indexes" / "by_architecture.md"
        ).read_text(encoding="utf-8")
        core_section = architecture_index.split(
            "## Première passe : les 15 propositions `CORE`", 1
        )[1].split("## Règle de la prochaine passe", 1)[0]
        indexed_core = set(
            re.findall(r"^- `(idea_\d{4})` - ", core_section, re.MULTILINE)
        )

        self.assertEqual(len(metadata_core), 15)
        self.assertEqual(indexed_core, metadata_core)

    def test_card_reference_keys_exist_in_bibliography(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        bibliography = (project_root / "bibliographie" / "references.bib").read_text(
            encoding="utf-8"
        )
        bib_keys = re.findall(r"^@\w+\{([^,]+),", bibliography, re.MULTILINE)
        self.assertEqual(len(bib_keys), len(set(bib_keys)), "duplicate BibTeX keys")

        for card in sorted((project_root / "cartes" / "inbox").glob("idea_*.md")):
            frontmatter = card.read_text(encoding="utf-8").split("---", 2)[1]
            reference_block = re.search(
                r"^references:\s*$\n(?P<items>(?:^  - .*$\n?)+)",
                frontmatter,
                re.MULTILINE,
            )
            if reference_block is None:
                continue
            keys = re.findall(r"^  - (\S+)\s*$", reference_block["items"], re.MULTILINE)
            self.assertTrue(keys, card.name)
            for key in keys:
                self.assertIn(key, bib_keys, f"{card.name}: {key}")

    def test_bibliography_local_files_exist(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        bibliography = (project_root / "bibliographie" / "references.bib").read_text(
            encoding="utf-8"
        )
        local_files = re.findall(r"^\s*file\s*=\s*\{([^}]+)\}", bibliography, re.MULTILINE)
        self.assertTrue(local_files)
        for local_file in local_files:
            self.assertTrue((project_root / local_file).exists(), local_file)


if __name__ == "__main__":
    unittest.main()
