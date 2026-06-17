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
