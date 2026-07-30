## Summary

Describe the problem and the smallest useful change that resolves it.

## Why this helps

Explain the expected benefit for context hygiene, model routing, verification, contributor experience, or repository quality.

## Scope

- Included:
- Intentionally excluded:

## Validation

List the exact checks, tests, commands, or manual review performed.

```text
commands and results
```

## Token-efficiency evidence

Complete this section when the change claims context or token reduction.

- Before input shape:
- After input shape:
- Measurement method:
- Result and caveats:

Do not claim a universal or fixed saving percentage from a single example.

## Safety checklist

- [ ] The pull request is focused and contains no unrelated changes.
- [ ] No secrets, credentials, private URLs, customer data, sensitive logs, or confidential prompts are included.
- [ ] Provider, tenancy, region, retention policy, approved model family, and data boundaries are unchanged, or the change is explicitly documented and approved.
- [ ] Lower-cost model guidance does not weaken security, correctness, or required verification.
- [ ] Exact errors, relevant evidence, assumptions, and validation results are preserved where correctness depends on them.
- [ ] New guidance is concise and does not duplicate canonical rules unnecessarily.
- [ ] `bash scripts/check-token-hygiene.sh` and relevant tests passed, or the reason they were not applicable is documented above.

Closes #
