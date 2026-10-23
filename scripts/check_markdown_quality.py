#!/usr/bin/env python3
"""Validate Markdown formatting and repository-local links without dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXCLUDED_PARTS = {".git", ".venv", "node_modules", "__pycache__"}
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "data:",
    "ftp://",
    "//",
)


def markdown_files(root: Path) -> list[Path]:
    """Return Markdown files in deterministic order, excluding generated trees."""
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_PARTS for part in relative_parts):
            continue
        files.append(path)
    return files


def scan_markdown(text: str) -> tuple[str, list[str]]:
    """Mask fenced code and check formatting in a single length-aware pass."""
    searchable_lines: list[str] = []
    errors: list[str] = []
    active_fence: str | None = None
    active_line = 0

    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        raw_line = line.rstrip("\r\n")
        match = FENCE_RE.match(raw_line)
        if active_fence is None:
            if match and (match.group(1)[0] != "`" or "`" not in match.group(2)):
                active_fence = match.group(1)
                active_line = line_number
                searchable_lines.append("\n" if line.endswith("\n") else "")
                continue
            if raw_line.rstrip(" \t") != raw_line:
                errors.append(f"line {line_number}: trailing whitespace")
            searchable_lines.append(line)
        else:
            if (
                match
                and match.group(1)[0] == active_fence[0]
                and len(match.group(1)) >= len(active_fence)
                and not match.group(2).strip()
            ):
                active_fence = None
                active_line = 0
            searchable_lines.append("\n" if line.endswith("\n") else "")

    if active_fence is not None:
        errors.append(
            f"line {active_line}: unclosed Markdown fence starting with {active_fence}"
        )
    return "".join(searchable_lines), errors


def destination_path(raw_destination: str) -> str | None:
    """Extract a local path from a Markdown link destination."""
    destination = raw_destination.strip()
    if destination.startswith("<") and ">" in destination:
        destination = destination[1 : destination.index(">")]
    else:
        destination = destination.split(maxsplit=1)[0]

    if not destination or destination.startswith("#"):
        return None
    lowered = destination.lower()
    if lowered.startswith(EXTERNAL_PREFIXES):
        return None

    parsed = urlsplit(destination)
    if parsed.scheme:
        return None
    return unquote(parsed.path)


def validate_local_link(
    root: Path, source: Path, raw_destination: str
) -> str | None:
    """Return an error for a missing or out-of-repository local link."""
    local_path = destination_path(raw_destination)
    if local_path is None or local_path == "":
        return None

    if local_path.startswith("/"):
        candidate = root / local_path.lstrip("/")
    else:
        candidate = source.parent / local_path

    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError:
        return f"link escapes the repository: {raw_destination}"

    if not resolved_candidate.exists():
        return f"missing local link target: {raw_destination}"
    return None


def validate_markdown(root: Path, path: Path) -> list[str]:
    """Validate one Markdown file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"cannot read as UTF-8: {exc}"]

    errors: list[str] = []
    if "\x00" in text:
        errors.append("contains a NUL byte")

    searchable_text, formatting_errors = scan_markdown(text)
    errors.extend(formatting_errors)
    destinations = [
        match.group(1) for match in INLINE_LINK_RE.finditer(searchable_text)
    ]
    destinations.extend(
        match.group(1) for match in REFERENCE_LINK_RE.finditer(searchable_text)
    )
    for destination in destinations:
        error = validate_local_link(root, path, destination)
        if error is not None:
            errors.append(error)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Markdown formatting and repository-local links."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current directory.",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    files = markdown_files(root)
    for path in files:
        relative_path = path.relative_to(root)
        errors.extend(
            f"{relative_path}: {error}"
            for error in validate_markdown(root, path)
        )

    if errors:
        print("Markdown quality checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Markdown quality checks passed for {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
