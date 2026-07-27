# Model Routing

Do not use the strongest model for every task. Use the **lowest approved model tier that can complete the task correctly**, then verify the result in proportion to the risk.

Model routing saves cost and latency only when it preserves correctness, security, data-handling requirements, and useful verification.

## Vendor-Neutral Model Tiers

Use capability tiers rather than hard-coding model names. Providers change model names and availability frequently.

| Tier | Intended use | Typical characteristics |
| --- | --- | --- |
| Economy / fast | Simple, bounded, low-risk work | Low latency, low cost, limited deep reasoning |
| Balanced | Normal engineering work with moderate reasoning | Better code understanding and multi-step execution |
| Advanced reasoning | Complex, ambiguous, high-risk, or cross-system work | Stronger reasoning, planning, and error analysis |

Map these tiers to models that are approved by your organisation and available in your tool.

## Good Economy / Fast Tasks

Use an economy or fast model when the task is bounded, reversible, and easy to verify, such as:

- formatting Markdown, YAML, JSON, or messages;
- rewriting or shortening supplied text;
- extracting lists, fields, headings, or action items;
- classifying already-provided content;
- summarising a known document or selected log section;
- generating simple documentation from explicit facts;
- producing a small code snippet from complete requirements;
- mechanical search-and-replace changes;
- adding straightforward tests for already-understood behaviour;
- converting structured information into a requested template.

A task is not simple merely because the requested answer is short. A one-line IAM, authentication, database, or production change can still be high risk.

## Good Balanced Tasks

Use a balanced model for ordinary engineering work that needs context and judgement but remains scoped, such as:

- a well-defined bug fix in one component;
- a small feature with clear acceptance criteria;
- focused code review;
- test failure diagnosis with a clear error and relevant files;
- a limited refactor with known compatibility requirements;
- Terraform or workflow explanation that does not change production controls;
- documentation that requires reconciling several repository files.

## Advanced Reasoning Tasks

Start with or escalate to an advanced reasoning model for:

- architecture and platform design;
- security review, threat modelling, or privilege analysis;
- production incident analysis;
- infrastructure, IAM, DNS, networking, database, or deployment changes;
- ambiguous or conflicting requirements;
- broad multi-file or multi-service changes;
- unfamiliar code with unclear ownership or side effects;
- data-loss, privacy, legal, financial, or safety-sensitive decisions;
- root-cause analysis after a simpler attempt fails;
- tasks requiring comparison of several plausible designs.

## Routing Decision

Use this sequence before starting substantial work:

```text
1. Confirm approved provider, model family, and data boundary.
2. Classify task risk and reversibility.
3. Estimate reasoning and context complexity.
4. Choose the lowest capable approved tier.
5. Run the smallest useful verification.
6. Escalate when a trigger is reached; do not loop repeatedly.
```

## Mandatory Escalation Triggers

Escalate from economy/fast to balanced or advanced reasoning when any of these occur:

- the request touches security, authentication, authorisation, IAM, secrets, or cryptography;
- production systems, customer data, infrastructure, deployments, migrations, or destructive actions are involved;
- requirements are incomplete, contradictory, or materially ambiguous;
- the change crosses several files, services, repositories, or trust boundaries;
- the model cannot explain the likely blast radius or rollback path;
- verification fails or the first result is materially incorrect;
- the task requires choosing between architectural or operational trade-offs;
- sensitive data requires a different approved model, region, tenancy, or provider boundary;
- the model starts guessing missing facts instead of requesting the required context.

Retry a failed economy-tier attempt at most once when the failure is clearly transient or easily corrected. Otherwise escalate the tier or stop and report the blocker.

## Automatic Routing vs Recommendation

Some agent hosts can select a model programmatically; others cannot.

- **When automatic routing is supported and authorised:** select the lowest approved tier that meets this policy.
- **When automatic routing is unavailable:** state the recommended tier in the plan or handoff. Do not pretend that a model switch occurred.
- **When the user explicitly selected a model:** do not silently override that choice. Recommend a different tier only when it materially affects cost, capability, or safety.
- **Never silently switch provider, tenancy, region, retention policy, or data boundary.** Model cost is secondary to approved data handling.

Example recommendation:

```text
Recommended tier: Economy / fast
Reason: Documentation formatting only; no code or security decisions.
Verification: Markdown lint and link check.
Escalate if: Source documents conflict or technical claims require validation.
```

## Verification by Tier

Lower-cost routing must not remove validation.

| Tier | Minimum verification examples |
| --- | --- |
| Economy / fast | Format check, schema parse, exact-field comparison, targeted lint |
| Balanced | Relevant unit test, focused diff review, targeted build or validation command |
| Advanced reasoning | Tests plus security/operational review, rollback analysis, stakeholder or human approval where required |

A stronger model is not a substitute for tests or human approval. A lower model is not acceptable when its result cannot be checked cheaply and reliably.

## Practical Examples

| Task | Starting tier | Escalation condition |
| --- | --- | --- |
| Reformat a README table | Economy / fast | Technical content is inconsistent |
| Extract action items from supplied notes | Economy / fast | Notes contain conflicting ownership or deadlines |
| Summarise selected CI error lines | Economy / fast | Root cause is not evident from the selected evidence |
| Fix a scoped unit-test failure | Balanced | Failure spans components or behaviour is unclear |
| Review a GitHub Actions OIDC trust policy | Advanced reasoning | Always high risk; requires least-privilege review |
| Design an AWS multi-region recovery pattern | Advanced reasoning | Always architectural and operationally significant |

## Anti-Patterns

Do not:

- route solely by prompt length;
- use an economy model for a high-risk one-line change;
- keep retrying a weak model to avoid escalation cost;
- send confidential content to a cheaper but unapproved provider;
- use an advanced model for deterministic formatting that a simple tool can perform;
- claim savings without recording the model, task, context, result, and verification;
- assume model names map permanently to the same capability tier.

## Reusable Routing Record

Use [`templates/model-routing-decision.md`](../templates/model-routing-decision.md) when routing decisions need to be visible or measured.

## Practical Rule

> If a task does not require deep reasoning, do not pay for deep reasoning. If risk or ambiguity rises, escalate early rather than paying for repeated weak attempts.
