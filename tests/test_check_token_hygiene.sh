#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CHECK_SCRIPT="$REPO_ROOT/scripts/check-token-hygiene.sh"
TEMP_DIRS=()

cleanup() {
  for directory in "${TEMP_DIRS[@]}"; do
    rm -rf "$directory"
  done
}
trap cleanup EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

new_repo() {
  local directory
  directory=$(mktemp -d)
  TEMP_DIRS+=("$directory")
  git -C "$directory" init -q
  printf '%s' "$directory"
}

expect_success() {
  local name="$1"
  local output
  shift

  if ! output=$("$@" 2>&1); then
    fail "$name should pass, output: $output"
  fi
}

expect_failure() {
  local name="$1"
  local expected="$2"
  local output
  shift 2

  if output=$("$@" 2>&1); then
    fail "$name should fail"
  fi

  if ! grep -Fq "$expected" <<<"$output"; then
    fail "$name missing '$expected': $output"
  fi
}

repo=$(new_repo)
printf 'small\n' > "$repo/notes with spaces.md"
git -C "$repo" add "notes with spaces.md"
expect_success \
  "staged filename with spaces" \
  bash -c "cd '$repo' && MAX_CONTEXT_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
dd if=/dev/zero of="$repo/build output.log" bs=1024 count=16 status=none
git -C "$repo" add "build output.log"
expect_failure \
  "large staged log with spaces" \
  "large-log-file: build output.log" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
dd if=/dev/zero of="$repo/context.txt" bs=1024 count=16 status=none
git -C "$repo" add context.txt
expect_failure \
  "large staged context" \
  "large-context-file: context.txt" \
  bash -c "cd '$repo' && MAX_CONTEXT_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
printf 'one\ntwo\nthree\n' > "$repo/AGENTS.md"
expect_failure \
  "oversized instruction file" \
  "instruction-too-large: AGENTS.md" \
  bash -c "cd '$repo' && MAX_INSTRUCTION_LINES=2 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
dd if=/dev/zero of="$repo/untracked.log" bs=1024 count=16 status=none
expect_success \
  "untracked files are outside staged check" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

directory=$(mktemp -d)
TEMP_DIRS+=("$directory")
dd if=/dev/zero of="$directory/fallback output.trace" bs=1024 count=16 status=none
expect_failure \
  "non-git fallback with spaces" \
  "large-log-file: fallback output.trace" \
  bash -c "cd '$directory' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

echo "token hygiene regression tests passed."
