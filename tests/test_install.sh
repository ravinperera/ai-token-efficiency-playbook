#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

run_install() {
  target_dir=$1
  shift
  (
    cd "$target_dir"
    TOKEN_EFFICIENCY_SOURCE_ROOT="$ROOT" sh "$ROOT/scripts/install.sh" "$@"
  )
}

mkdir -p "$TMP/codex"
run_install "$TMP/codex" codex
cmp "$ROOT/AGENTS.md" "$TMP/codex/AGENTS.md"

printf 'keep me\n' > "$TMP/codex/AGENTS.md"
if run_install "$TMP/codex" codex >/dev/null 2>&1; then
  echo "installer unexpectedly overwrote an existing file without --force" >&2
  exit 1
fi
[ "$(cat "$TMP/codex/AGENTS.md")" = "keep me" ]

run_install "$TMP/codex" --force codex
cmp "$ROOT/AGENTS.md" "$TMP/codex/AGENTS.md"

mkdir -p "$TMP/copilot"
run_install "$TMP/copilot" copilot
cmp "$ROOT/.github/copilot-instructions.md" "$TMP/copilot/.github/copilot-instructions.md"

mkdir -p "$TMP/cursor"
run_install "$TMP/cursor" cursor
cmp "$ROOT/.cursor/rules/token-efficiency.mdc" "$TMP/cursor/.cursor/rules/token-efficiency.mdc"

if run_install "$TMP/codex" unknown >/dev/null 2>&1; then
  echo "installer unexpectedly accepted an unsupported tool" >&2
  exit 1
fi

if run_install "$TMP/codex" --source-ref >/dev/null 2>&1; then
  echo "installer unexpectedly accepted --source-ref without a value" >&2
  exit 1
fi

mkdir -p "$TMP/bin" "$TMP/remote"
cat > "$TMP/bin/curl" <<'EOF'
#!/bin/sh
set -eu
url=""
output=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    -o)
      shift
      output=$1
      ;;
    -* )
      ;;
    *)
      url=$1
      ;;
  esac
  shift
done
[ -n "$url" ]
[ -n "$output" ]
printf '%s\n' "$url" > "$TOKEN_EFFICIENCY_TEST_URL_LOG"
cp "$TOKEN_EFFICIENCY_TEST_SOURCE" "$output"
EOF
chmod +x "$TMP/bin/curl"
(
  cd "$TMP/remote"
  PATH="$TMP/bin:$PATH" \
    TOKEN_EFFICIENCY_TEST_SOURCE="$ROOT/AGENTS.md" \
    TOKEN_EFFICIENCY_TEST_URL_LOG="$TMP/url.log" \
    sh "$ROOT/scripts/install.sh" --source-ref v1.2.3 codex
)
cmp "$ROOT/AGENTS.md" "$TMP/remote/AGENTS.md"
[ "$(cat "$TMP/url.log")" = "https://raw.githubusercontent.com/ravinperera/ai-token-efficiency-playbook/v1.2.3/AGENTS.md" ]

echo "installer tests passed"
