# Case Study: Multi-File Refactor

This case study shows how to guide a multi-file refactor without asking the AI to read an entire repository first.

## Scenario

A service needed a small refactor across application code, tests, and documentation. The original request asked the AI to scan the whole repo. The TokenSaver version named the exact behaviour change, the likely files, and the verification command.

## Before

### Prompt Shape

```text
Please review this whole repository and refactor the API error handling to be cleaner. Update anything that needs changing.

<repository attached or broad recursive scan requested>
```

### Context Included

- Full repository scan
- Unrelated directories and generated files
- Test fixtures not connected to the change
- Documentation unrelated to error handling
- No explicit acceptance criteria

### Approximate Input Size

| Item | Approximate tokens |
| --- | ---: |
| User prompt | 25 |
| Repo/file context | 24,000 |
| Total | 24,025 |

## After

### TokenSaver Prompt

```text
Refactor API error handling in TokenSaver mode.

Goal:
Return one consistent JSON error shape for validation and permission errors.

Relevant files:
- app/api/errors.py
- app/api/views.py
- tests/api/test_errors.py
- docs/api-errors.md

Acceptance:
- Existing public response fields stay compatible
- Add tests for validation and permission errors
- Update only the error-handling docs section

Verification:
pytest tests/api/test_errors.py
```

### Context Included

- Behaviour goal
- Four likely files
- Compatibility constraint
- Targeted tests
- Documentation boundary

### Approximate Input Size

| Item | Approximate tokens |
| --- | ---: |
| User prompt | 110 |
| Four relevant file snippets | 3,200 |
| Total | 3,310 |

## Result

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Approximate input tokens | 24,025 | 3,310 | -20,715 |
| Change boundary | Vague | Explicit | Improved |
| Verification | Unknown | Targeted test command | Improved |
| Risk of unrelated edits | Higher | Lower | Improved |

## Measurement Method

Save the broad prompt and the targeted prompt as text files, then compare with a tokenizer. The numbers above are example measurements for the prompt shapes, not a universal benchmark.

## Caveat

For refactors, do not over-compress acceptance criteria. The AI needs enough constraints to avoid changing public behaviour or touching unrelated files.
