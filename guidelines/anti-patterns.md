# Token Waste Anti-Patterns

Use this catalogue to spot common ways engineering workflows accidentally send too much low-value context to AI tools.

| Anti-pattern | Why it wastes tokens | Better approach |
| --- | --- | --- |
| Full repository dump | Most files are irrelevant to the current task. | Search first, then open only the smallest relevant files. |
| Whole CI log paste | Repeated setup output hides the real failure. | Paste the failing step, exact error, and a short summary of surrounding context. |
| Reposting unchanged context | The model has to reprocess information it already has. | State what changed since the last message. |
| Oversized memory files | Persistent instructions are loaded repeatedly. | Keep durable instructions short, current, and scoped to real preferences. |
| Wrong model for the task | Expensive reasoning is wasted on formatting or extraction. | Route simple tasks to cheaper or faster models where quality allows. |
| Screenshot-first debugging | Images are expensive and often less searchable than text. | Prefer logs, commands, file paths, and exact error messages. |
| Unbounded refactor requests | The assistant may inspect too many files before choosing a plan. | Name the target files, goal, constraints, and verification method. |
| Repeating boilerplate instructions | Long generic rules crowd out task-specific facts. | Keep reusable rules in project files and reference them briefly. |

## Review Checklist

Before sending context to an AI tool, ask:

- Can I remove any content that is not directly relevant?
- Did I include the exact error or decision needed?
- Can a file range replace a full file?
- Can a summary replace a long log?
- Did I explain what has changed since the last attempt?
