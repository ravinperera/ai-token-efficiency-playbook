from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_markdown_quality.py"
SPEC = importlib.util.spec_from_file_location("check_markdown_quality", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MarkdownQualityTests(unittest.TestCase):
    def test_valid_relative_link_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text(
                "# Project\n\n[Guide](docs/guide.md)\n", encoding="utf-8"
            )

            self.assertEqual([], MODULE.validate_markdown(root, readme))

    def test_missing_relative_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text("[Missing](docs/missing.md)\n", encoding="utf-8")

            errors = MODULE.validate_markdown(root, readme)
            self.assertIn("missing local link target", errors[0])

    def test_external_anchor_and_fenced_links_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text(
                "[Web](https://example.com) [Section](#section)\n\n"
                "```md\n[Example](missing.md)\n```\n",
                encoding="utf-8",
            )

            self.assertEqual([], MODULE.validate_markdown(root, readme))

    def test_trailing_whitespace_outside_fence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text("# Project  \n", encoding="utf-8")

            self.assertEqual(
                ["line 1: trailing whitespace"],
                MODULE.validate_markdown(root, readme),
            )

    def test_unclosed_fence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text("```text\nexample\n", encoding="utf-8")

            errors = MODULE.validate_markdown(root, readme)
            self.assertIn("unclosed Markdown fence", errors[0])

    def test_repository_escape_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text("[Outside](../outside.md)\n", encoding="utf-8")

            errors = MODULE.validate_markdown(root, readme)
            self.assertIn("link escapes the repository", errors[0])


    def _errors_for(self, markdown: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text(markdown, encoding="utf-8")
            return MODULE.validate_markdown(root, readme)

    def test_long_backtick_fence_protects_shorter_nested_examples(self) -> None:
        markdown = (
            "````markdown\n"
            "```python\n"
            "[Inside](missing-inside.md)  \n"
            "```\n"
            "````\n"
            "[Outside](missing-outside.md)\n"
        )
        self.assertEqual(
            ["missing local link target: missing-outside.md"],
            self._errors_for(markdown),
        )

    def test_tilde_fence_ignores_shorter_and_mixed_markers(self) -> None:
        markdown = (
            "~~~~markdown\n"
            "~~~\n"
            "````\n"
            "[Inside](missing-inside.md)\n"
            "~~~~~\n"
            "[Valid](README.md)\n"
        )
        self.assertEqual([], self._errors_for(markdown))

    def test_closing_fence_cannot_have_info_text(self) -> None:
        markdown = (
            "```text\n"
            "```not-a-closer\n"
            "[Inside](missing-inside.md)\n"
            "```\n"
        )
        self.assertEqual([], self._errors_for(markdown))

    def test_shorter_closing_fence_leaves_outer_fence_unclosed(self) -> None:
        markdown = (
            "````markdown\n"
            "```\n"
            "[Inside](missing-inside.md)\n"
        )
        self.assertEqual(
            ["line 1: unclosed Markdown fence starting with ````"],
            self._errors_for(markdown),
        )

    def test_four_space_indented_ticks_do_not_start_fence(self) -> None:
        markdown = "    ```\n[Outside](missing.md)\n"
        self.assertEqual(
            ["missing local link target: missing.md"],
            self._errors_for(markdown),
        )


if __name__ == "__main__":
    unittest.main()
