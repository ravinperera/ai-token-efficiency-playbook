from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

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

    def test_require_tiktoken_fails_without_fallback(self) -> None:
        output, errors = io.StringIO(), io.StringIO()
        with (
            patch.object(counter, "tiktoken_count", return_value=None),
            patch.object(sys, "argv", ["count-tokens.py", "--require-tiktoken"]),
            patch.object(sys, "stdin", io.StringIO("hello")),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            code = counter.main()

        self.assertEqual(code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("error: tiktoken unavailable", errors.getvalue())

    def test_require_tiktoken_emits_exact_count_when_available(self) -> None:
        output, errors = io.StringIO(), io.StringIO()
        with (
            patch.object(counter, "tiktoken_count", return_value=7) as tokenizer,
            patch.object(sys, "argv", ["count-tokens.py", "--require-tiktoken"]),
            patch.object(sys, "stdin", io.StringIO("sample")),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            code = counter.main()

        self.assertEqual(code, 0)
        tokenizer.assert_called_once_with("sample", "cl100k_base")
        self.assertEqual(output.getvalue().strip(), "7\ttiktoken\tstdin")
        self.assertEqual(errors.getvalue(), "")

    def test_conflicting_counting_modes_fail(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--require-tiktoken",
                "--approx-only",
            ],
            input="hello",
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("not allowed with argument", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
