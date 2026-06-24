# Token-Waste Anti-Patterns

Use this catalogue to spot common ways AI sessions become expensive, slow, or noisy.

| Anti-pattern | Why it wastes tokens | One-line fix |
| --- | --- | --- |
| Full-repo dump | Loads unrelated files before the task is understood. | Start with `rg`, file names, and the smallest relevant snippets. |
| Re-pasting whole logs | Repeats successful setup output and hides the real error. | Paste only the failed step, exact error, and nearby context. |
| Giant memory files | Every session carries stale instructions and old decisions. | Keep persistent memory short and archive old context into docs. |
| Restating unchanged context | Burns tokens on facts already established. | Say what changed since the last message. |
| Wrong model for the task | Expensive reasoning models get used for formatting or extraction. | Route simple tasks to cheaper/faster models where available. |
| Screenshot-only debugging | Forces the model to infer text from an image. | Provide exact error text and only use screenshots for visual state. |
| Broad refactor request | Encourages unrelated edits across many files. | Name the target behaviour, likely files, and verification command. |
| Unbounded tool output | Terminal commands return thousands of irrelevant lines. | Use filters, limits, summaries, or save logs to files and quote excerpts. |

## Use With The Checklist

Before asking an AI agent to continue, check whether the next prompt adds new signal or just repeats old context. If it repeats old context, summarise the delta instead.
