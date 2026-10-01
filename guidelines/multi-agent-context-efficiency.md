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

## Observe Progress Without Replaying Terminal History

A coordinator can waste context by repeatedly asking a model to inspect unchanged terminal output. When the runtime supports them, prefer bounded event subscriptions or server-side waits over model-driven polling loops. A wait must have a deadline and a cancellation path; unavailable event support calls for bounded polling with backoff, not an invented background capability.

Use a small observation cycle:

```text
bind the intended task and runtime target
-> wait for relevant activity or a deadline
-> read the smallest useful new output
-> verify the task-specific result
```

- Bind the machine, session, current agent/process identity, task identifier and source revision. A pane label or UI focus alone is insufficient, especially across machines or after reconnecting.
- Check the current state and use atomic submit-and-wait, an event cursor, or an equivalent race-safe mechanism where available. An old success message or a different occupant must not satisfy the current task's wait.
- Request bounded text output or a relevant artifact first. Distinguish model-visible context from terminal bytes that never entered a model request. Do not request extra screenshots or replay the full transcript when a small text result is enough.
- Treat runtime labels such as working, blocked, idle, done and unknown as observation signals with integration-specific meanings. Readiness for another prompt is not verified task success; an approval dialog is not authorization to approve.
- On timeout or disconnection, inspect authoritative state before resubmitting. A lost reply does not prove the prompt or command was never delivered. After reconnecting, refresh stale state and re-establish interrupted waits rather than trusting an old subscription.

### Reconnect Before Reconstructing

Separate three recovery cases: reattaching to surviving processes, restoring terminal layout/history after processes died, and resuming an agent's native conversation. The latter two do not prove that a test, deployment or other external action is still running or should be repeated.

Discover the actual recovery case, reconcile the task and its artifacts, then retrieve only the missing evidence. Do not restart an entire swarm or feed it full history solely because the client disconnected. Replayed terminal text is historical evidence, not a live completion signal.

### Measure Monitoring Overhead

For the same tasks, agents and verification criteria, compare periodic output reads with event-driven observation. Record model-visible monitoring tokens as a subset of total workflow tokens, duplicate output, observation calls, missed/stale events, detection latency, recovery effort and verified outcomes. Include server-side wait overhead and failed runs; fewer tool calls alone do not prove lower cost. No saving is claimed without comparable measurements.

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

Use the [multi-agent orchestration cost benchmark](../benchmarks/multi-agent-orchestration-cost.md) and its reusable measurement template when comparing workflow designs.

## Handoff Checklist

Before sending work to another agent, ask:

- Can the recipient resolve the authoritative state from a stable reference?
- Am I repeating files, logs, or discussion already available there?
- Does this role need every piece of context I am sending?
- Can I send the changed paths and exact failure signal instead?
- Is a new agent actually required, or can the current scoped agent finish safely?
- Will the total workflow still be measured rather than only this agent's context?

For a reusable structure, see [`../templates/handoff-template.md`](../templates/handoff-template.md).

## Runtime Coordination Design Reference

The observation and recovery guidance is informed by [Herdr's agent skill](https://github.com/herdrdev/herdr/blob/d6b40d4edd550ccea081f089605a64314f8c8b27/skills/herdr/SKILL.md), reviewed at commit `d6b40d4edd550ccea081f089605a64314f8c8b27` on 2026-10-01, and its [socket API](https://herdr.dev/docs/socket-api/) and [session-state documentation](https://herdr.dev/docs/session-state/) reviewed on the same date. The pinned repository [licence](https://github.com/herdrdev/herdr/blob/d6b40d4edd550ccea081f089605a64314f8c8b27/LICENSE) is Apache-2.0. These are original, vendor-neutral adaptations; no runtime implementation, bundled skill, or performance claim is copied. Herdr is not installed or required by this playbook. Validate supported waits and state semantics against the actual installed runtime version.
