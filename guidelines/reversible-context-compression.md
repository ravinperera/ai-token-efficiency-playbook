# Reversible Context Compression

Summaries reduce active context, but an irreversible summary can hide the exact evidence that later becomes important. For long-running agents, tool-heavy workflows, and large retrieval results, prefer **reversible compression** when omitted source material may need to be inspected again.

The goal is not to keep every byte in the prompt. The goal is to keep the active prompt small **without destroying the path back to authoritative evidence**.

## Core Pattern

```text
capture authoritative original
-> classify importance and sensitivity
-> preserve recent/critical evidence
-> compress low-value or repetitive material
-> record what was omitted and where it can be retrieved
-> use compact context
-> retrieve original evidence on demand
```

The authoritative original should remain outside the active prompt in a store with appropriate retention, access control, and project/tenant isolation.

## What To Preserve Verbatim

Do not compress away evidence when exact wording or exact values affect correctness. Typical examples include:

- the current user requirement and explicit constraints;
- exact error messages, identifiers, checksums, dates, versions, and commands involved in a failure;
- authentication, authorisation, security, privacy, legal, financial, or regulatory evidence;
- destructive-action plans and rollback conditions;
- recent conversation turns that establish the current task state;
- source passages that will be quoted, cited, or approved by a human;
- configuration values where a one-character difference changes behaviour.

Compression should remove redundancy, not decision-critical evidence.

## Compression Record

A reversible transform should leave a small receipt such as:

```text
source_ref: tool-call-184/logs
source_revision: sha256:...
transform: repeated-success-lines + stacktrace-dedup
original_tokens: 18420
compressed_tokens: 2130
omitted: 312 repeated success lines, 18 duplicate stack frames
retrieval: available
created_at: 2026-09-19T09:00:00Z
```

The exact schema is implementation-specific. The important properties are provenance, retrievability, and enough description for the agent to know when it should fetch the original.

## Inflation Guard

A transform is not useful merely because it is called compression.

Keep the original representation when any of these are true:

- the transformed content uses more tokens than the source;
- required evidence is missing or altered;
- retrieval metadata is broken or ambiguous;
- the transform makes verification materially harder;
- compression latency or retrieval overhead outweighs the expected saving for the task.

A safe implementation can compare measured token counts before replacing active context. If token measurement is unavailable, use bytes/characters as a rough diagnostic but do not report them as token savings.

## Cache-Aware Compression

Provider prompt caching can make a stable prefix cheaper than repeatedly rewritten context. A smaller prompt is not automatically cheaper if every request invalidates a useful cached prefix.

When the provider or host exposes cache telemetry:

- keep stable system/project instructions stable where practical;
- avoid recompressing unchanged earlier context on every turn;
- record cached/read/write token classes separately when available;
- compare total billable cost and latency, not raw input-token count alone;
- treat provider-specific cache discounts and expiry rules as runtime configuration, not permanent assumptions.

When cache telemetry is unavailable, note that limitation rather than claiming savings.

## Retrieval Policy

The agent should retrieve the original when:

- the compressed form says relevant details were omitted;
- a decision depends on an exact value or exact wording;
- verification fails or the compressed evidence is ambiguous;
- a human asks for the source evidence;
- the task crosses a security, production, legal, financial, or other high-risk boundary;
- a citation or audit record must point to authoritative material.

Do not repeatedly retrieve the same large source. Retrieve the smallest relevant range when the storage layer supports it.

## Multi-Agent Handoffs

For multi-agent systems, a compressed handoff can reduce repeated context fan-out. Keep one authoritative source reference and pass each specialist only the summary and evidence slice needed for its role.

A downstream agent must not treat the compressed handoff as more authoritative than the original source. It should be able to request the referenced source when the handoff is insufficient.

## Security And Privacy Controls

A reversible store can create a new data-retention boundary. Before adopting one, define:

- storage location and tenant/project isolation;
- encryption and access control;
- retention and deletion policy;
- whether secrets or regulated data may be stored;
- auditability of source retrievals;
- who can resolve a compressed reference;
- behaviour when the source is deleted or expires.

Compression does not make sensitive data non-sensitive.

## Measuring The Trade-Off

Compare raw context, irreversible summarisation, and reversible compression against the **same task and evidence requirements**. Record:

- active input tokens;
- cached/read/write tokens where exposed;
- output tokens;
- tool calls and source-retrieval calls;
- compression and retrieval latency;
- total cost under the actual billing model;
- task success and verification result;
- missing-evidence or stale-reference failures.

Use [`../benchmarks/reversible-context-compression.md`](../benchmarks/reversible-context-compression.md) for a repeatable protocol.

## Upstream Inspiration And Attribution

This guidance was informed by the reversible compression, retrieval, cache-alignment, and content-routing patterns described by [dschumann/Headroom](https://github.com/dschumann/Headroom), reviewed 2026-09-19. The playbook adopts the vendor-neutral design principles, not Headroom's published percentage-savings claims. Any quantitative claim here must be reproduced on the local evaluation corpus and runtime.