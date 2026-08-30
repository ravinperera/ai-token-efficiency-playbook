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

## External source provenance

Complete this section when the change is materially inspired by another repository, paper, standard, benchmark, or tool.

- Source and canonical URL:
- Revision, release, standard version, or review date:
- Licence:
- Reusable concept adopted:
- Source-specific details intentionally not copied:
- Claim-validation status:

See `docs/external-pattern-intake.md`. Prefer one canonical local rule and link to it rather than duplicating source material.

## Safety checklist

- [ ] The pull request is focused and contains no unrelated changes.
- [ ] No secrets, credentials, private URLs, customer data, sensitive logs, or confidential prompts are included.
- [ ] Provider, tenancy, region, retention policy, approved model family, and data boundaries are unchanged, or the change is explicitly documented and approved.
- [ ] Lower-cost model guidance does not weaken security, correctness, or required verification.
- [ ] Exact errors, relevant evidence, assumptions, and validation results are preserved where correctness depends on them.
- [ ] New guidance is concise and does not duplicate canonical rules unnecessarily.
- [ ] Reused external material has compatible licence/attribution handling, and quantitative claims are independently measured or clearly qualified.
- [ ] `bash scripts/check-token-hygiene.sh` and relevant tests passed, or the reason they were not applicable is documented above.

Closes #
