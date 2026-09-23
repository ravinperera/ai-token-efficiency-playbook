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

### Retry tax

Treat repeated failed or abandoned attempts as a separate cost component.

```text
retry tax = cost of attempts before the final successful attempt
```

The exact formula can be adapted to the telemetry available. Keep the definition stable within a benchmark so runs remain comparable.

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
