#!/bin/sh
set -eu

BASE_URL="${TOKEN_EFFICIENCY_BASE_URL:-https://raw.githubusercontent.com/ravinperera/ai-token-efficiency-playbook/main}"
SOURCE_ROOT="${TOKEN_EFFICIENCY_SOURCE_ROOT:-}"
force=0
tool=""

usage() {
  cat <<'EOF'
Usage: install.sh [--force] <codex|claude|gemini|copilot|cursor>

Installs the matching token-efficiency instruction file into the current repository.
Existing files are never overwritten unless --force is supplied.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --force)
      force=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [ -n "$tool" ]; then
        echo "Only one tool may be selected." >&2
        usage >&2
        exit 2
      fi
      tool="$1"
      ;;
  esac
  shift
done

if [ -z "$tool" ]; then
  usage >&2
  exit 2
fi

case "$tool" in
  codex|agents)
    source_path="AGENTS.md"
    destination="AGENTS.md"
    ;;
  claude)
    source_path="CLAUDE.md"
    destination="CLAUDE.md"
    ;;
  gemini)
    source_path="GEMINI.md"
    destination="GEMINI.md"
    ;;
  copilot)
    source_path=".github/copilot-instructions.md"
    destination=".github/copilot-instructions.md"
    ;;
  cursor)
    source_path=".cursor/rules/token-efficiency.mdc"
    destination=".cursor/rules/token-efficiency.mdc"
    ;;
  *)
    echo "Unsupported tool: $tool" >&2
    usage >&2
    exit 2
    ;;
esac

if [ -e "$destination" ] && [ "$force" -ne 1 ]; then
  echo "Refusing to overwrite existing $destination. Re-run with --force to replace it." >&2
  exit 3
fi

parent=$(dirname "$destination")
if [ "$parent" != "." ]; then
  mkdir -p "$parent"
fi

if [ -n "$SOURCE_ROOT" ]; then
  cp "$SOURCE_ROOT/$source_path" "$destination"
else
  command -v curl >/dev/null 2>&1 || {
    echo "curl is required when TOKEN_EFFICIENCY_SOURCE_ROOT is not set." >&2
    exit 4
  }
  tmp="${destination}.tmp.$$"
  trap 'rm -f "$tmp"' EXIT HUP INT TERM
  curl -fsSL "$BASE_URL/$source_path" -o "$tmp"
  mv "$tmp" "$destination"
  trap - EXIT HUP INT TERM
fi

echo "Installed $destination for $tool."
