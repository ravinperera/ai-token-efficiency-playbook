# Multi-Agent Orchestration Cost Benchmark

**Status:** Experimental protocol; no token-saving claim is made until comparable runs are measured.

This benchmark compares a well-scoped single-agent workflow with a multi-agent workflow that performs the same task. It is designed to catch a common measurement error: smaller context per specialist can still produce higher total token use once coordinator prompts, handoffs, retries, and review turns are included.

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
- safety or approval failures.

If the platform does not expose one of these token categories separately, leave it unknown rather than inventing a value. The overall provider/client total is more important than a guessed breakdown.

## Handoff Measurement

Record whether handoffs use:

- repeated free-form context;
- a compact structured summary;
- stable references such as commit SHAs, issue IDs, artifact paths, or versioned records;
- a mixture of the above.

Also record the approximate or reported handoff size. This helps distinguish savings caused by role specialization from savings caused by better state referencing.

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
| Handoff quality | Multi-agent state transfer is unambiguous and sufficient |
| Evidence | Token, timing, workflow, and outcome data are recorded |

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
- run order and count;
- raw measurements;
- failed runs and retries;
- success and safety results;
- aggregation method;
- limitations and hidden token categories.

Do not publish a universal percentage based on one task, one run, different-quality outputs, or estimated per-agent context alone.

Use [`../templates/multi-agent-orchestration-measurement.csv`](../templates/multi-agent-orchestration-measurement.csv) to capture individual runs.
