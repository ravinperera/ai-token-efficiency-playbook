# Token Observability And Attribution

Token optimisation is hard to improve when usage is visible only as one monthly total. Measure the work at the level where decisions are made: task, tool, model tier, project, cache behaviour, retries, and outcome.

The objective is not to maximise a single savings percentage. The objective is to explain where cost and context were spent, identify avoidable waste, and verify that cheaper execution still produces an acceptable result.

## Minimum Measurement Record

For each meaningful AI-assisted task, record the fields that are available without collecting sensitive prompt content:

- timestamp or run identifier;
- project or repository identifier, preferably pseudonymised when names are not needed;
- task category such as review, debugging, generation, extraction, or documentation;
- tool or agent host;
- provider and capability tier or model identifier;
- input, output, cached-input, and cache-write tokens when the provider exposes them;
- measured API cost or the pricing assumption used to estimate cost;
- number of model attempts, retries, and escalations;
- elapsed time;
- outcome or verification result.

Do not invent missing telemetry. Use `unknown` or leave a field blank and document the limitation.

## Separate Model Identity, Hosting And Measurement Basis

Keep the model developer/family, hosting platform and actual deployment route distinguishable. One family served directly and through a cloud platform is not two independent model families, but its routes can have different billing and approved data boundaries. Preserve requested identifiers and the model/route actually resolved after fallback. Normalise aliases only with a dated mapping to verified versions; an unfamiliar alias stays unresolved rather than being guessed into a family.

Use the existing measurement CSV's `route_id` and `run_id` to reference a versioned side record for hosting platform, model family/version, route resolution and observation coverage. Define what the existing `provider` field means for the dataset and keep that interpretation stable. Do not put credentials, account secrets or private endpoint URLs into public records, or change the established CSV columns to capture one report.

### Counts And Denominators

Before comparing routes or publishing a share, record the window, eligible cohort, metric unit, aggregation/weighting method, missing coverage and deduplication rule.

- Distinguish logical tasks, model-request attempts, tool/MCP operations and agent handoffs. A retry is another attempt, not another successful task; a tool call does not automatically have model-token usage.
- Count a model attempt once even when the client, gateway and provider all log it. Keep model-family and hosting-platform totals as alternate views of those same attempts, not totals to add together.
- Request share, input-token share and output-token share use different denominators. Retain failed attempts and known billable usage; missing usage stays unknown rather than zero. Report denominators based only on measured records as such.
- Record whether results pool requests or weight organisations/projects equally. Label top-N-only, sampled, filtered and observed-gateway subsets; do not describe them as the whole estate or market.
- Keep cache-token semantics and billing basis explicit. Do not add cached tokens again when already included in input totals; a higher raw-token share is not automatically a higher billed-cost share.
- Separate deployment/alias counts from verified distinct models. Traffic concentration alone does not establish task complexity, model quality, causal business value or governance coverage.

For a non-zero denominator, each share is `route's measured quantity / total measured quantity on the same basis`. A zero denominator makes the share undefined. Unknown coverage must remain visible even when known shares sum to 100%.

### Fictional Accounting Example

These invented values illustrate arithmetic only; they are not benchmark results or facts from the source report. Assume all model attempts and their token counts are observed in one window. Both routes serve the same verified fictional model family, with different hosting paths.

| Route | Hosting path | Attempts | Input tokens | Output tokens |
| --- | --- | --- | --- | --- |
| A | Direct | 10 | 90,000 | 2,000 |
| B | Cloud-hosted | 90 | 10,000 | 18,000 |
| Total | Both paths | 100 | 100,000 | 20,000 |

A accounts for 10% of attempts, 90% of input tokens and 10% of output tokens; B accounts for 90%, 10% and 90%, respectively. The family roll-up covers both paths once. None of these figures identifies the cheaper, safer or more accurate route without billing, task and verification evidence.

## Attribute Cost To Outcomes

Raw token totals are useful but incomplete. Prefer outcome-oriented measures such as:

```text
cost per successful task
tokens per successful task
attempts per successful task
cache-hit ratio
retry tax
routing waste
```

A run that uses fewer tokens but fails verification is not an efficiency win.

### Verified outcomes and incomplete tasks

Define the task cohort, observation cutoff, cost view and verification criteria before comparing results. Give each logical task one outcome at that cutoff: verified success, failed, cancelled/policy-stopped, or pending/unknown. A safe policy stop can be a successful safety decision without completing the requested task; report both dimensions. Do not relabel a pending check as either verified success or failure.

```text
cost per verified task = total cost of all tasks in the declared cohort / verified task count
```

Include known costs from failed, cancelled and pending tasks, plus retries and helpers, once in the numerator. Averaging only the costs of successful tasks answers a different question and must be labelled as survivor-only. With zero verified tasks the ratio is undefined, not zero. When costs or outcomes are incomplete, label the observation provisional, report known cost and missing coverage, and do not present it as a complete-cohort efficiency result. Keep the same cohort when later outcomes arrive; do not silently drop unfinished tasks.

### Retry tax

For a task that reaches verified success, use the following definition:

```text
pre-success retry tax = cost of unsuccessful attempts before the accepted successful attempt
```

Record the cost of tasks that never reached verified success separately; there is no final successful attempt from which to calculate their pre-success retry tax. In `retry_tax_cost`, leave that value blank with a not-applicable explanation in `notes` or a linked side record. Reserve zero for a measured zero, such as first-attempt success; missing attempt costs remain unknown. Do not change the CSV schema to encode the distinction.

Both pre-success retry tax and never-successful task cost are breakdowns of the cohort total, not additional costs to add on top. They are accounting categories, not proof that research, a rejected design or a safe stop had no value. Any alternative retry metric must have an explicit, stable definition rather than silently mixing these categories.

### Fictional mixed-outcome example

These invented USD amounts illustrate complete accounting, not measured model prices or performance. Assume all task costs, including any helpers and verification, are captured in the listed attempts at the same cutoff.

| Task | Attempt costs (USD) | Outcome | Total (USD) |
| --- | --- | --- | --- |
| A | 0.20 failed + 0.30 successful | Verified success | 0.50 |
| B | 0.15 failed + 0.25 failed | Failed | 0.40 |
| C | 0.10 before a policy stop | Stopped, not task-complete | 0.10 |
| Total | Five attempts | One verified task | 1.00 |

Cost per verified task is USD 1.00 / 1 = USD 1.00, not the survivor-only USD 0.50. A's pre-success retry tax is USD 0.20; B and C contribute USD 0.50 of never-successful task cost. These reconcile with A's successful attempt: 0.20 + 0.50 + 0.30 = USD 1.00. If A's verification is still pending, the verified count is zero and the provisional ratio is undefined. This example adds no new claim to the upstream sources below.

### Routing waste

Routing waste is the measured or estimated cost attributable to using a more expensive capability tier than the task needed.

Do not calculate it by assuming every task would succeed on the cheapest model. Establish the counterfactual with paired runs, historical evidence, or another reproducible method. Record the comparison model, pricing date, quality result, and any additional retries or latency.

## Account For Caching

Input-token totals can be misleading when providers price cached and uncached input differently.

When available, keep these separate:

```text
uncached input
cached input
cache writes
output
```

A change that slightly increases raw input tokens can still reduce cost if it improves prefix-cache reuse. Conversely, aggressive rewriting or compression can reduce raw tokens while destroying useful cache affinity.

Measure both token volume and billed cost rather than treating either one as a universal proxy for the other.

### Define Cache-Reuse Denominators

The term `cache-hit ratio` is ambiguous. Name the unit, eligible cohort, observation window, provider counter semantics, and missing coverage before publishing a percentage. Two different useful measures are:

- **Cached-input-token share:** `sum(observed reused/cached input tokens) / sum(observed input tokens)` for the same deduplicated attempts, **only when** the provider's input total already includes cached input. If it reports uncached and cached input as separate non-overlapping components, use their sum as the denominator instead. Cache writes are not reuse and do not belong in the numerator.
- **Eligible-request cache-hit rate:** `number of observed cache-eligible model attempts with >0 reused input tokens / number of observed cache-eligible model attempts`. Define eligibility using the provider's documented cache mechanism, including any minimum prefix or retention rules. A cache write or an attempted cache lookup alone is not a hit.

Count each submitted model attempt once, including failed attempts and retries with measured usage. A task may have multiple attempts; a tool call without model usage is not an automatic cache miss. When eligibility cannot be determined, report **observed reuse among telemetry-complete attempts** under that narrower label, not an eligible-request hit rate. Do not equate an unavailable cached-token counter with a measured zero.

For either metric, a zero denominator makes the result **undefined**. Publish the count of included attempts and the number excluded due to missing/incompatible counters or unknown eligibility. Do not pool providers or model routes with incompatible definitions until counts are normalised and their measurement coverage is disclosed.

**Fictional example (not measured performance):** Suppose two eligible attempts have complete, comparable counters. Attempt A has 1,000 total input tokens, 800 of them reused; B has 500 input tokens, none reused. The cached-input-token share is `800 / 1,500 = 53.3%`, while the eligible-request hit rate is `1 / 2 = 50%`. Neither percentage by itself proves a billed saving: actual cost also depends on uncached tokens, cache writes, output, pricing, any priming overhead and verification outcomes.

The existing [measurement CSV](../templates/token-observability-measurement.csv) carries input/cache token fields. Record cache eligibility, provider counter interpretation, unknown coverage and receipt/deduplication rules in its `notes` field or a versioned side record rather than silently changing the CSV schema.

## Subscription And API Cost Are Different Views

A coding assistant subscription, enterprise licence, bundled allowance, and pay-as-you-go API can represent the same model usage very differently.

Record which cost view is being used:

- **billed cost** — the amount actually charged for the measured usage;
- **API-equivalent estimate** — what the usage would cost at a documented public or contracted rate;
- **allocated subscription cost** — an internal allocation method for fixed-fee plans.

Never present an API-equivalent estimate as actual cash saved on a fixed subscription. If price tables are used, record their source and effective date because model pricing changes.

## Prefer Local Or Privacy-Preserving Collection

Usage analytics should not create a new sensitive-data pipeline merely to reduce AI cost.

Prefer telemetry that can be derived from local or provider-generated usage records without collecting full prompts, source code, retrieved documents, secrets, or user content. Where central reporting is required:

- minimise the fields collected;
- pseudonymise project or user identifiers when possible;
- document retention and access controls;
- separate operational metrics from raw conversation content;
- allow teams to understand what leaves the workstation or tenant boundary.

## Compare Changes With A Stable Baseline

When testing an optimisation, keep the task, repository revision, acceptance criteria, and verification method constant where possible.

Capture before and after values for:

```text
task success
input/output/cache tokens
attempts and retries
model tier
elapsed time
cost view used
verification result
```

Avoid publishing a general savings percentage from one unusually favourable task.

## Useful Diagnostic Questions

Ask these questions before changing prompts or model policy:

1. Which task categories consume the most total tokens?
2. Which tasks have the highest cost per successful outcome?
3. Where are repeated retries responsible for more cost than the final successful attempt?
4. Are expensive tiers being used for deterministic or low-risk work that succeeds on a lower approved tier?
5. Are cache misses caused by unnecessary prompt churn?
6. Are large projects or long-lived sessions carrying stale context that does not affect the result?
7. Is the reported saving a real billed saving or only an API-equivalent estimate?

## Guardrails

- Do not collect secrets or confidential content solely for cost analytics.
- Do not weaken verification to improve efficiency metrics.
- Do not silently move work across provider, tenancy, region, retention, or data-classification boundaries to reduce cost.
- Do not optimise for token count alone when retries, latency, quality, or cache behaviour move in the opposite direction.
- Keep counterfactual savings assumptions explicit and reproducible.

## Reusable Measurement Template

Use [`templates/token-observability-measurement.csv`](../templates/token-observability-measurement.csv) to record comparable runs without storing prompt or source content. The template separates uncached and cached input, retries, escalations, fallbacks, cost views, pricing assumptions, retry-tax inputs, routing counterfactuals, verification results, and the telemetry source.

Leave unavailable fields blank or mark them `unknown`; do not fabricate provider telemetry to make the record complete. When a routing-waste estimate is recorded, retain the reproducible counterfactual route and cost basis that produced it.

## Upstream Inspiration

[CodeBurn](https://github.com/getagentseal/codeburn) is one useful example of local-first, cross-tool usage attribution. Its project/model/task breakdowns, cache-aware accounting, retry-tax analysis, and routing-waste concepts informed this guide. This playbook does not depend on CodeBurn, copy its implementation, or adopt its pricing or savings claims as universal facts.

The separate identity and denominator views are informed by Kong's *The State of AI Governance*, supplied 18-page edition, pp. 7–10, reviewed 2026-10-05. Those pages distinguish model-family traffic, hosting routes, request counts and input/output token volume. A related [publisher article](https://konghq.com/blog/enterprise/enterprise-ai-governance) provides public context. The recording rules and fictional example above are original local guidance, not reproduced measurements. The report's customer-cohort shares and inferred workload explanations are not adopted as universal market shares, model-quality evidence or causal conclusions. No PDF text or artwork is reproduced. Source PDF SHA-256: `43867bd6a6b0e83dc4bbfdc0969d49352be53e59f48a1d69205b917e402d1417`.
