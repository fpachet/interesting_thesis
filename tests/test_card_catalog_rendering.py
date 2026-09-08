from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.generate_card_catalog import Card, latex_inline, main, render_card


class CardCatalogRenderingTests(unittest.TestCase):
    def test_default_export_is_outside_editorial_sources_and_archive(self) -> None:
        with (
            patch("sys.argv", ["generate_card_catalog.py"]),
            patch("scripts.generate_card_catalog.load_cards", return_value={}),
            patch("scripts.generate_card_catalog.load_argument_order", return_value=[]),
            patch("scripts.generate_card_catalog.render_document", return_value="export"),
            patch.object(Path, "mkdir"),
            patch.object(Path, "write_text", autospec=True) as write,
        ):
            main()
        expected = Path(__file__).resolve().parents[1] / "output" / "catalogue-idees.tex"
        write.assert_called_once_with(expected, "export", encoding="utf-8")

    def test_inline_markdown_and_delta_are_latex_safe(self) -> None:
        rendered = latex_inline("**progrès** avec `E(t-Δ)`")

        self.assertIn(r"\textbf{progrès}", rendered)
        self.assertIn(r"\texttt{E(t-\ensuremath{\Delta})}", rendered)
        self.assertNotIn("**", rendered)
        self.assertNotIn("Δ", rendered)

    def test_distinction_and_criterion_sections_are_rendered(self) -> None:
        card = Card(
            card_id="idea_test",
            title="Une proposition",
            kind="hypothesis",
            level="conceptual",
            sources=(),
            source_notes=(),
            references=(),
            sections={
                "Idée": "Une idée.",
                "Distinction": "Une distinction décisive.",
                "Critère": "Un critère vérifiable.",
                "Intérêt pour la thèse": "Une conséquence.",
            },
        )

        rendered = render_card(card)

        self.assertIn(r"\paragraph{Distinction}", rendered)
        self.assertIn("Une distinction décisive.", rendered)
        self.assertIn(r"\paragraph{Critère}", rendered)
        self.assertIn("Un critère vérifiable.", rendered)


if __name__ == "__main__":
    unittest.main()
