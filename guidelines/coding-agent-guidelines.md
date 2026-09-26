# Coding Agent Guidelines

## Default Behaviour

Coding agents should operate like focused engineers:

- inspect only relevant context
- make narrow changes
- verify the change
- report only what matters

## File Reading

Prefer:

```text
Search -> open relevant file -> inspect relevant section -> edit -> test
```

Avoid:

```text
Open many files -> dump context -> explain everything -> edit broadly
```

## Editing

- Keep diffs small.
- Follow existing patterns.
- Do not reformat unrelated files.
- Do not add abstractions unless they reduce real complexity.
- Do not generate large code blocks when a small patch is enough.

## Conversation Control

A user question is a control handoff.

For status, explanation, clarification, or safety questions:

- answer first;
- stop commands, edits, polling, retries, PR actions, and unrelated preparation;
- report already-running asynchronous work without launching more;
- wait for an explicit `continue`, `proceed`, `approved`, `go ahead`, or `try again` before resuming.

Do not infer approval from thanks, acknowledgements, reactions, or another question. See `guidelines/question-pause-control.md` for the full rule and `examples/question-pause-scenarios.md` for test scenarios.

For an external failure, retry at most once. If it still fails, stop and report the exact blocker and the single action needed.

## Verification

Run the smallest useful verification:

- targeted unit test
- linter for changed file
- type check for changed module
- one focused command that reproduces the issue

## Reporting

Final response should include:

- changed area
- verification result
- remaining risk or next step

Avoid long walkthroughs unless requested.
