# Context Hygiene

Context hygiene is the practice of keeping AI inputs small, relevant, and current.

## Good Context

Good context is:

- relevant
- current
- specific
- structured
- short enough to reason over

## Bad Context

Bad context includes:

- full logs when only one error matters
- entire repos when one module matters
- repeated requirements
- stale project notes
- screenshots without explaining the target question
- multiple unrelated issues in one prompt

## Practical Rules

- Start a new chat for a new problem domain.
- Compact long conversations before switching topics.
- Provide file paths and exact errors.
- Remove duplicate logs.
- Replace long logs with summaries.
- Keep project memory under active maintenance.

## Long-Lived Assistants

Long-lived conversational assistants should treat these as separate stores:

1. **Active working context** — the recent conversation and evidence needed for the current task.
2. **Durable memory** — stable facts, user preferences, decisions, procedures, and corrections that remain useful across sessions.
3. **Searchable history** — the full transcript or archive retained for exact lookup, but not loaded into every request.

Do not use a memory file as a complete conversation transcript. Keep durable memory concise, structured, current, and limited to information that is likely to matter again.

When the runtime exposes context-window usage, prefer deterministic monitoring over asking the model to guess whether the conversation is too large. Compact before the provider limit is reached. The exact threshold is runtime-specific and should leave enough headroom for the summary, the next user turn, tool definitions, and model output.

A safe compaction should:

- preserve a recent verbatim tail of the conversation;
- summarise the older portion into the task context, completed work, current state, next actions, important decisions, and user preferences;
- keep exact errors, identifiers, commands, dates, and unresolved risks when they affect correctness;
- retain the full history separately for later search;
- verify that the summary was saved before discarding or rotating the old active context;
- stop and report the problem if consolidation fails instead of silently losing context.

A simple runtime pattern is:

```text
monitor context usage -> compact before the limit -> verify the summary -> continue or rotate the session
```

This playbook documents the operating principle only. Semantic memory graphs, automatic conflict and staleness management, background consolidation agents, and platform-specific integrations such as OpenClaw remain future work.

## Multi-Agent Context

Multi-agent systems need an additional check: smaller context per agent does not necessarily mean fewer tokens overall. Scope evidence by role, hand off stable references instead of repeated state, and add specialist agents only when their value justifies coordination overhead.

See [multi-agent context efficiency](multi-agent-context-efficiency.md) for practical role scoping, pointer-based handoffs, batching, orchestration anti-patterns, and total-cost measurement.

## Before Sending A Prompt

Ask:

- What do I actually need the AI to decide?
- Which files or outputs are relevant?
- Can I remove repeated context?
- Can I provide an exact error instead of a full log?
- Is this a simple task that needs a cheaper model?
