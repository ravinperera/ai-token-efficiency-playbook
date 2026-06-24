# Per-Tool Token-Waste Notes

Different AI tools waste tokens in different ways. Use these notes alongside the canonical guidance in this repository.

| Tool | Common waste source | Mitigation |
| --- | --- | --- |
| Claude Code | Long `CLAUDE.md` files and repeated project memory. | Keep `CLAUDE.md` thin, link to durable docs, and summarise only current task state. |
| Codex | Broad repo scans and noisy terminal output. | Search first with `rg`, read narrow file ranges, and cap command output. |
| GitHub Copilot | Open tabs and large workspace context can influence suggestions. | Close unrelated files and keep `.github/copilot-instructions.md` short and task-focused. |
| Cursor | `@` references and broad rules can pull in too much context. | Reference specific files/folders and keep `.cursor/rules` scoped. |
| Gemini | Large prompt attachments and pasted logs can dominate the session. | Provide exact errors, relevant snippets, and a clear requested output. |

## Rule Of Thumb

If the tool lets you attach, reference, or auto-load context, treat that context as a cost. Load the smallest evidence set that can still produce a correct answer.
