from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "estimate-context-size.py"
SPEC = importlib.util.spec_from_file_location("estimate_context_size", MODULE_PATH)
assert SPEC and SPEC.loader
estimator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(estimator)


class EstimateContextSizeTests(unittest.TestCase):
    def test_estimate_tokens_handles_empty_ascii_and_unicode_text(self) -> None:
        self.assertEqual(estimator.estimate_tokens(""), 0)
        self.assertEqual(estimator.estimate_tokens("abcd"), 1)
        self.assertEqual(estimator.estimate_tokens("abcdefgh"), 2)
        self.assertEqual(estimator.estimate_tokens("éééé"), 1)

    def test_iter_files_is_recursive_deterministic_and_excludes_git(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            (root / ".git").mkdir()
            (root / "b.txt").write_text("b", encoding="utf-8")
            (root / "a.txt").write_text("a", encoding="utf-8")
            (root / "nested" / "c.txt").write_text("c", encoding="utf-8")
            (root / ".git" / "ignored.txt").write_text("ignored", encoding="utf-8")

            discovered = [
                path.relative_to(root).as_posix()
                for path in estimator.iter_files([str(root)])
            ]

        self.assertEqual(discovered, ["a.txt", "b.txt", "nested/c.txt"])

    def test_read_text_replaces_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.txt"
            path.write_bytes(b"valid\xff")
            self.assertEqual(estimator.read_text(path), "valid\ufffd")

    def test_missing_path_is_skipped_with_warning(self) -> None:
        missing = Path("definitely-missing-context-file.txt")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            discovered = list(estimator.iter_files([str(missing)]))

        self.assertEqual(discovered, [])
        self.assertIn(f"warning: skipped missing path: {missing}", stderr.getvalue())

    def test_markdown_cli_reports_per_file_and_total_counts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = root / "before.md"
            after = root / "after.md"
            before.write_text("one two\n", encoding="utf-8")
            after.write_text("abc", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    str(before),
                    str(after),
                    "--markdown",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        self.assertIn(
            "| Path | Bytes | Characters | Words | Lines | Est. tokens |",
            completed.stdout,
        )
        self.assertIn("| **Total** | 11 | 11 | 3 | 3 | 3 |", completed.stdout)
        self.assertIn("est_tokens is approximate", completed.stdout)


if __name__ == "__main__":
    unittest.main()
