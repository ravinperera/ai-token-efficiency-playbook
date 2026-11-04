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

    def test_iter_files_is_recursive_sorted_and_excludes_git_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            (root / "b.txt").write_text("b", encoding="utf-8")
            (root / "nested" / "a.txt").write_text("a", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("secret", encoding="utf-8")

            files = list(estimator.iter_files([str(root)]))
            self.assertEqual(files, [root / "b.txt", root / "nested" / "a.txt"])

    def test_recursive_scan_prunes_generated_trees_but_keeps_source_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            similar_name = root / "node_modules.txt"
            source.write_text("real context", encoding="utf-8")
            similar_name.write_text("also context", encoding="utf-8")

            for name in (".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"):
                artifact = root / name / "nested" / "generated.txt"
                artifact.parent.mkdir(parents=True)
                artifact.write_text("not context", encoding="utf-8")

            nested_artifact = root / "src" / "node_modules" / "generated.js"
            nested_artifact.parent.mkdir(parents=True)
            nested_artifact.write_text("not context", encoding="utf-8")

            self.assertEqual(
                list(estimator.iter_files([str(root)])),
                sorted([source, similar_name]),
            )

    def test_explicit_generated_paths_are_included_and_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            source.write_text("context", encoding="utf-8")
            generated_dir = root / "node_modules"
            generated_dir.mkdir()
            generated = generated_dir / "package.js"
            generated.write_text("explicit input", encoding="utf-8")

            self.assertEqual(
                list(estimator.iter_files([str(root), str(generated), str(generated_dir)])),
                [source, generated],
            )

    def test_excluded_ancestor_name_does_not_skip_explicit_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / ".venv" / "project"
            repo.mkdir(parents=True)
            document = repo / "README.md"
            document.write_text("include me", encoding="utf-8")

            self.assertEqual(list(estimator.iter_files([str(repo)])), [document])

    def test_read_text_preserves_unicode_and_replaces_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            unicode_path = root / "unicode.txt"
            invalid_path = root / "input.bin"
            unicode_path.write_text("café ☕", encoding="utf-8")
            invalid_path.write_bytes(b"good\xffbad")

            self.assertEqual(estimator.read_text(unicode_path), "café ☕")
            self.assertEqual(estimator.read_text(invalid_path), "good\ufffdbad")

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

            self.assertIn("| **Total** | 15 | 14 | 3 | 2 | 4 |", result.stdout)
            self.assertIn("est_tokens is approximate", result.stdout)

    def test_cli_reports_original_byte_size_for_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.bin"
            path.write_bytes(b"\xff\n")

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(path)],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn(
                "bytes=2 chars=2 words=1 lines=1 est_tokens=1",
                result.stdout,
            )

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

    def test_fail_on_missing_returns_nonzero_without_silent_measurement(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "does-not-exist.md",
                "--fail-on-missing",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("error: missing path: does-not-exist.md", result.stderr)
        self.assertNotIn("total:", result.stdout)


    def test_fail_on_empty_rejects_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), directory, "--fail-on-empty"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("error: no files selected for estimation", result.stderr)
            self.assertNotIn("total:", result.stdout)

    def test_fail_on_empty_rejects_fully_pruned_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generated = root / "node_modules" / "nested" / "generated.js"
            generated.parent.mkdir(parents=True)
            generated.write_text("generated content", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), directory,
                 "--fail-on-missing", "--fail-on-empty"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("error: no files selected for estimation", result.stderr)
            self.assertNotIn("total:", result.stdout)

    def test_fail_on_empty_allows_explicit_zero_byte_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "empty.md"
            source.write_text("", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(source),
                 "--fail-on-missing", "--fail-on-empty"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                "total: bytes=0 chars=0 words=0 lines=0 est_tokens=0",
                result.stdout,
            )

    def test_empty_directory_without_flag_retains_zero_total(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), directory],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                "total: bytes=0 chars=0 words=0 lines=0 est_tokens=0",
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
