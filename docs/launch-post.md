# Launch Post Draft: Stop Wasting Tokens In AI Coding Sessions

AI coding tools are powerful, but most teams waste tokens in a very predictable way.

The problem is not only that AI replies are sometimes too long. The bigger problem is that we keep feeding AI tools too much low-value context: full CI logs, whole files, broad repository scans, repeated memory, stale instructions, and screenshots where exact text would be better.

That is why I created the **AI Token Efficiency Playbook**.

The main idea is simple:

> Context is more expensive than reply style.

Short answers help, but the largest savings usually come before the answer is written. If the model receives cleaner input, it can work faster, stay focused, and avoid spending attention on noise.

## The Four Sources Of Token Waste

The playbook focuses on four common waste sources.

First, oversized input context. This happens when a user asks an AI agent to inspect a whole repository, a full Terraform plan, or a complete CI log before the task is clearly scoped.

Second, noisy tool output. CI systems, package managers, Terraform, Kubernetes, and test runners produce useful information, but they also produce a lot of successful setup output that is irrelevant to the failure.

Third, repeated instructions. Long memory files, duplicated project rules, and stale context get carried into every session even when they are no longer useful.

Fourth, poor model routing. Not every task needs the most expensive reasoning model. Formatting, extraction, simple summarisation, and small documentation edits can often use cheaper or faster models where the tool supports that choice.

## A Practical Example

In the CI log triage case study, the before prompt included a full deployment log with successful setup steps, provider installation output, repeated environment variables, and cleanup output. The approximate input size was around 7,825 tokens.

The TokenSaver version included only the workflow name, failed step, exact AWS error, relevant recent change, one relevant file, and the desired outcome. That reduced the approximate input to around 95 tokens while keeping the failure signal intact.

The goal was not blind compression. The goal was to keep the evidence that changes correctness and remove the noise that does not.

## What The Repo Provides

The repo includes drop-in instruction files for common AI coding tools:

- Codex / general coding agents via `AGENTS.md`
- Claude Code via `CLAUDE.md`
- Gemini via `GEMINI.md`
- GitHub Copilot via `.github/copilot-instructions.md`
- Cursor via `.cursor/rules/token-efficiency.mdc`

It also includes prompt modes, checklists, context hygiene guidance, model-routing notes, examples, and a lightweight script to catch common token-hygiene problems before they are committed.

## How To Use It

Start with the 30-second install section in the README. Copy the instruction file for your tool into your own repository, then use TokenSaver mode when debugging, reviewing code, or refactoring.

A simple prompt looks like this:

```text
Use TokenSaver mode for this task.
Answer first. Read only relevant files. Summarise large outputs. Do not repeat unchanged context. Use the smallest useful verification. Keep final response short unless I ask for detail.
```

## Final Thought

AI token efficiency is not about making AI less useful. It is about giving the model cleaner evidence, better boundaries, and less noise.

If your team uses AI coding agents, CI debugging, infrastructure-as-code, or long engineering chats, this playbook gives you a practical starting point.

Repo: https://github.com/ravinperera/ai-token-efficiency-playbook
