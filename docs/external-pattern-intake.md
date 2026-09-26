# External Pattern Intake And Provenance

This playbook should learn from strong public projects without becoming a copy of them. Use this process when a contribution is materially inspired by another repository, paper, standard, benchmark, or tool.

The objective is to keep one practical, vendor-neutral reference while preserving provenance, licence obligations, and evidence quality.

## 1. Start With A Local Gap

Before importing an idea, state the problem in this repository that the pattern would solve.

Good reasons include:

- an existing guideline is incomplete or ambiguous;
- a recurring token-waste pattern has no practical control;
- a benchmark is missing an important comparison;
- a provider-specific technique can be generalized safely;
- a new agent/runtime pattern changes how context should be retrieved, stored, or measured.

Do not add a pattern only because another repository is popular or because it creates activity.

## 2. Record The Source

For each material source, capture enough information for a future maintainer to find the same evidence again.

| Field | Record |
| --- | --- |
| Project or source | Repository, paper, standard, article, or tool name |
| Canonical URL | Stable upstream location where possible |
| Revision | Commit, tag, release, standard version, or review date |
| Licence | Upstream licence or `not identified` |
| Useful concept | The reusable idea being evaluated |
| Local gap | The problem this repository needs to solve |
| Evidence status | Reproduced, independently verified, source claim only, or not applicable |

A commit or tagged release is preferable to a moving `main` branch when the exact upstream behaviour matters.

## 3. Separate The Idea From The Implementation

Extract the general engineering principle before writing local guidance.

For example:

```text
upstream implementation detail -> reusable principle -> local vendor-neutral control
```

Prefer describing the principle in the playbook's existing vocabulary. Do not import another project's directory layout, naming scheme, prompts, policy text, or code unless doing so is genuinely useful and permitted.

When substantial text, code, data, or examples are reused, confirm that the licence permits the intended reuse and preserve any required notices or attribution. If the licence or reuse conditions are unclear, summarize the idea in original wording or do not reuse the material.

## 4. Validate Claims Independently

Treat upstream quantitative claims as hypotheses, not facts for this playbook.

If a source claims a token, cost, latency, quality, or context reduction:

1. identify the exact task and baseline;
2. preserve equivalent success criteria and required evidence;
3. measure the complete workflow, including indexing, compaction, fallback reads, retries, and verification where relevant;
4. record provider/model/tool versions that materially affect the result;
5. report limitations and failed cases alongside successful runs.

Use the repository's [evaluation corpus](../benchmarks/evaluation-corpus.md) and benchmark protocols when they fit. Do not convert one upstream result or one local run into a universal saving percentage.

## 5. Integrate Once, Then Link

Add the synthesized rule to the single canonical location that owns it:

- `guidelines/` for operating rules and patterns;
- `benchmarks/` for measurement methods;
- `templates/` for reusable capture formats;
- `checklists/` for short operational gates;
- provider adapters only for provider-specific routing or syntax.

If another document needs the same rule, link to the canonical source instead of copying the paragraph. This reduces both maintenance drift and token duplication.

## 6. Preserve Safety Boundaries

A source pattern must not weaken existing controls merely because it is more token-efficient. In particular, do not bypass:

- approved provider, tenancy, region, retention, or data boundaries;
- secrets and sensitive-data restrictions;
- human approval or independent review required by risk;
- production, security, compliance, or architecture escalation;
- exact evidence needed to verify a consequential result.

## 7. Leave A Maintenance Trail

In the pull request, summarize:

- the source and revision reviewed;
- the concept adopted;
- what was deliberately not copied or generalized;
- how claims were validated, or why no quantitative claim is made;
- the canonical local document that now owns the rule.

Revisit the source only when its behaviour materially changes, a local benchmark contradicts the guidance, or the upstream licence/availability changes. The playbook should remain useful even if the upstream project disappears.

## Decision Rule

Adopt an external pattern when it is **useful, generalizable, supportable, and safer or clearer than the current guidance**. Otherwise, document nothing and keep the repository smaller.
