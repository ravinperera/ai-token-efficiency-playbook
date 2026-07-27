# Token Efficiency Instructions For AI Agents

Use TokenSaver mode by default in this repository.

Canonical guidance lives in:

- `guidelines/token-saving-principles.md`
- `guidelines/context-hygiene.md`
- `guidelines/cli-output-compression.md`
- `guidelines/model-routing.md`
- `guidelines/coding-agent-guidelines.md`
- `guidelines/question-pause-control.md`
- `checklists/token-efficiency-checklist.md`

## Agent Contract

- Answer first; explain only what changes the decision or implementation.
- Read only relevant files; search before opening broad context.
- Summarise logs, command output, and long files instead of pasting them back.
- Avoid repeating unchanged context, prior requirements, or obvious steps.
- Make focused edits and avoid unrelated refactors.
- Verify with the smallest useful command.
- Preserve accuracy over compression.
- Use the lowest approved model tier capable of the task when the host supports routing.
- Prefer economy/fast models for bounded formatting, extraction, rewriting, and simple summarisation.
- Escalate for security, production, architecture, ambiguity, broad multi-file work, sensitive data, or a materially failed first attempt.
- If the host cannot switch models, state the recommended tier; never pretend a switch occurred.
- Never silently switch provider, tenancy, region, retention policy, approved model family, or data boundary.

## Questions Pause Execution

When the user asks a status, explanation, clarification, or safety question:

- answer the question first and stop;
- do not run commands, edit files, poll, retry, open or merge PRs, or continue unrelated work;
- disclose any already-running asynchronous work without launching more;
- resume only after the user explicitly says `continue`, `proceed`, `approved`, `go ahead`, or `try again`.

Retry an external failure at most once. If it still fails, stop and report the exact blocker plus the single action needed.

## Final Response

Default shape:

1. What changed or what was found.
2. Verification result.
3. Remaining action or risk, only if material.

Keep final responses under 10 lines unless the task requires more detail.
