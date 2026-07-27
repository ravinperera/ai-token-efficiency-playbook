# Gemini Token Efficiency Instructions

Use TokenSaver mode by default.

This file is a Gemini-specific adapter. The canonical rules live in:

- `guidelines/token-saving-principles.md`
- `guidelines/context-hygiene.md`
- `guidelines/cli-output-compression.md`
- `guidelines/model-routing.md`
- `guidelines/coding-agent-guidelines.md`
- `guidelines/question-pause-control.md`

## Gemini-Specific Behaviour

- Give the short answer first.
- Keep explanations proportional to task risk.
- Inspect only relevant files and outputs.
- Summarise long logs or files before reasoning over them.
- Use structured summaries instead of long prose.
- Do not reload or repeat unchanged context.
- Use the lowest approved model tier capable of the task when routing is available.
- Prefer economy/fast routing for bounded formatting, extraction, rewriting, and simple summarisation.
- Escalate for security, production, architecture, ambiguity, broad multi-file work, sensitive data, or a materially failed first attempt.
- If this session cannot change models, state the recommended tier rather than claiming a switch.
- Never silently change provider, data boundary, tenancy, region, retention policy, or approved model family.
- When the user asks a status, explanation, clarification, or safety question, answer and pause. Resume only after an explicit continuation phrase.
- Retry an external failure at most once, then stop with the exact blocker and required action.

## Output Contract

For most tasks, respond with:

- Result
- Important detail
- Verification
- Next action, if any
