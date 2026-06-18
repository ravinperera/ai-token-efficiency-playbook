# Gemini Token Efficiency Instructions

Use TokenSaver mode by default.

This file is a Gemini-specific adapter. The canonical rules live in:

- `guidelines/token-saving-principles.md`
- `guidelines/context-hygiene.md`
- `guidelines/cli-output-compression.md`
- `guidelines/model-routing.md`
- `guidelines/coding-agent-guidelines.md`

## Gemini-Specific Behaviour

- Give the short answer first.
- Keep explanations proportional to task risk.
- Inspect only relevant files and outputs.
- Summarise long logs or files before reasoning over them.
- Use structured summaries instead of long prose.
- Do not reload or repeat unchanged context.

## Output Contract

For most tasks, respond with:

- Result
- Important detail
- Verification
- Next action, if any
