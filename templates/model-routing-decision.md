# Model Routing Decision

Use this template when model selection affects cost, latency, capability, data handling, or safety.

## Task

- Request:
- Expected output:
- Scope:
- Reversibility: Easy / Moderate / Difficult

## Data Boundary

- Data classification: Public / Internal / Confidential / Restricted
- Approved provider or tenancy:
- Approved model family:
- Region or residency requirement:
- Retention or training restriction:

## Risk Classification

- Risk: Low / Medium / High / Critical
- Security or access impact:
- Production impact:
- Customer or personal-data impact:
- Destructive or irreversible action:

## Recommended Tier

- Tier: Economy / fast | Balanced | Advanced reasoning
- Reason:
- Host can switch automatically: Yes / No
- User selected a model explicitly: Yes / No

## Budget And Quota

- Maximum request/task cost, if used:
- Maximum attempts/retries:
- Token or latency ceiling, if used:
- Current quota/rate-limit constraint:
- Pricing/quota source and review date, if material:

## Context And Cache Plan

- Minimum files or evidence required:
- Context that should be excluded:
- Logs or documents to summarise first:
- Stable prefix/cache expected: Yes / No / Unknown
- Cache affinity may influence route: Yes / No
- Cache must not block escalation: Confirmed / N/A

## Fallback Policy

- Approved fallback route(s):
- Same provider/tenancy/region/retention boundary: Yes / No / N/A
- Fallback trigger(s): quota / rate limit / unavailable / transient error / budget / other
- Stop condition when no approved capable route remains:

## Verification

- Check or command:
- Expected result:
- Human approval required: Yes / No

## Escalation Triggers

Escalate or stop if:

- requirements are ambiguous or conflicting;
- the change crosses additional files, services, or trust boundaries;
- security, production, data-loss, or compliance risk appears;
- verification fails;
- the first result is materially incorrect;
- the model begins guessing missing facts;
- fallback would cross an unapproved data boundary;
- the current route no longer meets the required capability tier.

## Routing Telemetry

- Route initially selected:
- Route actually used:
- Fallback/escalation reason:
- Attempt count:
- Input tokens:
- Output tokens:
- Cached/read/write tokens, if exposed:
- Estimated or actual cost:
- Latency:

## Outcome

- Tier actually used:
- Result:
- Verification result:
- Escalated: Yes / No
- Escalation reason:
- Budget/quota outcome:
- Follow-up:
