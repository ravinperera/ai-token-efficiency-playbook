from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "estimate-context-size.py"
SPEC = importlib.util.spec_from_file_location("estimate_context_size", SCRIPT_PATH)
assert SPEC and SPEC.loader
estimator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = estimator
SPEC.loader.exec_module(estimator)


class EstimateContextSizeTests(unittest.TestCase):
    def test_token_estimate_handles_empty_and_short_text(self) -> None:
        self.assertEqual(estimator.estimate_tokens(""), 0)
        self.assertEqual(estimator.estimate_tokens("a"), 1)
        self.assertEqual(estimator.estimate_tokens("abcdefgh"), 2)

    def test_iter_files_is_sorted_and_excludes_git_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.txt").write_text("b", encoding="utf-8")
            (root / "a.txt").write_text("a", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("secret", encoding="utf-8")

            files = [path.name for path in estimator.iter_files([str(root)])]
            self.assertEqual(files, ["a.txt", "b.txt"])

    def test_read_text_replaces_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.bin"
            path.write_bytes(b"good\xffbad")
            self.assertEqual(estimator.read_text(path), "good\ufffdbad")

    def test_markdown_cli_reports_unicode_totals(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first.md"
            second = root / "second.md"
            first.write_text("hello world\n", encoding="utf-8")
            second.write_text("£\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    str(first),
                    str(second),
                    "--markdown",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("| **Total** | 15 | 14 | 3 | 4 | 4 |", result.stdout)
            self.assertIn("est_tokens is approximate", result.stdout)

    def test_missing_path_is_warned_and_skipped(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "does-not-exist.md"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("warning: skipped missing path", result.stderr)
        self.assertIn(
            "total: bytes=0 chars=0 words=0 lines=0 est_tokens=0",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
