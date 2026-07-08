# Per-Tool Token Waste Notes

Different AI tools can waste context in different ways. Use these notes to choose the smallest useful input for each tool.

## Codex And General Coding Agents

Common waste source: loading broad repository context before the task is scoped.

Mitigation:

- Start with the goal, target files, and verification command.
- Ask the agent to search before opening large files.
- Keep project instructions short and avoid repeating repo-wide context in every prompt.

## Claude Code

Common waste source: long memory or project instruction files that are loaded repeatedly.

Mitigation:

- Keep durable instructions focused on stable project rules.
- Move task-specific details into the current prompt only.
- Summarise previous attempts instead of pasting full conversations.

## GitHub Copilot

Common waste source: irrelevant open tabs, large files, or noisy comments affecting completion context.

Mitigation:

- Close unrelated files before requesting suggestions.
- Open the smallest relevant file range.
- Keep comments close to the code being changed.

## Cursor

Common waste source: broad `@` references and large context selections.

Mitigation:

- Reference specific files instead of folders where possible.
- Use small selections for targeted edits.
- Split large refactors into smaller changes with separate verification.

## Gemini CLI And Terminal Agents

Common waste source: full terminal output from commands that only have one useful failure line.

Mitigation:

- Pipe long output through `tail`, `grep`, or a summarising command first.
- Include command, exit status, and exact failure line.
- Avoid pasting repeated dependency install logs unless they are the failure.

## Cross-Tool Rule

For every tool, the best default is:

1. State the goal.
2. Provide the smallest relevant files or errors.
3. Say what has already been tried.
4. Ask for the smallest useful verification.
