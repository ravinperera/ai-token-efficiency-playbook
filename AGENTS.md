# Token Efficiency Instructions For AI Agents

Follow these instructions in this repository unless the user asks for more detail.

## Core Behaviour

- Answer first. Explain only what is needed.
- Remove filler, greetings, apologies, and repeated framing.
- Do not restate the user's request unless clarification is needed.
- Prefer concise bullets or short paragraphs.
- Keep final responses short and action-focused.
- Preserve technical accuracy. Do not compress so much that meaning is lost.

## Context Discipline

- Read only files relevant to the task.
- Use targeted search before opening broad files.
- Summarise large files instead of quoting them.
- Do not dump full logs, full files, or long command output unless requested.
- If output is large, extract errors, paths, commands, and key facts.
- Avoid repeating context that is already visible in the conversation.

## Tool Use

- Prefer precise commands over broad scans.
- Before running noisy commands, narrow the scope.
- When command output is long, summarise the important lines.
- Do not run unrelated checks just to be comprehensive.
- Verify changes with the smallest useful test.

## Coding Work

- Make focused edits.
- Avoid unrelated refactors.
- Follow existing project patterns.
- Report changed files and verification briefly.
- Include only code snippets that the user needs.

## Final Response Format

Default final response:

- What changed
- How it was verified
- Any remaining action

Keep it under 10 lines unless the task requires more.
