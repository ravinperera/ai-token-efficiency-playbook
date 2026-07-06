# Token Hygiene CI

The token hygiene workflow runs `scripts/check-token-hygiene.sh` on pull requests and pushes to `main`.

The check is intentionally lightweight. It is designed to catch common sources of unnecessary AI context before they become part of the repository.

## What it checks

The script checks for:

- AI instruction files that have grown too long
- large context files that may be expensive to paste or load into agents
- large log, output, or trace files that should usually be summarised instead of committed

## Default thresholds

| Setting | Default | Purpose |
| --- | ---: | --- |
| `MAX_INSTRUCTION_LINES` | `120` lines | Keeps agent instruction files concise. |
| `MAX_CONTEXT_FILE_KB` | `256` KB | Flags large files that may create avoidable context load. |
| `MAX_LOG_FILE_KB` | `64` KB | Flags raw logs that should usually be reduced to the failing step and exact error. |

## When a failure is useful

A failure does not automatically mean the content is wrong. It means the change deserves a context-hygiene review.

Before raising a threshold, check whether the file can be improved by:

- moving detail into a focused guide
- replacing raw logs with a short failure summary
- linking to generated artifacts instead of committing them
- removing repeated instructions or stale examples

## Local usage

Run the same check locally before opening a pull request:

```bash
bash scripts/check-token-hygiene.sh
```

To test a higher threshold locally:

```bash
MAX_CONTEXT_FILE_KB=512 bash scripts/check-token-hygiene.sh
```

Only increase thresholds in CI when the larger content is useful, safe to publish, and still aligned with the playbook's goal of reducing low-value context.
