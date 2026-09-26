from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "estimate-context-size.py"
SPEC = importlib.util.spec_from_file_location("estimate_context_size_dedup", SCRIPT_PATH)
assert SPEC and SPEC.loader
estimator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = estimator
SPEC.loader.exec_module(estimator)


class ContextPathDedupTests(unittest.TestCase):
    def test_directory_and_nested_file_are_counted_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first.md"
            second = root / "second.md"
            first.write_text("first\n", encoding="utf-8")
            second.write_text("second\n", encoding="utf-8")

            files = list(estimator.iter_files([str(root), str(first)]))

            self.assertEqual(files, [first, second])

    def test_first_seen_display_path_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            target = nested / "context.md"
            target.write_text("context\n", encoding="utf-8")

            files = list(estimator.iter_files([str(target), str(root)]))

            self.assertEqual(files, [target])


if __name__ == "__main__":
    unittest.main()
