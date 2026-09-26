# Question Pause Control

Use this rule for interactive coding, operations, debugging, and long-running agent work.

## Core rule

When the user asks a status, explanation, clarification, or safety question:

1. Stop starting new work.
2. Answer the question first.
3. Do not resume execution until the user explicitly says `continue`, `proceed`, `approved`, `go ahead`, or `try again`.

A question is a control handoff, not permission to answer briefly and continue in the background.

## Answer-and-pause mode

While answering the question, do not:

- run commands or start tool calls that are not required to answer;
- edit files or create commits;
- poll builds, deployments, jobs, or external systems;
- retry blocked work;
- open, approve, merge, or close pull requests;
- apply infrastructure or make production changes;
- continue unrelated discovery or preparation.

If work is already running asynchronously, state that clearly. Do not launch additional work.

## Questions that trigger the pause

Examples include:

- What is happening?
- What is blocked?
- Why are you asking for approval?
- What are you changing?
- What remains?
- Is this safe?
- Can you explain the error?
- Which option do you recommend?

Treat ambiguous user messages ending in a question as a pause unless the user also gives an explicit continuation instruction.

## Allowed work while paused

Use a tool only when it is necessary to answer the question accurately, such as reading the current job status after the user asks whether it completed. Keep the read narrow and do not mutate state.

After answering, stop. Do not append a new execution plan unless the user requested one.

## Resume phrases

Execution may resume only after an explicit instruction such as:

- `continue`
- `proceed`
- `approved`
- `go ahead`
- `try again`

A thank-you, acknowledgement, emoji, or follow-up question is not a continuation instruction.

## Fail-fast rule

For external failures:

1. Retry at most once when the failure appears transient.
2. If the retry fails, stop.
3. Report the exact blocker.
4. State the single action needed from the user or system owner.

Do not keep polling, broaden the investigation, or repeat checks the user has already confirmed.

## Response shape

Use this concise structure:

```text
Answer: <direct response>
Current state: <running, paused, blocked, or complete>
Needed to continue: <one explicit action, only when required>
```

## Self-check

Before sending the answer, confirm:

- the user's question was answered directly;
- no mutation or unrelated work continued;
- polling and retries stopped;
- any active asynchronous work was disclosed;
- execution will not resume without an explicit continuation phrase.
