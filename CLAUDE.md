# Claude Code Token Efficiency Instructions

Use TokenSaver mode by default.

This file is a Claude-specific adapter. The canonical rules live in:

- `guidelines/token-saving-principles.md`
- `guidelines/context-hygiene.md`
- `guidelines/cli-output-compression.md`
- `guidelines/model-routing.md`
- `guidelines/coding-agent-guidelines.md`
- `guidelines/question-pause-control.md`

## Claude-Specific Behaviour

- Keep project memory short and current.
- Store durable facts only; avoid conversation filler.
- Search before reading large files or broad directories.
- Summarise tool output and logs before continuing.
- Prefer focused edits, targeted verification, and short final answers.
- Preserve exact errors, commands, paths, assumptions, and risks that affect correctness.
- Use the lowest approved model tier capable of the task when model routing is available.
- Use economy/fast routing only for bounded, low-risk work such as formatting, extraction, rewriting, or simple summarisation.
- Escalate for security, production, architecture, ambiguity, broad multi-file work, sensitive data, or a materially failed first attempt.
- If this session cannot change models, state the recommended tier rather than claiming a switch.
- Never silently change provider, data boundary, tenancy, region, retention policy, or approved model family.
- When the user asks a status, explanation, clarification, or safety question, answer and pause. Resume only after an explicit continuation phrase.
- Retry an external failure at most once, then stop with the exact blocker and required action.

## Final Answer

Use this shape unless the user asks for more detail:

1. Result.
2. Key files or actions.
3. Verification.
4. Next step, only if useful.
