# AI Token Efficiency Playbook

[![Token hygiene](https://github.com/ravinperera/ai-token-efficiency-playbook/actions/workflows/token-hygiene.yml/badge.svg)](https://github.com/ravinperera/ai-token-efficiency-playbook/actions/workflows/token-hygiene.yml)

Drop-in instructions, prompts, examples, and lightweight checks to reduce wasted AI tokens across Codex, Claude Code, GitHub Copilot, Cursor, Gemini, and other AI coding agents.

This project is not just about making AI replies shorter. The main thesis is:

> Context is more expensive than reply style.

Most token waste comes from oversized context, repeated memory, noisy logs, and using the wrong model for the job. This playbook focuses on **context hygiene** and **model routing** so AI tools stay useful without carrying unnecessary token load.

## 30-Second Install

Pick your tool, copy the matching file into your repository, and commit it.

| Tool | Copy this file |
| --- | --- |
| Codex / general coding agents | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI / agents | `GEMINI.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/token-efficiency.mdc` |

```bash
cp AGENTS.md /path/to/your-repo/AGENTS.md
```

For best results, also copy the canonical guidance in `guidelines/` and the checklist in `checklists/token-efficiency-checklist.md`.

## What This Provides

Ready-to-copy instruction files and supporting material:

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
│   ├── bad-vs-good-context.md
│   └── case-study-ci-log-triage.md
├── scripts/
│   └── check-token-hygiene.sh
├── templates/
│   └── token-savings-measurement.md
└── checklists/
    └── token-efficiency-checklist.md
```

## The Standard

The canonical rules live in `guidelines/`. Tool-specific files such as `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are intentionally thin adapters.

AI agents should:

- Use context hygiene before optimizing response style.
- Search before reading large files.
- Read the smallest relevant file range.
- Summarise large logs instead of repeating them.
- Avoid restating unchanged context.
- Keep persistent instruction and memory files short.
- Use cheaper or faster models for simple tasks where appropriate.
- Preserve technical accuracy over extreme compression.

## Why This Matters

Token waste normally comes from four places:

1. Oversized input context: whole repos, full files, screenshots, and long chat history.
2. Noisy tool output: full CI logs, Terraform plans, stack traces, and terminal dumps.
3. Repeated instructions: duplicated memory files, repeated project rules, and stale context.
4. Poor model routing: using high-cost reasoning models for simple formatting, summarisation, or extraction.

Short replies help, but context hygiene usually saves more.

## Example Token-Saver Prompt

```text
Use TokenSaver mode for this task.
Answer first. Read only relevant files. Summarise large outputs. Do not repeat unchanged context. Use the smallest useful verification. Keep final response short unless I ask for detail.
```

## Optional Local Check

Run the lightweight hygiene check before committing AI instruction files or logs:

```bash
bash scripts/check-token-hygiene.sh
```

With pre-commit:

```bash
pip install pre-commit
pre-commit run --all-files
```

## FAQ

### Does this make AI less accurate?

No. The goal is to remove low-value context, not useful evidence. Accuracy comes first: keep exact errors, relevant files, commands, assumptions, risks, and verification results.

### How do I measure savings?

Use your AI tool's token dashboard where available, or run the same workflow before and after applying the playbook and compare prompt/context size. Record the tool, model, input shape, output shape, and caveats so the result is reproducible. Use `templates/token-savings-measurement.md` as a starting point.

### Is this only for coding agents?

No. It works for AI chat, code review, incident triage, CI debugging, infrastructure-as-code, documentation cleanup, and long-running engineering tasks.

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

Contributions are welcome. Useful additions include new tool-specific instruction files, before/after examples, workflow patterns, enforcement checks, and measured token-saving case studies.
