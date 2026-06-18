# Claude Code Token Efficiency Instructions

Use TokenSaver mode by default.

This file is a Claude-specific adapter. The canonical rules live in:

- `guidelines/token-saving-principles.md`
- `guidelines/context-hygiene.md`
- `guidelines/cli-output-compression.md`
- `guidelines/model-routing.md`
- `guidelines/coding-agent-guidelines.md`

## Claude-Specific Behaviour

- Keep project memory short and current.
- Store durable facts only; avoid conversation filler.
- Search before reading large files or broad directories.
- Summarise tool output and logs before continuing.
- Prefer focused edits, targeted verification, and short final answers.
- Preserve exact errors, commands, paths, assumptions, and risks that affect correctness.

## Final Answer

Use this shape unless the user asks for more detail:

1. Result.
2. Key files or actions.
3. Verification.
4. Next step, only if useful.
