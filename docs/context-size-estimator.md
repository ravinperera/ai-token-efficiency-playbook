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
