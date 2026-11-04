# Context Size Estimator

Use `scripts/estimate-context-size.py` to create a quick, reproducible before/after comparison for prompts, logs, handoffs, or selected documentation files.

The helper is intentionally dependency-free. It does **not** claim exact model billing tokens. Instead, it reports stable size signals that are useful when comparing two versions of the same workflow:

- bytes
- characters
- words
- lines
- approximate tokens, estimated as characters divided by four

## Usage

Estimate one file:

```bash
python3 scripts/estimate-context-size.py prompts/debugging-mode.md
```

Estimate several files or a directory:

```bash
python3 scripts/estimate-context-size.py AGENTS.md guidelines/ templates/
```

Generate a Markdown table for a case study:

```bash
python3 scripts/estimate-context-size.py before.md after.md --markdown
```

For CI or repeatable benchmarks, require every requested input path to exist **and** at least one file to be selected after recursive exclusions:

```bash
python3 scripts/estimate-context-size.py before.md after.md --fail-on-missing --fail-on-empty
```

`--fail-on-missing` rejects nonexistent input paths. Separately, `--fail-on-empty` rejects a selection containing **no files** (for example, an empty directory or one containing only pruned dependency trees), with exit code 2 and no misleading zero-total output. A zero-byte file is still a valid, measured file and succeeds. Neither flag changes the default interactive behaviour: absent paths are warned about and skipped, and an empty selection prints a zero total.

When measuring a directory, the helper recursively skips generated or dependency
directories named `.git`, `.venv`, `venv`, `node_modules`, `__pycache__`,
or `.pytest_cache` at any depth. This keeps the default estimate focused on
the selected source context rather than installed dependencies or caches.
The exclusion applies only while walking a containing directory: pass a
specific file or subdirectory explicitly if it is genuinely part of your
context. For example:

```bash
python3 scripts/estimate-context-size.py node_modules/selected-example.js
```


## How to use the numbers

Use the same files, tool, and measurement method before and after the change. Record the result in [`templates/token-savings-measurement.md`](../templates/token-savings-measurement.md).

Good use:

- compare a raw CI log with a trimmed triage handoff
- compare a full-file prompt with a smaller file-range prompt
- compare repeated project instructions with a short canonical instruction file

Avoid:

- claiming exact billing savings from the approximate estimate alone
- comparing unrelated workflows
- including private logs, secrets, customer data, or sensitive prompts
