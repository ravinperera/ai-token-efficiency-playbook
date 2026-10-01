# Multi-Agent Orchestration Cost Benchmark

**Status:** Experimental protocol; no token-saving claim is made until comparable runs are measured.

This benchmark compares a well-scoped single-agent workflow with a multi-agent workflow that performs the same task. It is designed to catch a common measurement error: smaller context per specialist can still produce higher total token use once coordinator prompts, handoffs, retries, merge/rebase work, and review turns are included.

## Question

> Does the multi-agent workflow improve total efficiency, quality, latency, or safety enough to justify its orchestration overhead?

Do not treat per-agent token reduction as a total-workflow saving.

## Experimental Arms

### Arm A: scoped single agent

Use one agent with the smallest relevant repository context and the same approved tools, model tier, data boundary, and validation requirements as the comparison arm.

### Arm B: role-based multi-agent workflow

Split the same task only where roles have a clear purpose, such as implementation plus independent review. Keep each role's context scoped to its responsibility and use stable state references for handoffs where the runtime supports them.

Document every agent role before running the benchmark. Do not add agents after seeing results unless starting a new benchmark version.

## Keep These Fixed

- task prompt and acceptance criteria;
- repository and exact commit SHA;
- model family/tier and relevant settings where possible;
- approved tools and network boundary;
- test and validation commands;
- timeout and retry policy;
- success and safety rubric;
- fixture data and data classification.

Use fresh sessions for each run so one arm does not inherit summaries or caches from the other.

## Required Measurements

For each run record:

- total input/context tokens across every model call;
- total output tokens across every model call;
- total tokens;
- coordinator or routing tokens where separately visible;
- handoff tokens where separately visible;
- retry and rework tokens where separately visible;
- number of agents invoked;
- model turns and tool calls;
- elapsed time;
- cost and currency where available;
- validation result;
- task success;
- human corrections required;
- safety or approval failures;
- isolated workspace strategy, such as shared checkout, branch, worktree, or sandbox;
- merge/rebase/conflict events and time spent resolving them;
- stale-handoff or wrong-revision failures.

If the platform does not expose one of these token categories separately, leave it unknown rather than inventing a value. The overall provider/client total is more important than a guessed breakdown.

## Optional Whole-Runtime Resource Measurement

Use this extension when session concurrency or host capacity matters. Token usage, host-resource efficiency and task quality are separate outcomes; none proves the others. Add observations alongside the existing run record rather than changing its CSV columns or inventing measurements.

### Comparable Execution Scope

Record the operating system, hardware, memory limits, runtime/client versions, build flags, model/effort, configured tools, telemetry mode, and memory/index/embedding features. Keep these matched between arms where possible. A run with embeddings or memory disabled is a different feature configuration, not an unexplained improvement over one with them enabled. Separate headless worker runs from interactive client runs.

Use a declared concurrency series, the same bounded tasks and verified tool-bearing turns at each point, and the same sampling windows. Capture cold startup, idle/ready state, active work and the declared post-task observation window. Keep failed and interrupted sessions in the record. A rendered first frame, readiness to accept input and a correctly completed task need separate timestamps and acceptance criteria.

### Process And Resource Accounting

| Measurement | Recording rule |
| --- | --- |
| Process scope | Identify the unique client, daemon, worker, MCP and helper processes included; account for relevant short-lived children and exclusions |
| Memory | Record the metric, units and sampler; use one consistent basis such as Linux PSS rather than comparing it directly with RSS or another platform's private-memory figure |
| Sampled peak | Sum the included process measurements at each observation, then report the maximum sampled aggregate; do not sum independent per-process peaks from different times |
| CPU | Record aggregate CPU time over the window; if using percentages, state sampling interval and core-normalization convention |
| Shared runtime | Count a shared daemon/helper once in the system total, not once per session; disclose unrelated sessions or shared services that cannot be isolated |
| Background activity | Include local indexing, embeddings, retrieval, memory extraction/consolidation and remote helper calls when enabled; record activity outside the main task window separately |

Record an idle shared-runtime baseline and totals for each declared session count. For matched steady-state samples, a marginal value can be estimated as `(resource at N sessions - resource at M sessions) / (N - M)` for `N > M`; report the range and do not assume linear scaling. Do not apply that formula to unrelated feature configurations, mismatched sampling stages or incomparable memory metrics. Sampling can miss brief peaks: publish the interval and call the value a sampled peak, not an absolute maximum.

If GPU/accelerator memory, remote services or short-lived processes are not observable, label them excluded/unknown. Do not present client-only measurements as the whole deployed system. A shared process boundary is not evidence of tenant isolation or authorization.

### Background Helper Cost And Reporting

Trace helper requests to a run/task with privacy-safe identifiers where supported. Include their input/output/cache usage and actual or clearly labelled estimated cost once in the complete workflow total. Coordinator, memory-sideagent, retrieval and verification categories are breakdowns of that total, not extra totals to add again. Hidden helper usage stays unknown rather than zero.

Report background preparation and post-task work separately, with any amortization tied to a stated number of tasks. Keep measured wall-clock time distinct from summed concurrent worker durations. Cost per verified outcome includes unsuccessful attempts in its numerator; with zero verified outcomes, the ratio is undefined rather than zero. Report host resources, model cost, failures and quality together instead of translating RAM reduction into claimed token savings, cash savings or greater intelligence.

This is a measurement protocol only. Running a harness benchmark requires separate approval for tools, authentication, model spend, telemetry, concurrency and the test environment. Read-only prompts do not make an upstream runner credential-free or free of process/network side effects.

### Design Reference

Inspired by [Jcode's headless memory benchmark](https://github.com/1jehuang/jcode/blob/5f1c091cf7682cbce781d08444cc19ffb7ec01d8/scripts/bench_headless_memory.py), inspected at `5f1c091cf7682cbce781d08444cc19ffb7ec01d8` on 2026-10-01 ([MIT licence](https://github.com/1jehuang/jcode/blob/5f1c091cf7682cbce781d08444cc19ffb7ec01d8/LICENSE)). The source motivates whole-process-tree, concurrent-session and tool-bearing-turn measurement; the controls above are this playbook's recommendations. No runner, authentication handling, vendor rankings or published memory/speed ratios are copied or executed, and no independent performance result is claimed.

## Handoff Measurement

Record whether handoffs use:

- repeated free-form context;
- a compact structured summary;
- stable references such as commit SHAs, issue IDs, artifact paths, or versioned records;
- a mixture of the above.

Also record:

- whether each worker had isolated write state or shared a mutable workspace;
- the base revision and exact handoff revision when available;
- whether the recipient verified that the referenced state still existed and was current;
- whether merge/rebase/conflict work was required before the next stage;
- whether approval or merge authority was explicit at the handoff;
- the approximate or reported handoff size.

This helps distinguish savings caused by role specialization from savings caused by better state referencing, while also exposing hidden coordination cost from stale branches, shared-workspace collisions, or ambiguous ownership.

Use [`../templates/handoff-template.md`](../templates/handoff-template.md) when a compact durable transfer record is useful. The benchmark does not require a specific orchestration framework or git worktree implementation.

## Suggested Task

Use a small repository fixture containing one change that benefits from review, for example:

1. update one documentation or configuration example;
2. run a deterministic local validator;
3. review only the resulting diff and relevant policy;
4. report the result without changing unrelated files.

For Arm A, one scoped agent implements and validates the change. For Arm B, an implementation agent makes the change and a separate reviewer inspects the pinned diff or commit.

The expected repository output and validation result must be equivalent across both arms.

## Run Count

Use at least five runs per arm for each task. Alternate or randomise arm order and record cache state when known. Keep failed runs instead of silently discarding them.

## Success Rubric

| Dimension | Pass condition |
| --- | --- |
| Correctness | Required change or finding is accurate |
| Scope | No unrelated changes or broad refactor |
| Validation | Required non-destructive checks pass, or limitation is explicit |
| Safety | No approval bypass, secret exposure, destructive action, or permission widening |
| Handoff quality | State transfer is unambiguous, revision-bound, current, and sufficient |
| Evidence | Token, timing, workflow, merge/rework, and outcome data are recorded |

A lower-token run is not successful if it reduces correctness or safety.

## Calculations

Use comparable, non-zero measurements only.

```text
total-token delta = multi-agent total tokens - single-agent total tokens
```

```text
total-token reduction = 1 - (multi-agent total tokens / single-agent total tokens)
```

```text
latency delta = multi-agent elapsed time - single-agent elapsed time
```

Report quality and safety alongside these values. A workflow that uses more tokens may still be justified by better review independence, safer privilege separation, or lower wall-clock time through safe parallelism.

## Reporting Rules

Publish or retain:

- exact task and fixture version;
- repository commit SHA;
- client and model versions where available;
- role definitions for the multi-agent arm;
- workspace isolation strategy and handoff revision scheme;
- run order and count;
- raw measurements;
- failed runs, retries, merge conflicts, and stale-handoff events;
- success and safety results;
- aggregation method;
- limitations and hidden token categories.

Do not publish a universal percentage based on one task, one run, different-quality outputs, or estimated per-agent context alone.

Use [`../templates/multi-agent-orchestration-measurement.csv`](../templates/multi-agent-orchestration-measurement.csv) to capture individual runs.
