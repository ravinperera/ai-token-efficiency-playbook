# Case Study Template

Use this template when submitting measured before/after examples.

## Scenario

Describe the task and why token waste appeared.

## Before

### Prompt Shape

```text
Paste or summarise the original prompt shape here.
```

### Approximate Input Size

```bash
python3 scripts/count-tokens.py before-prompt.txt
```

| Item | Approximate tokens |
| --- | ---: |
| Prompt/context | TODO |
| Total | TODO |

## After

### TokenSaver Prompt

```text
Paste the reduced prompt shape here.
```

### Approximate Input Size

```bash
python3 scripts/count-tokens.py after-prompt.txt
```

| Item | Approximate tokens |
| --- | ---: |
| Prompt/context | TODO |
| Total | TODO |

## Result

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Approximate input tokens | TODO | TODO | TODO |
| Correctness retained | TODO | TODO | TODO |

## Measurement Method

Record:

- tool and model
- tokenizer or approximation used
- commands used to count tokens
- whether follow-up prompts were needed
- caveats that could affect the numbers

Do not make fixed-percentage claims. Savings depend on task, tool, model, and loaded context.
