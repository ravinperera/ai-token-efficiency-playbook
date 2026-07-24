#!/usr/bin/env bash
set -euo pipefail

MAX_INSTRUCTION_LINES="${MAX_INSTRUCTION_LINES:-120}"
MAX_CONTEXT_FILE_KB="${MAX_CONTEXT_FILE_KB:-256}"
MAX_LOG_FILE_KB="${MAX_LOG_FILE_KB:-64}"

failures=0

check_instruction_file() {
  local file="$1"

  if [ ! -f "$file" ]; then
    return 0
  fi

  local lines
  lines=$(wc -l < "$file" | tr -d ' ')

  if [ "$lines" -gt "$MAX_INSTRUCTION_LINES" ]; then
    echo "instruction-too-large: $file has $lines lines; limit is $MAX_INSTRUCTION_LINES"
    failures=$((failures + 1))
  fi
}

check_large_file() {
  local file="$1"

  if [ ! -f "$file" ]; then
    return 0
  fi

  local size_kb
  size_kb=$(du -k "$file" | awk '{print $1}')

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
  while IFS= read -r -d '' file; do
    check_large_file "$file"
  done < <(git diff --cached --name-only --diff-filter=ACM -z)
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
