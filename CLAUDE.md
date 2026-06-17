# Claude Code Token Efficiency Instructions

Use token-efficient mode by default.

## Response Style

- Be concise.
- Skip filler and preambles.
- Give the answer first.
- Use detail only when it changes the decision or implementation.
- Do not repeat the user's request.
- Do not narrate obvious steps.

## Project Work

- Search before reading large files.
- Read only relevant files.
- Summarise large outputs.
- Avoid full-file dumps unless explicitly requested.
- Prefer direct edits and focused verification.
- Do not perform broad refactors without need.

## Debugging

- Identify the likely failure point first.
- Ask for missing high-value information only when blocked.
- Prefer one focused test over many noisy commands.
- Report the exact failing signal, not the full log.

## Memory Hygiene

- Keep project memory short.
- Store durable facts, not conversation filler.
- Remove stale or duplicated instructions.
- Prefer compact checklists over long prose.

## Final Answer

Keep final answers short:

1. Done / result.
2. Key files or actions.
3. Verification.
4. Next step only if useful.
