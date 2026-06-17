# Context Hygiene

Context hygiene is the practice of keeping AI inputs small, relevant, and current.

## Good Context

Good context is:

- relevant
- current
- specific
- structured
- short enough to reason over

## Bad Context

Bad context includes:

- full logs when only one error matters
- entire repos when one module matters
- repeated requirements
- stale project notes
- screenshots without explaining the target question
- multiple unrelated issues in one prompt

## Practical Rules

- Start a new chat for a new problem domain.
- Compact long conversations before switching topics.
- Provide file paths and exact errors.
- Remove duplicate logs.
- Replace long logs with summaries.
- Keep project memory under active maintenance.

## Before Sending A Prompt

Ask:

- What do I actually need the AI to decide?
- Which files or outputs are relevant?
- Can I remove repeated context?
- Can I provide an exact error instead of a full log?
- Is this a simple task that needs a cheaper model?
