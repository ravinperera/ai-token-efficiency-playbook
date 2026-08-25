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
│   ├── progressive-context-retrieval.md
│   ├── cli-output-compression.md
│   ├── document-to-markdown.md
│   ├── model-routing.md
│   ├── per-tool-notes.md
│   └── anti-patterns.md
├── examples/
│   ├── before-after-prompts.md
│   ├── bad-vs-good-context.md
│   ├── case-study-ci-log-triage.md
│   └── image-vs-markdown-context.md
├── benchmarks/
│   ├── document-conversion-measurement.md
│   └── dynamic-resource-discovery.md
├── scripts/
│   ├── check-token-hygiene.sh
│   └── estimate-context-size.py
├── tests/
│   ├── test_check_token_hygiene.sh
│   └── test_estimate_context_size.py
├── templates/
│   ├── ci-failure-triage.md
│   ├── document-context-extraction.md
│   ├── handoff-template.md
│   ├── model-routing-decision.md
│   ├── resource-discovery-measurement.csv
│   └── token-savings-measurement.md
└── checklists/
    └── token-efficiency-checklist.md
```

See [`CHANGELOG.md`](CHANGELOG.md) for the lightweight version history and release notes.

## The Standard

The canonical rules live in `guidelines/`. Tool-specific files such as `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are intentionally thin adapters.

AI agents should:

- Use context hygiene before optimizing response style.
- Search before reading large files.
- Use progressive retrieval: discover structure first, then load the smallest relevant symbol or range.
- Read the smallest relevant file range.
- Convert text-heavy documents to searchable Markdown before loading whole documents or screenshot collections.
- Keep the original visual only when layout, charts, diagrams, or image content affect the answer.
- Summarise large logs instead of repeating them.
- Avoid restating unchanged context.
- Keep persistent instruction and memory files short.
- Use the lowest approved model tier capable of the task.
- Escalate early when security, production, architecture, ambiguity, sensitive data, or repeated failure appears.
- Preserve technical accuracy over extreme compression.

For tool-specific context risks, see the [per-tool token waste notes](guidelines/per-tool-notes.md).

For codebase discovery, structural views, persistent code indexes, context receipts, and canonical project context, see [progressive context retrieval](guidelines/progressive-context-retrieval.md).

For common mistakes and fixes, see the [token waste anti-patterns catalogue](guidelines/anti-patterns.md).

For PDFs, Office files, spreadsheets, screenshots, and scans, see the [document-to-Markdown context reduction guide](guidelines/document-to-markdown.md).

For lower-model selection and escalation rules, see the [practical model-routing guide](guidelines/model-routing.md) and the [routing decision template](templates/model-routing-decision.md).

For long-running chats and assistants, see the [long-lived assistant guidance](guidelines/context-hygiene.md#long-lived-assistants).

For the repository's operating assumptions and residual limitations, see the [repository safety assumptions](docs/safety-assumptions.md).

## Why This Matters

Token waste normally comes from four places:

1. Oversized input context: whole repos, full files, complete documents, screenshots, and long chat history.
2. Noisy tool output: full CI logs, Terraform plans, stack traces, and terminal dumps.
3. Repeated instructions: duplicated memory files, repeated project rules, and stale context.
4. Poor model routing: using high-cost reasoning models for simple formatting, summarisation, or extraction.

Short replies help, but context hygiene usually saves more.

## Long-lived assistant context

Long-running assistants should keep three concerns separate:

```text
active working context != durable memory != searchable full history
```

The active context should contain only the recent conversation and evidence needed for the current task. Durable memory should contain stable facts, preferences, decisions, procedures, and corrections. Full history should remain searchable for exact lookup rather than being loaded into every request.

When the runtime supports context-window telemetry, monitor usage deterministically and compact before the provider limit. A safe compaction keeps recent turns, creates a structured continuation summary, verifies that the summary was saved, and retains the full history separately.

This is a small operating guideline, not a memory-runtime implementation. Semantic memory graphs, automated conflict and staleness management, background consolidation, and platform-specific integrations remain future work.

## Practical model routing

Use capability tiers instead of hard-coding model names:

| Tier | Example use |
| --- | --- |
| Economy / fast | Formatting, extraction, rewriting, selected-text summarisation, deterministic transformations |
| Balanced | Scoped bug fixes, focused code review, ordinary engineering tasks with clear acceptance criteria |
| Advanced reasoning | Security, production, architecture, incidents, ambiguous requirements, broad cross-system work |

Recommended routing flow:

```text
confirm approved data boundary -> classify risk -> choose lowest capable tier -> verify -> escalate when triggered
```

Do not silently switch provider, tenancy, region, retention policy, approved model family, or data boundary merely to reduce cost. If the agent host cannot change models automatically, it should state the recommended tier rather than pretending a switch happened.

Start with:

- [Practical model-routing guide](guidelines/model-routing.md)
- [Model-routing decision template](templates/model-routing-decision.md)

## Document-to-Markdown workflow

Text-heavy PDFs, Word documents, PowerPoint files, spreadsheets, screenshots, and scans can often be converted to searchable Markdown before AI use. Microsoft [MarkItDown](https://github.com/microsoft/markitdown) is one example of a local conversion utility designed for LLM and text-analysis workflows.

The recommended process is:

```text
convert locally -> inspect -> search -> select relevant sections -> attach a visual only when needed
```

This avoids providing an entire document when the task needs only a few sections. The original page or image should still be retained when the answer depends on diagrams, charts, colour, spatial layout, UI appearance, handwriting, or complex tables.

Start with:

- [Document-to-Markdown guidance](guidelines/document-to-markdown.md)
- [Image-heavy vs selected-Markdown example](examples/image-vs-markdown-context.md)
- [Document context extraction template](templates/document-context-extraction.md)
- [Document conversion measurement protocol](benchmarks/document-conversion-measurement.md)

The playbook makes no fixed token-saving claim for conversion. Measure the complete document, complete Markdown, selected Markdown, and selected-Markdown-plus-visual approaches against the same task.

## Emerging benchmark: dynamic resource discovery

Agent clients are beginning to discover skills, tools, agents, and MCP servers on demand instead of preloading every capability into each session. The [dynamic resource discovery benchmark](benchmarks/dynamic-resource-discovery.md) defines a vendor-neutral method for comparing those approaches across input context, total tokens, cost, latency, task success, resource selection, and safety.

Use [`templates/resource-discovery-measurement.csv`](templates/resource-discovery-measurement.csv) to capture raw runs. This repository does **not** claim a saving until comparable, reproducible measurements have been collected.

## Example Token-Saver Prompt

```text
Use TokenSaver mode for this task.
Answer first. Read only relevant files. Summarise large outputs. Do not repeat unchanged context. Use the smallest useful verification. Keep final response short unless I ask for detail.
```

For CI/CD failures, use [`templates/ci-failure-triage.md`](templates/ci-failure-triage.md) to provide the exact failure signal without pasting full raw logs.

For concise task transfers, use [`templates/handoff-template.md`](templates/handoff-template.md) to capture facts, errors, recent changes, tried commands, and open questions without carrying unnecessary context.

## Optional Local Check

Run the lightweight hygiene check before committing AI instruction files or logs:

```bash
bash scripts/check-token-hygiene.sh
```

The same check can also run in CI. See [`docs/token-hygiene-ci.md`](docs/token-hygiene-ci.md) for the workflow purpose, default thresholds, and tuning guidance.

To produce rough before/after context-size numbers for a case study, use the dependency-free estimator documented in [`docs/context-size-estimator.md`](docs/context-size-estimator.md):

```bash
python3 scripts/estimate-context-size.py before.md after.md --markdown
```

Run the helper regression tests before changing file discovery, thresholds, encoding, totals, or output formats:

```bash
python3 -m unittest discover -s tests -p 'test_estimate_context_size.py' -v
bash tests/test_check_token_hygiene.sh
```

The shell suite verifies staged filenames containing spaces, log and context thresholds, instruction-size limits, untracked-file behavior, and the non-Git fallback. GitHub Actions runs both dependency-free suites on pull requests and pushes to `main`.

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

No. It works for AI chat, code review, incident triage, CI debugging, infrastructure-as-code, document review, documentation cleanup, and long-running engineering tasks. Runtime-specific memory and session-management implementations remain outside the current scope.

## What This Is Not

This is not a benchmark claim that every workflow saves a fixed percentage. Token savings depend on the task, model, tool, document format, conversion quality, and how much context is loaded. The aim is practical reduction without making the AI less useful.

## Recommended Use

Use this playbook when working with:

- AI coding agents
- terminal-based AI tools
- large codebases and codebases with reusable structural indexes
- text-heavy documents and screenshot collections
- CI/CD logs
- infrastructure-as-code projects
- long debugging sessions
- long-lived assistants that need basic context and memory boundaries
- repeated review or refactor workflows

## Contributing

Contributions are welcome. Useful additions include new tool-specific instruction files, before/after examples, workflow patterns, enforcement checks, and measured token-saving case studies.
