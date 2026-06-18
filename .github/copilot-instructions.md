# GitHub Copilot Token Efficiency Instructions

Apply TokenSaver mode for chat, code review, and agent-style work.

Canonical guidance lives in:

- `guidelines/token-saving-principles.md`
- `guidelines/context-hygiene.md`
- `guidelines/cli-output-compression.md`
- `guidelines/model-routing.md`
- `guidelines/coding-agent-guidelines.md`

## Copilot-Specific Behaviour

- Suggest focused changes, not broad rewrites.
- Prefer minimal examples over large snippets.
- Prioritise bugs, security issues, regressions, and missing tests in reviews.
- Avoid repeating generated code that already exists in the repository.
- Summarise large outputs and ask for narrower context when the prompt is too broad.
- Preserve correctness over brevity.
