# CLI Output Compression

Terminal output can burn tokens quickly. Do not paste everything unless everything matters.

## Compress Logs Into This Shape

```text
Command:
<command run>

Error:
<exact error line>

Relevant context:
<2-5 lines around the failure>

What changed recently:
<short note>
```

## Examples

Bad:

```text
Here are 3,000 lines of CI logs...
```

Good:

```text
Command: terraform plan
Error: Unsupported attribute at modules/ecs/main.tf:42
Relevant: module output does not expose target_group_arn
Recent change: split ALB and ECS service components
```

## Useful Shell Patterns

Use targeted filters before sending output to AI:

```bash
terraform plan 2>&1 | tail -80
```

```bash
pytest tests/test_api.py -q
```

```bash
rg "error|failed|exception|unsupported|denied" logs.txt
```

## Rule

Send the smallest output that preserves the failure signal.
