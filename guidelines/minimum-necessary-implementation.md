# Minimum-Necessary Implementation

Token efficiency is not only about shorter prompts. AI coding agents can also waste tokens, review time, dependencies, and future maintenance by building more software than the requirement needs.

Use a **minimum-necessary implementation** check before writing new code.

## Decision Ladder

Stop at the first option that satisfies the requirement safely:

1. **Does this need to exist?** Remove speculative scope and unrequested flexibility (YAGNI).
2. **Does the repository already solve it?** Reuse an existing helper, convention, component, script, or workflow.
3. **Does the standard library solve it?** Prefer a maintained built-in capability over custom code.
4. **Does the native platform solve it?** Prefer browser, shell, database, cloud, framework, or operating-system primitives when they meet the requirement.
5. **Does an already-approved dependency solve it?** Reuse what is already present before introducing another package.
6. **What is the smallest clear implementation?** Add only the code required for the accepted behaviour and verification.

A new dependency is not automatically better than a few lines of code, and a one-liner is not automatically better than readable code. Choose the smallest solution that remains understandable, testable, supportable, and compatible with the repository.

## Never Optimise Away Safety

Minimality is not code golf. Do not remove or weaken:

- input validation required by the trust boundary;
- authentication, authorisation, secret handling, or security controls;
- error handling needed for safe failure and diagnosis;
- accessibility requirements;
- compatibility requirements that are part of the acceptance criteria;
- rollback, audit, or observability controls required by the environment;
- tests that protect meaningful behaviour.

If removing code changes a required property, it is not an efficiency improvement.

## Agent Workflow

Before implementing, record the first rung that works:

```text
Requirement -> existing solution? -> stdlib/native? -> existing dependency? -> minimum new code -> targeted verification
```

For a non-trivial change, the agent should be able to answer:

- What requirement requires this code?
- What existing option was checked first?
- Why is new code or a dependency necessary?
- What is the smallest useful verification?
- What would make the implementation too small to be safe or maintainable?

## Measure Total Engineering Output

Do not treat token count as the only success metric. Compare approaches using the same task and acceptance criteria, then record:

- input and output tokens;
- new and changed lines of code;
- new dependencies or services introduced;
- tool calls and retries;
- verification effort and result;
- latency and cost where available;
- maintainability signals such as duplicated logic or unnecessary abstraction;
- correctness and safety failures.

A lower-token answer that creates more code, dependencies, retries, or review effort can be a net loss.

## Practical Examples

| Request | Prefer | Avoid |
| --- | --- | --- |
| Cache a pure function | Existing/stdlib cache primitive when suitable | A custom cache manager without a requirement for one |
| Parse a standard data format | Existing stdlib or approved parser | A new parser written from scratch |
| Add a simple browser control | Native accessible platform control when it meets UX needs | A new UI dependency for basic behaviour |
| Add shared logic | Existing local helper if semantics match | A second near-duplicate abstraction |
| Support hypothetical future variants | Implement current accepted variants | Speculative plugin layers and extension points |

## Review Gate

Before merging an AI-generated change, ask:

> If the same requirement can be met with less new surface area and the same safety, correctness, clarity, and verification, why are we keeping the extra surface area?

Use this as a design question, not a demand for the fewest possible lines.

## Upstream Inspiration and Attribution

This guidance was informed by the decision-ladder idea in [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), reviewed 2026-09-19. Ponytail is MIT-licensed and publishes its own benchmark results. This playbook does **not** adopt those percentages as general facts; quantitative savings must be reproduced on the local evaluation corpus and environment before being claimed here.
