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
printf 'one\ntwo\nthree' > "$repo/AGENTS.md"
expect_failure \
  "oversized instruction file without final newline" \
  "instruction-too-large: AGENTS.md has 3 lines" \
  bash -c "cd '$repo' && MAX_INSTRUCTION_LINES=2 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
dd if=/dev/zero of="$repo/untracked.log" bs=1024 count=16 status=none
expect_success \
  "untracked files are outside staged check" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
truncate -s 16384 "$repo/committed.log"
git -C "$repo" add committed.log
git -C "$repo" -c user.name=Fixture -c user.email=fixture@example.invalid commit -qm "Add log fixture"
expect_failure \
  "large committed log in clean checkout" \
  "large-log-file: committed.log" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
truncate -s 16384 "$repo/committed.txt"
git -C "$repo" add committed.txt
git -C "$repo" -c user.name=Fixture -c user.email=fixture@example.invalid commit -qm "Add text fixture"
expect_failure \
  "large committed context in clean checkout" \
  "large-context-file: committed.txt" \
  bash -c "cd '$repo' && MAX_CONTEXT_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
truncate -s 16384 "$repo/illustration.png"
git -C "$repo" add illustration.png
git -C "$repo" -c user.name=Fixture -c user.email=fixture@example.invalid commit -qm "Add media fixture"
expect_success \
  "non-text media excluded from text thresholds" \
  bash -c "cd '$repo' && MAX_CONTEXT_FILE_KB=4 bash '$CHECK_SCRIPT'"

directory=$(mktemp -d)
TEMP_DIRS+=("$directory")
dd if=/dev/zero of="$directory/fallback output.trace" bs=1024 count=16 status=none
expect_failure \
  "non-git fallback with spaces" \
  "large-log-file: fallback output.trace" \
  bash -c "cd '$directory' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"


# Disk allocation differs from logical size on sparse and tiny files.
repo=$(new_repo)
truncate -s 16384 "$repo/sparse.log"
git -C "$repo" add sparse.log
expect_failure \
  "sparse staged log above limit" \
  "large-log-file: sparse.log is 16KB; limit is 4KB" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
printf 'x' > "$repo/tiny.log"
git -C "$repo" add tiny.log
expect_success \
  "one-byte file below 1KB limit" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=1 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
printf 'x' > "$repo/-flag.log"
git -C "$repo" add -- -flag.log
expect_success \
  "staged filename beginning with a dash" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=1 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
truncate -s 4096 "$repo/boundary.log"
git -C "$repo" add boundary.log
expect_success \
  "exact 4KB limit" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"
truncate -s 4097 "$repo/boundary.log"
git -C "$repo" add boundary.log
expect_failure \
  "one byte above 4KB limit" \
  "large-log-file: boundary.log is 5KB; limit is 4KB" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"


# Staged checks must read the Git index rather than subsequent worktree edits.
repo=$(new_repo)
truncate -s 16384 "$repo/staged-large.log"
git -C "$repo" add staged-large.log
printf 'small\n' > "$repo/staged-large.log"
expect_failure \
  "large staged log despite smaller worktree" \
  "large-log-file: staged-large.log" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
printf 'small\n' > "$repo/staged-small.log"
git -C "$repo" add staged-small.log
truncate -s 16384 "$repo/staged-small.log"
expect_success \
  "small staged log despite larger unstaged worktree" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
truncate -s 16384 "$repo/removed-worktree.log"
git -C "$repo" add removed-worktree.log
rm "$repo/removed-worktree.log"
expect_failure \
  "large staged log missing from worktree" \
  "large-log-file: removed-worktree.log" \
  bash -c "cd '$repo' && MAX_LOG_FILE_KB=4 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
printf 'one\ntwo\nthree\n' > "$repo/AGENTS.md"
git -C "$repo" add AGENTS.md
printf 'one\n' > "$repo/AGENTS.md"
expect_failure \
  "long staged instructions despite shorter worktree" \
  "instruction-too-large: AGENTS.md has 3 lines" \
  bash -c "cd '$repo' && MAX_INSTRUCTION_LINES=2 bash '$CHECK_SCRIPT'"

repo=$(new_repo)
printf 'one\n' > "$repo/AGENTS.md"
git -C "$repo" add AGENTS.md
printf 'one\ntwo\nthree\n' > "$repo/AGENTS.md"
expect_success \
  "short staged instructions despite longer worktree" \
  bash -c "cd '$repo' && MAX_INSTRUCTION_LINES=2 bash '$CHECK_SCRIPT'"

echo "token hygiene regression tests passed."
