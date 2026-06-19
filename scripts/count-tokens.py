#!/usr/bin/env python3
"""Count tokens for a file or stdin.

Uses tiktoken when installed. Falls back to a documented approximation when it
is not available, so the script remains useful in lightweight environments.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read_input(path: str | None) -> str:
    if path and path != "-":
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def approximate_tokens(text: str) -> int:
    # Rough approximation: words/punctuation plus a small allowance for spacing.
    # This is not model-exact, but is stable enough for before/after comparison.
    pieces = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    return max(1, int(len(pieces) * 1.15)) if text else 0


def tiktoken_count(text: str, encoding_name: str) -> int | None:
    try:
        import tiktoken  # type: ignore
    except Exception:
        return None

    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def main() -> int:
    parser = argparse.ArgumentParser(description="Count tokens for a file or stdin.")
    parser.add_argument("path", nargs="?", help="File to count. Use '-' or omit for stdin.")
    parser.add_argument(
        "--encoding",
        default="cl100k_base",
        help="tiktoken encoding to use when tiktoken is installed. Default: cl100k_base",
    )
    parser.add_argument(
        "--approx-only",
        action="store_true",
        help="Skip tiktoken and use the deterministic approximation.",
    )
    args = parser.parse_args()

    text = read_input(args.path)
    count = None if args.approx_only else tiktoken_count(text, args.encoding)
    method = "tiktoken" if count is not None else "approximation"

    if count is None:
        count = approximate_tokens(text)

    source = args.path or "stdin"
    print(f"{count}\t{method}\t{source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
