#!/usr/bin/env python3
"""Estimate prompt/context size for before/after AI workflows.

This intentionally avoids model-specific tokenization dependencies. It reports bytes,
characters, words, lines, and a rough token estimate so contributors can compare
context size consistently without claiming exact billing numbers.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Iterable


def iter_files(paths: Iterable[str]) -> Iterable[Path]:
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and ".git" not in child.parts:
                    yield child
        elif path.is_file():
            yield path
        else:
            print(f"warning: skipped missing path: {path}", file=sys.stderr)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def estimate_tokens(text: str) -> int:
    # A conservative, dependency-free approximation commonly used for English text.
    # Real token counts vary by model, language, formatting, and tokenizer.
    return max(1, round(len(text) / 4)) if text else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate context size for files or directories without model-specific tokenization."
    )
    parser.add_argument("paths", nargs="+", help="Files or directories to estimate")
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Print a Markdown table suitable for case studies",
    )
    args = parser.parse_args()

    rows: list[tuple[str, int, int, int, int, int]] = []
    totals = [0, 0, 0, 0, 0]

    for path in iter_files(args.paths):
        text = read_text(path)
        byte_count = len(text.encode("utf-8"))
        char_count = len(text)
        word_count = len(text.split())
        line_count = text.count("\n") + (1 if text else 0)
        token_estimate = estimate_tokens(text)
        rows.append((str(path), byte_count, char_count, word_count, line_count, token_estimate))
        totals[0] += byte_count
        totals[1] += char_count
        totals[2] += word_count
        totals[3] += line_count
        totals[4] += token_estimate

    if args.markdown:
        print("| Path | Bytes | Characters | Words | Lines | Est. tokens |")
        print("| --- | ---: | ---: | ---: | ---: | ---: |")
        for row in rows:
            print(f"| `{row[0]}` | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} |")
        print(f"| **Total** | {totals[0]} | {totals[1]} | {totals[2]} | {totals[3]} | {totals[4]} |")
    else:
        for row in rows:
            print(
                f"{row[0]}: bytes={row[1]} chars={row[2]} words={row[3]} "
                f"lines={row[4]} est_tokens={row[5]}"
            )
        print(
            f"total: bytes={totals[0]} chars={totals[1]} words={totals[2]} "
            f"lines={totals[3]} est_tokens={totals[4]}"
        )

    print("note: est_tokens is approximate; use your model/tool tokenizer for exact billing numbers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
