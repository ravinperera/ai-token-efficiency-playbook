# Minimum-Necessary Implementation Benchmark

Use this benchmark to compare implementation approaches against the **same requirement and acceptance criteria** while measuring total engineering cost, not just reply length, token count, or lines of code.

The benchmark tests whether a reuse-first, YAGNI-oriented implementation reduces unnecessary engineering surface without weakening correctness, security, accessibility, operability, or maintainability.

## Comparison Arms

Run at least two comparable arms:

1. **Baseline implementation** — the normal agent/tool workflow with no extra minimum-necessary instruction beyond the repository's ordinary rules.
2. **Minimum-necessary implementation** — use the decision ladder in [`../guidelines/minimum-necessary-implementation.md`](../guidelines/minimum-necessary-implementation.md): remove speculative scope, reuse repository capabilities, prefer standard/native functionality, reuse approved dependencies, then add the smallest clear new implementation.

An optional third arm may test a deliberately terse or "fewest lines" instruction, but treat it as a safety control rather than an optimisation target. The shortest implementation is not the benchmark winner if it drops required behaviour or safeguards.

## Choose A Reproducible Task

Pick a task with objective acceptance criteria and at least one plausible over-building trap, for example:

- add a browser control that may already exist natively;
- parse or transform a standard format with a standard-library option;
- add caching, retries, validation, or rate limiting where local primitives may already exist;
- extend a repository that already contains a suitable helper or dependency;
- implement a small feature where speculative extensibility would be easy to add unnecessarily.

Pin the repository revision. Keep the task wording, source state, tool permissions, model/provider settings, and verification procedure constant across arms.

## Protect Required Engineering Surface

Before each run, identify controls that are **not removable waste**. Typical examples include:

- trust-boundary validation;
- authentication, authorisation, secret handling, and security checks;
- data-loss prevention and safe error handling;
- accessibility required by the acceptance criteria;
- compatibility and migration behaviour that is actually required;
- rollback, audit, logging, or observability controls required by the environment;
- tests that protect meaningful behaviour.

If an arm saves tokens or code by dropping a required property, record the run as a correctness/safety failure rather than a successful optimisation.

## Required Measurements

Capture the complete workflow, including failed attempts and verification.

| Metric | Baseline | Minimum-necessary | Optional terse control |
| --- | ---: | ---: | ---: |
| Input/context tokens | | | |
| Output/reasoning tokens where exposed | | | |
| Cached input/read/write tokens where exposed | | | |
| Model/tool turns | | | |
| Retries/fix cycles | | | |
| Wall-clock time | | | |
| Actual/estimated model cost | | | |
| Files changed | | | |
| Lines added/changed | | | |
| New dependencies | | | |
| New services/runtime components | | | |
| New configuration surface | | | |
| Tests added/changed | | | |
| Verification commands/checks | | | |
| Verification time | | | |
| Review comments or rework events | | | |
| Acceptance criteria passed | | | |
| Safety/accessibility controls preserved | | | |
| Reused existing/native capability | | | |

If a metric is unavailable, record `N/A`; do not infer it from unrelated signals.

## Total Engineering Cost

Do not collapse every metric into one universal score. Report the important dimensions separately, then explain the trade-off.

A useful comparison asks:

```text
Did the approach meet the same requirement with less new surface area,
less model/tool work, and no loss of correctness or required safeguards?
```

For local experiments, teams may define a weighted score, but the weights must be documented before inspecting the results. Avoid weights that make security, correctness, or required accessibility tradeable for cheaper tokens.

## Reuse And Warm-State Effects

Reuse can make later tasks cheaper, but an existing helper, dependency, cache, generated asset, or local index may itself have historical creation/maintenance cost.

Record when an arm benefits from:

- a pre-existing repository helper or component;
- an already-installed dependency;
- warm model/provider cache state;
- generated or indexed context created earlier;
- environment-specific tooling not available to every arm.

Do not charge a task the full historical cost of a mature shared dependency unless that is the decision being evaluated, but do not present warm-state reuse as a universal first-use saving either.

## Correctness And Safety Gate

A run is not comparable as a successful implementation if it:

- misses an acceptance criterion;
- breaks an existing test or documented compatibility requirement;
- removes required validation, security, accessibility, recovery, or audit behaviour;
- adds hidden manual steps not represented in the measurement;
- relies on an undeclared dependency, service, or external state;
- cannot be verified independently.

Keep failed runs in the raw data. Failure/retry cost is part of the engineering cost.

## Reporting

For repeated or non-deterministic runs, report the median and range for quantitative metrics and preserve raw rows. Separate:

- **code-surface reduction** from **token reduction**;
- **model/API cost** from **engineering/review effort**;
- **reuse benefits** from **first-use setup cost**;
- **shorter code** from **lower maintenance burden**;
- **successful minimality** from **unsafe omission**.

Use [`../templates/minimum-necessary-implementation-measurement.csv`](../templates/minimum-necessary-implementation-measurement.csv) for raw measurements and [`../templates/benchmark-run-manifest.md`](../templates/benchmark-run-manifest.md) for the environment/model/source provenance of material benchmark runs.

## Upstream Inspiration And Attribution

The reuse-first decision ladder and the idea that unnecessary code can increase total engineering cost were informed by [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), reviewed 2026-09-23. Ponytail is MIT-licensed and publishes its own reproducible benchmark methodology and results.

This benchmark does **not** import Ponytail's headline percentage savings as general facts. Treat upstream numbers as hypotheses until the same task, environment, model/tool setup, acceptance criteria, and verification are reproduced locally.