# Token Efficiency Checklist

Use this before and during an AI coding, debugging, review, or research session. The goal is to reduce unnecessary context without dropping evidence needed for correctness.

## Before Prompting

- [ ] Define the exact outcome, scope, constraints, and acceptance criteria.
- [ ] Remove unrelated conversation history, files, logs, screenshots, and duplicated instructions.
- [ ] Provide exact errors and the smallest surrounding evidence instead of complete logs.
- [ ] Confirm the approved provider, model family, tenancy, region, retention policy, and data boundary before routing for cost.
- [ ] Choose the lowest approved model tier that can reliably perform the task; identify escalation triggers in advance.

## Retrieve Context Progressively

- [ ] Search or inspect metadata before opening large files or documents.
- [ ] Prefer `metadata/search -> structure/outline -> relevant symbol or range -> full file only when justified`.
- [ ] Query a trusted structural index or durable project memory before rediscovering stable repository facts, when one is available.
- [ ] Verify indexed or remembered facts against source when freshness, authorization, or correctness could have changed.
- [ ] Convert text-heavy documents to searchable text/Markdown first; retain visuals only when layout, diagrams, charts, handwriting, or image content matter.
- [ ] Summarise noisy tool output and keep the exact failing lines, identifiers, commands, and nearby evidence required for verification.

See [progressive context retrieval](../guidelines/progressive-context-retrieval.md), [context hygiene](../guidelines/context-hygiene.md), and [document-to-Markdown guidance](../guidelines/document-to-markdown.md).

## For Coding Agents

- [ ] Keep one canonical project policy and make provider-specific instruction files thin adapters rather than duplicated policy copies.
- [ ] Ask the agent to read only the files, symbols, or ranges needed for the current step.
- [ ] Use targeted tests and deterministic checks before broad test suites or repository-wide scans when the scope is narrow.
- [ ] Preserve security, production, architecture, compliance, and ambiguity escalation rules even when optimizing tokens.
- [ ] Do not trade away exact evidence, required human approval, or independent verification merely to shorten context.

## Long-Lived Sessions And Memory

- [ ] Keep active working context separate from durable memory and searchable full history.
- [ ] Persist only stable facts, decisions, procedures, corrections, and compact checkpoints that are useful beyond the current turn.
- [ ] Record source/provenance and freshness for durable memory when stale information could change the result.
- [ ] Compact before the provider context limit when telemetry is available, and verify that the continuation summary or checkpoint was saved before discarding active context.
- [ ] Remove or invalidate stale, superseded, unauthorized, or task-specific memory.

## Measure Claims

- [ ] If claiming token or context savings, compare equivalent tasks with the same required evidence and success criteria.
- [ ] Record input/output tokens or a clearly documented proxy, tool calls, latency, correctness, fallback reads, and relevant indexing/compaction overhead.
- [ ] Do not publish a universal saving percentage from one example, one provider, or one repository.
- [ ] Use the [evaluation corpus](../benchmarks/evaluation-corpus.md) and relevant benchmark protocol when a repeatable comparison is useful.

## After The Task

- [ ] Keep the final handoff concise: outcome, changed facts, verification, unresolved risks, and next action.
- [ ] Save only durable project knowledge; leave transient logs and working notes out of persistent context.
- [ ] Record a reusable lesson only when it changes future retrieval, routing, verification, or safety behaviour.
- [ ] Start the next task with a clean context rather than carrying unrelated material forward.
