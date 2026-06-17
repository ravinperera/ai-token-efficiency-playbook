# Model Routing

Do not use the strongest model for every task. Match the model to the job.

## Use Cheaper/Faster Models For

- formatting
- summarisation
- simple Q&A
- rewriting messages
- extracting lists
- basic code snippets
- log summarisation
- documentation cleanup

## Use Stronger Models For

- architecture decisions
- security review
- complex debugging
- multi-file refactors
- infrastructure design
- ambiguous requirements
- production incident analysis

## Routing Pattern

```text
Classify task -> choose model -> limit context -> run -> verify
```

## Practical Rule

If a task does not require deep reasoning, do not pay for deep reasoning.

## Safety Note

Do not route sensitive data to models or providers that are not approved for that data classification.
