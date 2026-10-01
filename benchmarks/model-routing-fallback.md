# Model Routing And Bounded Fallback Benchmark

**Status:** Reproducible protocol only. No model runs, router implementation, or measured savings are supplied.

Use this protocol to test whether [model routing](../guidelines/model-routing.md) improves complete-workflow cost or latency while preserving quality and approved data boundaries. A cheaper successful final attempt does not erase the cost or risk of earlier attempts.

## Freeze The Experiment

Before collecting results, complete a [benchmark run manifest](../templates/benchmark-run-manifest.md) and a [routing decision record](../templates/model-routing-decision.md). Pin:

- this protocol, the repository commit, and all six task/input pairs from the [fixed evaluation corpus](evaluation-corpus.md), including their must-retain items and failure conditions;
- exact prompts, instruction versions, tools, model settings where comparable, verifier and scoring rubric;
- approved route identifiers and provider/model versions where exposed, capability floors and provider, tenancy, region, retention and training constraints;
- the task-risk classifier or routing rules, their version, and the allowed route for each risk class; classification must not see held-out answers or trial outcomes;
- the fixed baseline model, selected before seeing results and approved for every included task;
- attempt, token, spend and elapsed-time ceilings, transient retry policy, fallback order, verification-failure escalation policy and stop conditions;
- cache preparation, trial count, arm order, random seed where supported, concurrency and telemetry/cost sources.

Record unavailable model versions or measurements as `unknown`. Do not invent comparability. If a route is unavailable or unapproved, record a blocked run rather than silently changing the experiment. The corpus includes security and operational questions: task-aware routing may legitimately select the same advanced tier for several or all cases.

## Three Arms

| Arm | Selection | Retry and fallback behavior |
| --- | --- | --- |
| A — fixed approved model | One preselected model for every task | Bounded retries on the same route only; stop if it cannot meet the task |
| B — task-aware routing | Frozen risk/capability rules choose an approved route before the first attempt | Same bounded transient retry policy as A; no route change within the run |
| C — routing with bounded fallback | Same initial routing rules as B | Same transient retry policy, plus a predeclared approved fallback/escalation order and triggers |

All arms have identical total budget, time and attempt ceilings and the same required verification. Different route choices are the experimental variable. Count the first attempt, retries and fallback attempts toward one ceiling; a fallback never resets the budget. No arm may knowingly continue below the task's capability floor. A/B stop when a different route is required. C may proceed only if its next route is approved, capable and within the remaining limits.

Use an existing authorized host or manual route selection for any future execution. If switching is unsupported, mark that arm unavailable; a recommendation is not an executed route. This protocol does not authorize API spending or external actions.

## Matched Trials And Cache Conditions

1. Run every frozen task under A, B and C with at least five trials per arm per cache condition. Record every scheduled run, including blocked, aborted and unsuccessful runs.
2. Use fresh task sessions and identical evidence. Randomize or rotate arm order and record it. Never carry answers, conversation memory or learned corrections from one arm into another.
3. Separate cold and warm-cache strata. Define the exact reusable prefix and preparation procedure for each route. Charge cache priming/build overhead once under a declared allocation rule and retain its ledger. Do not assume a fallback shares another route's cache.
4. Record observed cache hits/misses and cached/read/write counts, not just requested cache state. If clearing or observing cache is unsupported, label the condition unknown and keep it separate from controlled cold/warm results.
5. Preserve prompts and outputs in an approved evidence store, using redacted identifiers or hashes in public records. Keep the identical acceptance rubric even when a run fails or times out.

## Failure And Boundary Scenarios

Alongside normal runs, predeclare a matched failure schedule: for example, the first request is unavailable, an attempt times out with ambiguous billing, verification fails, or the next candidate route violates the approved region/retention boundary. Apply the same trigger position and evidence to each arm; do not selectively induce failures to favor fallback.

Use synthetic fixtures and an approved simulator or tabletop review for boundary scenarios. Never send sensitive data to an unapproved route merely to test rejection. Keep simulated policy outcomes separate from observed runtime outcomes; neither a tabletop nor this document proves runtime enforcement.

Before each attempted submission, check route approval, capability and remaining budget. Record a rejected candidate as a routing decision with zero submitted attempts, plus any real decision overhead. If delivery or billing is ambiguous, reconcile authoritative state before retrying; retain unresolved usage as unknown, not zero. Define a conservative reservation rule or stop when the remaining budget cannot be established.

Distinguish a prevented boundary violation from an actual unauthorized request. Both remain visible in the report; an actual boundary breach fails the safety gate regardless of output quality or cost. Budget exhaustion, unsafe fallback, no capable approved route, and deadline exhaustion are explicit terminal outcomes.

## Capture Every Attempt And The Whole Run

Use the [routing benchmark record](../templates/model-routing-benchmark-record.md), linked to the existing manifest. Retain a unique request/attempt identifier and its parent run. Include unsuccessful and cancelled requests, partial outputs, routing/classification calls, cache preparation, verifier calls, tool usage, retries, backoff and human correction effort.

- Measure end-to-end latency from initial routing through final verification or stop. Also record routing, request, queue/backoff and verification durations. Overlapping durations are diagnostic subsets, not values to sum into wall-clock time.
- Sum unique model-request usage once. Router and verifier model calls belong in that total; their category totals are subsets. Deterministic routing has no model tokens, but still has time/compute overhead.
- Follow the [observability accounting guidance](../guidelines/token-observability.md). Cached input may already be included in input tokens; cache reads/writes and reasoning tokens may overlap other counters. Record provider semantics and normalize before aggregation. Do not add overlapping categories or combine duplicate client and provider receipts.
- Separate billed cost, API-equivalent estimates and allocated subscription cost. Record currency, pricing source/effective date, cache pricing and allocation assumptions. Include failed-attempt, router, verifier and tool costs. Missing billing is unknown, not free.
- Report actual route sequence, trigger/reason, verification result, must-retain score, human corrections, task outcome, budget outcome and safety/data-boundary outcome independently.

The [observability CSV](../templates/token-observability-measurement.csv) can hold the run totals; the attempt ledger explains those totals. Do not count both as independent usage records.

## Score And Report

Score each output against the unchanged corpus rubric, preferably with the evaluator unaware of the arm. Keep required evidence, incorrect claims, failure conditions and correction effort visible. Any model-based evaluator must be fixed across arms, and its usage belongs in the ledger.

Report task pass separately from governed success. A governed success requires a task pass, passed verification, no boundary/approval failure, and compliance with the declared budgets. Correctly stopping an unsafe route may pass the safety scenario while leaving the task unsuccessful; do not relabel that as a completed task.

For each arm and cache/failure stratum, publish the scheduled count, completed count, governed successes, failures, blocked/aborted runs, unknown telemetry count, route distribution and raw records. Report per-case results before aggregate results so task mix cannot conceal regressions. Use the same predeclared task weights for all arms.

```text
governed success rate = governed successes / all scheduled runs
cost per verified outcome = total workflow cost across all runs / governed successes
```

Use one clearly named cost view per calculation. With no governed successes, report the ratio as undefined. With missing costs, disclose the incomplete subtotal and coverage; do not claim a total-cost saving. Include all unsuccessful runs and amortized preparation costs in the numerator.

Report latency distributions and sample counts for all terminal outcomes and for successes separately. Timeouts are censored/limited observations, not fast successes. Five trials do not establish reliable tail latency; publish raw durations and avoid unsupported percentile precision. Compare paired tasks/trials and disclose uncertainty, model drift, cache differences, rate limits and unobserved costs.

A routing or fallback policy is not an improvement merely because it uses fewer tokens or rescues one task. Report quality, failure rate, budget compliance and data-boundary outcomes alongside any cost/latency difference. This protocol contains no benchmark result.
