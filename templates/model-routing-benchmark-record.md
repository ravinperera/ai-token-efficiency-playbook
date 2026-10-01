# Model Routing Benchmark Record

Blank capture template for the [routing/fallback benchmark](../benchmarks/model-routing-fallback.md). No values below are measured results. Reuse the [run manifest](benchmark-run-manifest.md) for source, model, tool and environment provenance and the [routing decision](model-routing-decision.md) for approved routes and boundaries.

## Frozen Comparison Plan

- Experiment ID and protocol/corpus commit:
- Manifest and routing-policy references/digests:
- Included case IDs and unchanged acceptance rubric:
- Approved fixed model for arm A:
- Versioned selection rules for arms B/C:
- Approved fallback order and triggers for C:
- Capability floor and approved data boundary per task:
- Total attempts, tokens, spend and elapsed-time ceilings (same for all arms):
- Same-route retry policy and unknown-cost reservation/stop rule:
- Cache strata, prefix digest, priming procedure and cost allocation:
- Trials per case/arm/stratum; randomized or rotated order/seed:
- Normal/failure scenarios; injected-event schedule; simulated versus observed:
- Verification method, evaluator and scoring version:
- Pricing source/date, currency and cost view:

## Per-Run Identity And Outcome

- Run ID, case ID, trial, arm A/B/C and order:
- Session and observed cache state (`cold | warm | mixed | unknown`):
- Failure scenario and execution mode (`observed | simulated | tabletop`):
- Scheduled/start/end timestamps; elapsed time:
- Initial route, actual route sequence and rejected candidates:
- Attempts submitted, retries, fallbacks and ambiguous requests:
- Must-retain items correct / required; failure conditions triggered:
- Verification evidence and result:
- Task result (`pass | fail | partial | blocked | aborted`):
- Budget result and stop reason:
- Boundary result (`within policy | prevented violation | actual breach | unknown`):
- Approval outcome, if applicable:
- Governed success (`yes | no`) and rationale:
- Human corrections and effort:
- Unknown telemetry, anomalies and evidence references:

## Attempt And Overhead Ledger

Repeat this block for each submitted request, including unsuccessful requests and model-based routing/verification. Record deterministic routing, rejected candidates and preparation as separately identified overhead events, not fake model attempts.

- Event ID; parent run ID; provider request ID or deduplication key:
- Event kind (`task | retry | fallback | routing | verification | cache preparation | rejected candidate`):
- Attempt number if submitted; route/model/version actually used:
- Selection/fallback reason; approval and boundary check before submission:
- Budget before/after, reserved cost and limit decision:
- Submitted/acknowledged/finished timestamps; delivery certainty:
- Observed input/output/total token counters and their source:
- Cached input, cache writes and reasoning counters; inclusion/overlap semantics:
- Normalized non-overlapping usage; unknown fields:
- Observed cache state and prefix/cache identity where available:
- Billed cost; API-equivalent estimate; allocated subscription cost (separate):
- Routing, queue/backoff, request, verification and tool durations:
- Tool/compute costs and allocation, if material:
- Status/error, partial output, verification and reconciliation evidence:

## Reconciled Totals And Comparison

- Unique request IDs included; duplicate receipts excluded:
- Total input/output/normalized tokens across all requests:
- Routing/verifier/retry token subsets (already included above):
- Preparation allocation and total cost by separate cost view:
- End-to-end elapsed time; phase timing subsets and overlaps:
- Scheduled/completed/successful/failed/blocked/aborted counts per arm/stratum:
- Per-case quality and governed success rates:
- Total cost including unsuccessful runs / governed successes, or undefined:
- Unknown-cost coverage and incomplete subtotals:
- Paired latency/cost differences, sample counts and uncertainty:
- Boundary failures, prevented violations, budget failures and approval failures:
- Evidence-store references; reviewer/date; limitations:

If exporting run totals to the [observability CSV](token-observability-measurement.csv), keep the same run IDs. Ledger events and aggregate rows are two views of the same usage, not additive datasets.
