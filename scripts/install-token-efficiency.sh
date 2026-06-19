#!/usr/bin/env sh
set -eu

TOOL="${1:-}"
FORCE="false"

if [ "$TOOL" = "--help" ] || [ "$TOOL" = "-h" ] || [ -z "$TOOL" ]; then
  cat <<'USAGE'
Usage: sh scripts/install-token-efficiency.sh <tool> [--force]

Tools:
  claude   -> CLAUDE.md
  codex    -> AGENTS.md
  gemini   -> GEMINI.md
  copilot  -> .github/copilot-instructions.md
  cursor   -> .cursor/rules/token-efficiency.mdc

Examples:
  sh scripts/install-token-efficiency.sh codex
  sh scripts/install-token-efficiency.sh cursor --force
USAGE
  exit 0
fi

if [ "${2:-}" = "--force" ]; then
  FORCE="true"
fi

case "$TOOL" in
  claude)
    SOURCE_URL="https://raw.githubusercontent.com/ravinperera/ai-token-efficiency-playbook/main/CLAUDE.md"
    DEST="CLAUDE.md"
    ;;
  codex)
    SOURCE_URL="https://raw.githubusercontent.com/ravinperera/ai-token-efficiency-playbook/main/AGENTS.md"
    DEST="AGENTS.md"
    ;;
  gemini)
    SOURCE_URL="https://raw.githubusercontent.com/ravinperera/ai-token-efficiency-playbook/main/GEMINI.md"
    DEST="GEMINI.md"
    ;;
  copilot)
    SOURCE_URL="https://raw.githubusercontent.com/ravinperera/ai-token-efficiency-playbook/main/.github/copilot-instructions.md"
    DEST=".github/copilot-instructions.md"
    ;;
  cursor)
    SOURCE_URL="https://raw.githubusercontent.com/ravinperera/ai-token-efficiency-playbook/main/.cursor/rules/token-efficiency.mdc"
    DEST=".cursor/rules/token-efficiency.mdc"
    ;;
  *)
    echo "Unknown tool: $TOOL" >&2
    echo "Supported: claude, codex, gemini, copilot, cursor" >&2
    exit 2
    ;;
esac

if [ -e "$DEST" ] && [ "$FORCE" != "true" ]; then
  echo "Refusing to overwrite existing file: $DEST" >&2
  echo "Re-run with --force if you want to replace it." >&2
  exit 3
fi

mkdir -p "$(dirname "$DEST")"

tmp_file="$(mktemp)"
if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$SOURCE_URL" -o "$tmp_file"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$tmp_file" "$SOURCE_URL"
else
  echo "curl or wget is required." >&2
  rm -f "$tmp_file"
  exit 4
fi

mv "$tmp_file" "$DEST"
echo "Installed Token Efficiency instructions for $TOOL at $DEST"
