#!/usr/bin/env bash
set -euo pipefail

MAX_INSTRUCTION_LINES="${MAX_INSTRUCTION_LINES:-120}"
MAX_CONTEXT_FILE_KB="${MAX_CONTEXT_FILE_KB:-256}"
MAX_LOG_FILE_KB="${MAX_LOG_FILE_KB:-64}"

failures=0

# Pre-commit checks must inspect the staged snapshot, not later worktree edits.
source_mode=worktree
if git rev-parse --is-inside-work-tree >/dev/null 2>&1 &&
   ! git diff --cached --quiet --; then
  source_mode=staged
fi

is_regular_file() {
  local file="$1"
  if [ "$source_mode" = staged ]; then
    local entry
    entry=$(git ls-files --stage -- "$file")
    case "$entry" in
      100644\ *|100755\ *) return 0 ;;
      *) return 1 ;;  # Ignore symlinks and gitlinks in the index.
    esac
  else
    [ -f "$file" ]
  fi
}

check_instruction_file() {
  local file="$1"

  if ! is_regular_file "$file"; then
    return 0
  fi

  local lines
  if [ "$source_mode" = staged ]; then
    lines=$(git show ":$file" | awk 'END { print NR }')
  else
    lines=$(awk 'END { print NR }' "$file")
  fi

  if [ "$lines" -gt "$MAX_INSTRUCTION_LINES" ]; then
    echo "instruction-too-large: $file has $lines lines; limit is $MAX_INSTRUCTION_LINES"
    failures=$((failures + 1))
  fi
}

check_large_file() {
  local file="$1"

  if ! is_regular_file "$file"; then
    return 0
  fi

  # Measure file contents, not disk allocation (sparse files may use no blocks).
  # Media assets are not text context or raw execution logs. Keep media policy separate.
  case "$file" in
    *.png|*.jpg|*.jpeg|*.gif|*.webp|*.ico|*.pdf)
      return 0
      ;;
  esac

  local size_bytes size_kb
  if [ "$source_mode" = staged ]; then
    size_bytes=$(git cat-file -s ":$file")
  else
    size_bytes=$(wc -c < "$file")
  fi
  size_kb=$(( (size_bytes + 1023) / 1024 ))

  case "$file" in
    *.log|*.out|*.trace)
      if [ "$size_kb" -gt "$MAX_LOG_FILE_KB" ]; then
        echo "large-log-file: $file is ${size_kb}KB; limit is ${MAX_LOG_FILE_KB}KB"
        failures=$((failures + 1))
      fi
      ;;
    *)
      if [ "$size_kb" -gt "$MAX_CONTEXT_FILE_KB" ]; then
        echo "large-context-file: $file is ${size_kb}KB; limit is ${MAX_CONTEXT_FILE_KB}KB"
        failures=$((failures + 1))
      fi
      ;;
  esac
}

check_instruction_file "AGENTS.md"
check_instruction_file "CLAUDE.md"
check_instruction_file "GEMINI.md"
check_instruction_file ".github/copilot-instructions.md"
check_instruction_file ".cursor/rules/token-efficiency.mdc"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [ "$source_mode" = worktree ]; then
    # Clean CI checkouts have no staged diff; scan tracked content instead of nothing.
    while IFS= read -r -d '' file; do
      check_large_file "$file"
    done < <(git ls-files -z)
  else
    # Pre-commit checks must use index blobs, not unstaged worktree changes.
    # Treat renames as delete/add and include type changes; only regular index files count.
    while IFS= read -r -d '' file; do
      check_large_file "$file"
    done < <(git diff --cached --no-renames --name-only --diff-filter=ACMT -z)
  fi
else
  while IFS= read -r -d '' file; do
    file="${file#./}"
    check_large_file "$file"
  done < <(find . -type f -not -path './.git/*' -print0)
fi

if [ "$failures" -gt 0 ]; then
  echo "token hygiene check failed with $failures issue(s)."
  echo "Adjust thresholds with MAX_INSTRUCTION_LINES, MAX_CONTEXT_FILE_KB, or MAX_LOG_FILE_KB."
  exit 1
fi

echo "token hygiene check passed."
