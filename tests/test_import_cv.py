import tempfile
import unittest
from pathlib import Path

from scripts.import_cv import choose_input, line_to_markdown


class MarkdownFormattingTests(unittest.TestCase):
    def test_known_heading(self):
        self.assertEqual(line_to_markdown("Technical Skills"), "## Technical Skills")

    def test_uppercase_heading(self):
        self.assertEqual(line_to_markdown("PROJECTS"), "## Projects")

    def test_bullet(self):
        self.assertEqual(line_to_markdown(" • Built an API"), "- Built an API")

    def test_plain_content_is_not_rewritten(self):
        self.assertEqual(line_to_markdown("Python | Django"), "Python | Django")


class InputSelectionTests(unittest.TestCase):
    def test_selects_only_pdf_in_inbox(self):
        with tempfile.TemporaryDirectory() as directory:
            inbox = Path(directory)
            expected = inbox / "resume.pdf"
            expected.touch()
            self.assertEqual(choose_input(None, inbox), expected)

    def test_rejects_ambiguous_inbox(self):
        with tempfile.TemporaryDirectory() as directory:
            inbox = Path(directory)
            (inbox / "one.pdf").touch()
            (inbox / "two.pdf").touch()
            with self.assertRaisesRegex(ValueError, "multiple PDFs"):
                choose_input(None, inbox)


if __name__ == "__main__":
    unittest.main()
