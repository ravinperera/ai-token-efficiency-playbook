from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "count-tokens.py"
SPEC = importlib.util.spec_from_file_location("count_tokens", SCRIPT_PATH)
assert SPEC and SPEC.loader
counter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = counter
SPEC.loader.exec_module(counter)


class CountTokensTests(unittest.TestCase):
    def test_approximation_is_deterministic_for_empty_and_punctuation(self) -> None:
        self.assertEqual(counter.approximate_tokens(""), 0)
        self.assertEqual(counter.approximate_tokens("hello"), 1)
        self.assertEqual(counter.approximate_tokens("hello, world!"), 4)

    def test_approx_only_cli_counts_file_without_tiktoken(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("hello, world!", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(path), "--approx-only"],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                result.stdout.strip(),
                f"4\tapproximation\t{path}",
            )

    def test_approx_only_cli_reads_stdin(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--approx-only"],
            input="one two",
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.stdout.strip(), "2\tapproximation\tstdin")


if __name__ == "__main__":
    unittest.main()
