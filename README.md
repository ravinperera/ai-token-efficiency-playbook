# AI Token Efficiency Playbook

Drop-in instructions, prompts, and workflows to reduce token usage across Codex, Claude Code, GitHub Copilot, Cursor, Gemini, and other AI coding agents.

This project is not just about making AI replies shorter. The bigger goal is to reduce waste across the whole AI workflow: noisy prompts, oversized context, repeated explanations, full log dumps, unnecessary file reads, verbose memory files, and using expensive models for simple tasks.

## What This Provides

Ready-to-copy instruction files for common AI coding tools:

```text
.
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── .github/
│   └── copilot-instructions.md
├── .cursor/
│   └── rules/
│       └── token-efficiency.mdc
├── prompts/
│   ├── tokensaver-mode.md
│   ├── debugging-mode.md
│   ├── code-review-mode.md
│   └── architecture-mode.md
├── guidelines/
│   ├── token-saving-principles.md
│   ├── coding-agent-guidelines.md
│   ├── context-hygiene.md
│   ├── cli-output-compression.md
│   └── model-routing.md
├── examples/
│   ├── before-after-prompts.md
│   └── bad-vs-good-context.md
└── checklists/
    └── token-efficiency-checklist.md
```

## The Standard

AI agents should:

- Answer first, explain only when useful.
- Remove filler, greetings, apologies, and repeated framing.
- Read only relevant files.
- Summarise large logs instead of repeating them.
- Avoid restating unchanged context.
- Prefer concise diffs, focused commands, and short verification notes.
- Ask before scanning large directories or dumping large files.
- Keep persistent instruction/memory files short.
- Use cheaper or faster models for simple work where possible.
- Preserve technical accuracy over extreme compression.

## Quick Install

Copy the instruction file for your tool into your project:

| Tool | File |
| --- | --- |
| Codex / general agents | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI / agents | `GEMINI.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/token-efficiency.mdc` |

## Why This Matters

Token waste normally comes from four places:

1. Oversized input context.
2. Noisy tool and terminal output.
3. Repeated project memory and instructions.
4. Verbose AI responses.

Short replies help, but context hygiene usually saves more.

## Example Token-Saver Prompt

```text
Use token-efficient mode for this task.
Answer first. No filler. Read only relevant files. Summarise large outputs. Do not repeat unchanged context. Keep final response short unless I ask for detail.
```

## What This Is Not

This is not a benchmark claim that every workflow saves a fixed percentage. Token savings depend on the task, model, tool, and how much context is loaded. The aim is practical reduction without making the AI less useful.

## Recommended Use

Use this playbook when working with:

- AI coding agents
- terminal-based AI tools
- large codebases
- CI/CD logs
- infrastructure-as-code projects
- long debugging sessions
- repeated review or refactor workflows

## Contributing

Contributions are welcome. Useful additions include new tool-specific instruction files, before/after examples, workflow patterns, and measured token-saving case studies.
