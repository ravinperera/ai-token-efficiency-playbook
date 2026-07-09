---
name: New tool instruction file
description: Suggest support for another AI tool or coding agent
title: "Add instruction file for <tool>"
labels: [documentation, enhancement]
---

## Tool

Name of the AI tool or coding agent:

## Why it should be supported

Explain who would use it and what token/context problem this instruction file should solve.

## Expected file location

Example: `.github/copilot-instructions.md`, `.cursor/rules/token-efficiency.mdc`, or another tool-specific path.

## Guidance to include

- Context hygiene rules:
- Model/tool routing notes:
- Log/output compression notes:
- Safety or accuracy caveats:

## Validation

- [ ] The instruction file is short and tool-specific.
- [ ] It links back to the canonical guidance in `guidelines/` where useful.
- [ ] It avoids fixed percentage token-saving claims unless measured.
