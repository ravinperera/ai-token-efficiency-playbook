# Token Efficiency Instructions For AI Agents

Use TokenSaver mode by default in this repository.

Canonical guidance lives in:

- `guidelines/token-saving-principles.md`
- `guidelines/context-hygiene.md`
- `guidelines/cli-output-compression.md`
- `guidelines/model-routing.md`
- `guidelines/coding-agent-guidelines.md`
- `checklists/token-efficiency-checklist.md`

## Agent Contract

- Answer first; explain only what changes the decision or implementation.
- Read only relevant files; search before opening broad context.
- Summarise logs, command output, and long files instead of pasting them back.
- Avoid repeating unchanged context, prior requirements, or obvious steps.
- Make focused edits and avoid unrelated refactors.
- Verify with the smallest useful command.
- Preserve accuracy over compression.

## Final Response

Default shape:

1. What changed or what was found.
2. Verification result.
3. Remaining action or risk, only if material.

Keep final responses under 10 lines unless the task requires more detail.
