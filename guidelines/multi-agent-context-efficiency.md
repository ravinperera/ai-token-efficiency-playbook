# Multi-Agent Context Efficiency

Multi-agent workflows can reduce the context carried by each specialist, but they do not automatically reduce total token use. Orchestration adds prompts, handoffs, retries, duplicated evidence, and coordination turns.

Use multiple agents only when specialization, independent verification, parallelism, or risk separation provides enough value to justify that overhead.

## Start With The Smallest Workflow

Escalate gradually:

```text
one scoped agent -> small specialist pair -> larger role-based workflow
```

Prefer one agent when the task is narrow, reversible, and easy to verify. Add another role when there is a concrete reason, such as independent review, a distinct specialty, or safe parallel work. Avoid launching every available agent by default.

## Scope Context By Role

Each agent should receive only the evidence and instructions needed for its responsibility.

For example:

- an implementation agent needs the acceptance criteria, relevant files, and local validation commands;
- a security reviewer needs the diff, threat-relevant context, and policy boundaries rather than the whole development transcript;
- a documentation reviewer needs the changed behavior and affected documentation paths rather than every build log.

Shared repository rules can remain common, but task evidence should be selected for each role.

## Reference State Instead Of Repeating It

Prefer durable references over repasting large state between agents.

A useful handoff can often be reduced to:

```text
task -> repository/ref -> changed paths -> validation result -> unresolved question
```

Use commit SHAs, branch names, issue IDs, artifact paths, or other immutable/pinned references when the runtime can resolve them. Include a short summary only for facts that cannot be recovered cheaply from the referenced state.

Do not rely on vague pointers such as `latest`, `current changes`, or `the previous output` when the workflow can identify an exact revision.

## Keep Notifications Small

A notification should normally say that work is ready and where the authoritative state lives. It should not duplicate the entire task description, diff, logs, and prior discussion if those are already stored durably.

Separate:

```text
wake-up signal != durable task state != full history
```

This reduces repeated context and makes recovery easier when an agent session is restarted.

## Batch Similar Review Work Carefully

When several same-priority handoffs require the same review role, consider batching their identifiers and loading each relevant diff or artifact on demand. This can avoid repeatedly loading identical policy, repository, or tool context.

Do not batch unrelated high-risk work merely to save tokens. Separation can be more important than efficiency when tasks have different approval boundaries, data classifications, or blast radii.

## Avoid Context Amplification

Watch for these multi-agent anti-patterns:

- every agent receives the full conversation;
- every handoff repeats the complete diff or log;
- reviewer agents re-read the whole repository instead of the changed surface;
- downstream agents receive both raw evidence and several redundant summaries of it;
- retries replay unchanged context without narrowing the failure;
- a coordinator continuously republishes state already available through a repository, issue tracker, or artifact store.

Prefer search, exact references, changed-file lists, and minimal failure signals.

## Measure Total Orchestration Cost

Do not claim efficiency because each individual agent has a smaller context window. Measure the complete workflow.

At minimum track:

- total input/context tokens across all agents;
- total output tokens across all agents;
- handoff and coordinator tokens;
- retry and rework tokens;
- number of model turns and tool calls;
- elapsed time and cost where available;
- task success and validation result;
- safety or approval failures.

The relevant comparison is usually:

```text
single-agent total cost vs multi-agent total cost at comparable quality and safety
```

A multi-agent workflow can still be worthwhile when it costs more if it materially improves correctness, review independence, latency through safe parallelism, or risk control. Record that trade-off explicitly rather than labeling it a token saving.

## Handoff Checklist

Before sending work to another agent, ask:

- Can the recipient resolve the authoritative state from a stable reference?
- Am I repeating files, logs, or discussion already available there?
- Does this role need every piece of context I am sending?
- Can I send the changed paths and exact failure signal instead?
- Is a new agent actually required, or can the current scoped agent finish safely?
- Will the total workflow still be measured rather than only this agent's context?

For a reusable structure, see [`../templates/handoff-template.md`](../templates/handoff-template.md).
