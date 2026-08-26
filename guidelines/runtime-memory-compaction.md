# Runtime Memory And Compaction

Long-running assistants eventually need to reduce active context without losing the facts required to continue safely. Treat compaction as a state-management operation, not as an invitation to discard old messages because the prompt feels large.

## Separate Three Stores

Keep these concerns distinct:

```text
active working context != durable memory != searchable history
```

- **Active working context** contains the recent turns and evidence needed for the current task.
- **Durable memory** contains stable facts, preferences, decisions, procedures, and corrections that are likely to matter again.
- **Searchable history** retains the complete record for exact lookup without injecting it into every model request.

Do not repeatedly send the entire history merely because it is available.

## Deterministic Compaction Trigger

Prefer a measurable trigger when the runtime exposes context or usage telemetry. A practical policy is:

```text
observe usage -> reserve headroom -> compact before the hard limit -> verify -> continue
```

Reserve enough headroom for the compaction request itself, the next user turn, tool schemas, retrieved evidence, and the expected answer. The threshold is runtime-specific; do not hard-code a percentage in shared guidance and assume it is safe everywhere.

Other valid triggers include a turn-count threshold, a byte/token budget, a completed workflow stage, or an idle boundary. Record which trigger fired so later benchmarks can distinguish policy choices.

## What A Continuation Summary Should Preserve

A compacted continuation should preserve, when relevant:

- the current objective and acceptance criteria;
- work completed and artifacts created;
- current state and the next permitted action;
- important decisions and why they were made;
- exact identifiers, paths, commands, errors, dates, versions, and unresolved risks;
- user preferences or constraints that materially affect the task;
- source references needed to re-verify important claims;
- outstanding approvals, blockers, and questions;
- a short recent verbatim tail when exact conversational wording matters.

Use [`templates/continuation-checkpoint.md`](../templates/continuation-checkpoint.md) as a compact handoff format.

## Memory Quality Controls

Durable memory should be smaller than the history it replaces and should carry enough metadata to detect when it should not be trusted blindly.

For each material memory or checkpoint, record where practical:

- source or evidence reference;
- capture/update time;
- scope such as user, repository, project, tenant, or environment;
- source revision/version when the fact depends on mutable code or documentation;
- confidence or verification state for inferred information;
- superseded-by or contradiction markers when state changes.

Do not silently resolve conflicting memory by choosing the most convenient entry. Re-check an authoritative source when the conflict affects a material action.

## Retrieval Before Reinjection

Persistent memory is useful when it prevents repeated context loading. Prefer targeted retrieval over injecting a complete memory store into each request:

```text
query memory -> retrieve a few relevant records -> verify freshness -> add only useful evidence
```

Semantic search can improve recall, but exact identifiers, approvals, security-sensitive facts, and mutable code state should be verified against authoritative sources before high-impact use.

## Safe Compaction Transaction

Compaction changes the source of truth for the next turn, so make the replacement recoverable.

1. Capture the current active-state identifier and the range being compacted.
2. Produce the structured continuation summary.
3. Persist the new checkpoint or compacted state.
4. Verify that the write completed and the checkpoint can be read back.
5. Only then rotate, trim, or replace the older active context.
6. If replacement fails, retain or restore the previous state and surface the failure rather than continuing with partial memory.

Avoid concurrent mutations to the same session while a destructive clear-and-rewrite compaction is in progress unless the runtime explicitly provides transactional semantics.

## Recovery And Staleness

A compaction or memory runtime should have a defined fallback when:

- persistence fails or returns partial state;
- the summary cannot be read back;
- the checkpoint points to a stale repository or document revision;
- source access has been revoked;
- contradictory memory is discovered;
- the searchable archive is unavailable;
- token/context telemetry is missing or unreliable.

Safe fallback options include retaining the previous active state, loading the last verified checkpoint, retrieving authoritative source material again, or stopping before a material action that cannot be reconstructed safely.

## Measure The Whole Trade-Off

Compaction has its own cost. Compare policies using the same tasks and record at least:

- input and output tokens before and after compaction;
- tokens/cost used by the compaction operation itself;
- latency added by compaction;
- number of retrieval calls after compaction;
- task success and factual continuity;
- missed or distorted facts;
- stale-memory or contradiction failures;
- recovery success when persistence is interrupted.

A smaller prompt is not a win if the system repeatedly re-fetches lost facts or makes more mistakes.

## Implementation Examples, Not Requirements

This playbook stays vendor-neutral. Current runtime documentation illustrates several of the patterns above:

- OpenAI Agents SDK sessions and Responses compaction describe persistent session state, threshold-triggered compaction, usage accounting, and recovery considerations: https://openai.github.io/openai-agents-python/sessions/
- OpenAI Agents SDK usage reporting shows how model-call and automatic-compaction usage can be measured together: https://openai.github.io/openai-agents-python/usage/
- LangGraph memory documentation distinguishes short-term thread state from long-term memory and documents trimming, summarisation, semantic retrieval, and checkpoint management: https://langchain-ai.github.io/langgraph/how-tos/persistence/

These references are examples of runtime approaches, not endorsements and not a fixed implementation contract for this repository.

## Design Rule

The goal is not to remember everything in every request. The goal is to preserve recoverable state while making the next model call carry only the evidence it actually needs.
