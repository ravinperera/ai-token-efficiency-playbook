# Progressive Context Retrieval

Large codebases do not need to be loaded into an AI agent all at once. A better default is to reveal context in layers and stop as soon as the task is answerable.

Use this progression:

```text
metadata / search -> structure / outline -> relevant symbol or range -> full file only when justified
```

This pattern reduces repeated context, keeps evidence focused, and makes it easier to measure what each retrieval step actually costs.

## 1. Start With Discovery, Not File Dumps

Before reading a large file, first identify where the answer is likely to live.

Prefer:

- repository metadata and changed-file lists;
- filename and symbol search;
- dependency or call-graph queries;
- directory listings;
- headings, signatures, or structural outlines;
- exact error locations and stack frames.

Only load source bodies after discovery has narrowed the candidate set.

## 2. Use Structural Views Before Full Content

For large source files, a structural view can often answer the first question: what is here and where is the relevant part?

A structural view might contain:

- function, class, method, route, resource, or module names;
- signatures and type information;
- line ranges;
- imports and dependencies;
- call relationships;
- configuration keys;
- headings for documentation.

After locating the likely symbol or section, retrieve only that implementation plus the minimum surrounding context required to reason safely.

Do not assume an outline is sufficient for behavioural changes. Read the implementation, tests, and callers when correctness depends on them.

## 3. Reuse Structural Memory Carefully

A persistent repository index, code graph, symbol database, or retrieval cache can avoid rediscovering the same architecture on every session.

Use persistent structural memory for questions such as:

- where is this function defined?
- what calls this component?
- which routes reach this handler?
- which files depend on this module?
- what changed around this symbol?

Treat the index as a discovery layer, not unquestioned ground truth.

Before relying on it for a material decision:

- confirm which repository and revision it represents;
- refresh or invalidate it after relevant changes;
- fall back to source when the index is incomplete or stale;
- verify high-impact conclusions against authoritative files;
- keep project boundaries explicit so results from one codebase do not leak into another.

## 4. Make Context Consumption Observable

Where the runtime exposes enough telemetry, record a small context receipt for meaningful reads.

Useful fields include:

```text
source/ref
view type
bytes returned
estimated or provider-reported input tokens
tool calls
bytes or sections avoided, if measured
freshness / index revision
reason for escalation to a larger view
```

Receipts make it possible to distinguish real context reduction from workflows that simply hide cost across more tool calls.

Do not infer a fixed token-saving percentage from bytes alone. Tokenization, tool envelopes, duplicated prompts, retries, and model behaviour all affect total cost.

## 5. Escalate Context Deliberately

Move to a larger view only when the smaller view cannot answer the task safely.

Examples:

- A symbol search finds the handler, but a bug fix requires its implementation and tests.
- A call graph identifies callers, but an API change requires reading the compatibility layer.
- A structural outline shows configuration keys, but a security review requires exact default values and validation logic.

A useful escalation note is short:

```text
Need full implementation because the decision depends on error handling not visible in the outline.
```

This creates an audit trail without forcing verbose reasoning into every prompt.

## 6. Keep One Canonical Project Context

Repeated platform-specific instruction files can become both a token cost and a governance drift risk.

Prefer:

```text
canonical project context / policy
        -> thin Codex adapter
        -> thin Claude adapter
        -> thin Copilot adapter
        -> thin Cursor adapter
        -> thin Gemini adapter
```

The canonical source should hold shared architecture, safety boundaries, validation commands, and durable project conventions. Provider-specific files should contain only tool-specific behaviour, routing details, or constraints that cannot be expressed once.

This repository follows that principle: `guidelines/` contains the canonical guidance while files such as `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` remain adapters.

## 7. Separate Retrieval Policy From Prompt Advice

Prompt instructions such as "read only what you need" are useful, but a retrieval layer can enforce stronger limits where the environment supports it.

Possible controls include:

- refuse secrets, binaries, generated output, or oversized lockfiles by default;
- return an outline for large files before allowing a full read;
- cap ranges or response sizes;
- require a reason before escalating to a larger view;
- log what was requested versus what was returned.

Do not block evidence required for correctness. Security-sensitive and production work may legitimately require broader context than routine editing.

## Practical Workflow

```text
1. identify the task and authoritative repository/ref
2. search for candidate files/symbols
3. query structure or persistent index if available
4. read the smallest relevant implementation range
5. expand to callers/tests/config only when the decision requires it
6. verify against source when using cached or indexed knowledge
7. record total workflow cost when benchmarking
```

## When Full-File Reads Are Reasonable

A full file can still be the cheapest safe choice when it is:

- small;
- tightly scoped to the task;
- a policy or configuration file whose global interactions matter;
- a test file where fixture/setup context is required;
- easier to load once than repeatedly retrieve many overlapping ranges.

The goal is not to minimize every individual read. The goal is to minimize total irrelevant context while preserving correctness.

## Related Implementations

These public projects illustrate useful implementation patterns without defining this playbook's requirements:

- [Graft](https://github.com/flyingrobots/graft) demonstrates governed structural reads, refusals, and context receipts.
- [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) demonstrates a persistent structural code index and graph-style queries.
- [OpenMontage](https://github.com/open-montage/OpenMontage) demonstrates a canonical shared project context with tool- and stage-specific knowledge loaded as needed.

Treat their performance claims as project-specific until reproduced on your own workload. The playbook deliberately keeps the pattern vendor-neutral.

## Measurement

When evaluating this approach, compare the complete workflow rather than one tool response. Use the [structural memory retrieval benchmark](../benchmarks/structural-memory-retrieval.md) and capture task success alongside tokens, bytes, tool calls, latency, freshness failures, and indexing overhead so local efficiency does not hide total workflow cost.
