# Selective Skill Loading

Large agent skill libraries can improve specialist performance, but preloading every skill into every session wastes context and makes it harder to reason about which instructions are active.

Prefer discovery and selective loading: identify the smallest relevant skill set for the task, load only those instructions and dependencies, and keep unrelated skills out of the active context.

## Recommended Flow

```text
classify task -> discover candidate skills -> inspect metadata -> select minimum set -> load -> execute -> verify -> unload or refresh when no longer needed
```

The runtime may implement this with built-in skills, plugins, MCP resources, repository-local instruction files, or another mechanism. The pattern is intentionally vendor-neutral.

## Discover Before Loading

Keep the always-on routing layer small. It should know enough to find skills, not contain the full content of every skill.

A useful discovery record includes:

- skill name and purpose;
- source repository or package;
- version, release, or commit identifier;
- supported agent/runtime or platform prerequisites;
- required packages, binaries, APIs, or data sources;
- permissions or external actions the skill may request;
- expected inputs and outputs;
- known limitations or high-risk use cases.

Load the actual skill instructions only after the task matches the skill's purpose.

## Prefer The Minimum Sufficient Skill Set

More skills are not automatically better. Overlapping instructions can increase context, produce conflicting procedures, and make failures harder to diagnose.

Use these rules:

1. Start with the smallest skill that covers the requested workflow.
2. Add another skill only when the task needs a distinct capability.
3. Avoid loading broad domain packs when a single procedural skill is enough.
4. Do not keep completed-task skills active merely because they were useful earlier in the session.
5. If two skills conflict, resolve the conflict before execution rather than allowing instruction order to decide silently.

## Record Provenance And Version

Reproducible agent work needs reproducible procedural knowledge.

For material tasks, record which skill version was used. A release tag or immutable commit is preferable when repeatability matters. If a floating branch or latest version is used, record that fact and the retrieval time.

Do not describe a result as reproducible when the skill, dependency, model, data source, or configuration can change without being recorded.

## Keep Dependencies Explicit

A skill that depends on a Python package, CLI, database, hosted API, GPU, browser, or operating-system feature should say so before execution.

Before installing or invoking a dependency:

- check whether it is already available;
- confirm that the dependency is allowed in the current environment;
- avoid installing a broad package set for a narrow task;
- separate local dependencies from external services and network calls;
- preserve existing approval requirements for downloads, installation, authentication, and data egress.

Token efficiency is not a reason to bypass software-supply-chain or data-boundary controls.

## Separate Skill Discovery From Authority

Finding a skill must not grant new permissions.

A skill may describe how to publish, delete, install, download, call an external service, or modify a system, but the agent still needs the authority and approval required by the surrounding environment.

Use the same principle for high-stakes domains: specialist instructions can assist with evidence gathering and analysis, but they do not replace qualified human or institutional accountability for clinical, regulatory, safety, legal, or similarly consequential decisions.

## Preserve Raw Evidence For Reproducible Work

When a skill transforms scientific, analytical, or engineering data, keep authoritative raw inputs immutable where practical and record:

- source identifiers and retrieval time;
- parameters and configuration;
- dependency and tool versions;
- random seeds where relevant;
- checksums or artifact versions where useful;
- transformation steps that produced derived outputs.

Do not save only the agent's summary when exact evidence is needed to reproduce or audit the result.

## Refresh And Unload

A skill should not remain trusted forever merely because it was loaded once.

Refresh or re-evaluate when:

- the task changes materially;
- the skill source or version changes;
- dependencies or APIs change;
- permissions or data boundaries change;
- the skill's output conflicts with current authoritative evidence;
- a high-risk action requires current approval.

Unload or exclude skills that no longer contribute to the current task so their instructions do not consume context or influence unrelated work.

## Measure The Trade-Off

Compare selective loading with preloading using the same task and success criteria. Capture:

- always-on instruction tokens;
- skill-discovery tokens and tool calls;
- loaded-skill tokens;
- total input and output tokens;
- discovery and execution latency;
- task success and verification result;
- wrong-skill or missing-skill failures;
- conflicting-instruction incidents;
- dependency setup cost.

A selective approach is useful only if it preserves task quality and required safety controls.

## Reusable Skill Manifest

Use [`templates/agent-skill-manifest.md`](../templates/agent-skill-manifest.md) to keep discovery metadata small and portable. The manifest records identity, immutable source/version, runtime prerequisites, dependencies, permissions, external actions, expected inputs/outputs, reproducibility metadata, refresh triggers, and human-accountability requirements without preloading the skill's full procedure.

The manifest is descriptive metadata, not an authorization grant. A runtime must still enforce its own permission, approval, installation, network, data-boundary, and high-risk review controls before executing the skill.

## Upstream Inspiration

[K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) is one useful example of a large, portable collection of procedural skills for specialist workflows. Its skill-oriented packaging, explicit scientific tooling, reproducibility emphasis, and warnings around installing only needed skills informed this guide. This playbook does not copy the repository's skill content or treat its compatibility, adoption, or performance claims as independently verified facts.
