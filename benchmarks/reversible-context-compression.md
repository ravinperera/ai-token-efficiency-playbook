# Reversible Context Compression Benchmark

This benchmark compares three ways of supplying large evidence to the same AI task:

1. **Raw context** — provide the complete selected evidence.
2. **Irreversible summary** — replace the evidence with a summary that cannot retrieve omitted source material.
3. **Reversible compression** — provide a compact representation plus stable references that can retrieve original evidence when needed.

The benchmark does not assume that reversible compression wins. It measures the trade-off between active context, cache behaviour, retrieval overhead, correctness, and cost.

## Use The Same Task

Choose one task from `evaluation-corpus.md` or define an equivalent fixed task. Keep constant across all three arms:

- model/provider and reasoning setting;
- system/project instructions;
- task prompt and acceptance criteria;
- authoritative source evidence;
- verification procedure;
- tool permissions;
- maximum retry count.

Run multiple repetitions when the model is non-deterministic.

## Prepare The Evidence

Select a source that contains both repetitive material and decision-critical details, for example:

- a synthetic CI log with repeated success lines plus one exact failure;
- a large API/RAG result with duplicates plus a small relevant subset;
- a long conversation history with an exact unresolved requirement;
- a multi-agent handoff with source references.

Mark the **must-retain evidence** before creating summaries or compressed forms. A run fails if the final answer needs that evidence and cannot recover it accurately.

## Arm A: Raw Context

Provide the complete selected evidence with no semantic compression.

Record the provider's token/cache accounting where available. This arm is the correctness baseline, not automatically the cost baseline.

## Arm B: Irreversible Summary

Create a bounded summary of the same source and remove direct retrieval access to omitted material for the run.

The summary must state its generation method and approximate size. Do not manually improve it after seeing the task result.

## Arm C: Reversible Compression

Create a compressed representation that:

- preserves recent/critical evidence verbatim;
- states what categories of information were omitted;
- includes stable source references;
- allows the agent to retrieve the smallest relevant original range on demand;
- falls back to the original representation when the transform is larger or fails required-evidence validation.

Record every retrieval call and the amount of source material reintroduced.

## Measurements

Capture at least:

| Metric | Raw | Summary | Reversible |
| --- | ---: | ---: | ---: |
| Initial active input tokens | | | |
| Cached input/read tokens | | | |
| Cache-write tokens | | | |
| Output tokens | | | |
| Retrieval/tool-call count | | | |
| Reintroduced source tokens | | | |
| Compression latency | | | |
| Retrieval latency | | | |
| Total wall-clock latency | | | |
| Actual/estimated cost | | | |
| Required evidence preserved | | | |
| Task success | | | |
| Verification success | | | |

When a provider does not expose a metric, record `N/A`; do not invent it.

## Cache Test

Where prompt-cache telemetry exists, repeat the same follow-up request after the initial run and record whether each strategy preserved a useful stable prefix. A transform that reduces raw tokens but repeatedly invalidates cache may cost more overall.

Record provider-specific cache pricing and expiry assumptions with the result because these can change.

## Failure Conditions

A strategy fails the benchmark run if it:

- loses or alters must-retain evidence;
- produces a materially incorrect answer because evidence was omitted;
- cannot resolve a referenced original when retrieval is required;
- uses stale or wrong-project evidence;
- reports a token/cost saving without comparable measurement;
- exceeds the allowed retry/retrieval budget without completing the task.

## Report Results

Report medians across comparable repetitions and include the raw measurements. Separate:

- **context reduction** from **billable-cost reduction**;
- **compression cost** from **inference cost**;
- **initial savings** from **retrieval payback**;
- **cache effects** from ordinary token reduction.

Do not generalise a result from one model, provider, cache policy, source shape, or task to all agent workloads.

## Interpretation

Reversible compression is useful when it lowers active context while preserving a reliable path to evidence. It is not a success when retrieval is broken, critical details disappear, or cache/latency overhead outweighs the reduction.
