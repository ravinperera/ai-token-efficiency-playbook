# Gemini Token Efficiency Instructions

Use this repository in token-efficient mode.

## Default Mode

- Short answer first.
- No filler.
- No unnecessary repetition.
- Keep explanations proportional to task risk.
- Prefer structured summaries over long prose.

## File And Context Handling

- Inspect only relevant files.
- Search before opening large files.
- Summarise large files or logs.
- Avoid pasting full command output back to the user.
- Do not reload unchanged context.

## Engineering Tasks

- Follow existing patterns.
- Keep edits narrow.
- Verify with targeted commands.
- Mention only material findings.
- Avoid generic advice unless requested.

## Output Contract

For most tasks, respond with:

- Result
- Important detail
- Verification
- Next action, if any
