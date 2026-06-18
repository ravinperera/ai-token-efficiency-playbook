# Case Study: CI Log Triage

This case study shows how context hygiene reduces token usage without hiding the failure signal.

## Scenario

A GitHub Actions deployment failed while configuring AWS credentials for a Terraform deployment.

The original workflow attached a large CI log and asked the AI to inspect everything. The TokenSaver version provided only the failed step, exact error, relevant recent change, and desired outcome.

## Before

### Prompt Shape

```text
The deploy-prod workflow failed. Here is the full GitHub Actions log from the run. Please review everything and tell me what happened.

<full log pasted: checkout, setup, dependency install, terraform init, terraform validate, terraform plan, configure aws credentials, terraform apply, cleanup>
```

### Context Included

- Full CI log with unrelated successful steps
- Repeated environment variables
- Dependency install output
- Terraform provider installation output
- Cleanup output
- No explicit recent change

### Approximate Input Size

| Item | Approximate tokens |
| --- | ---: |
| User prompt | 25 |
| Full CI log excerpt | 7,800 |
| Total | 7,825 |

## After

### TokenSaver Prompt

```text
Triage this CI failure in TokenSaver mode.

Workflow:
deploy-prod

Failed step:
Configure AWS credentials

Error:
AccessDenied: Not authorized to perform sts:AssumeRoleWithWebIdentity

Relevant recent change:
GitHub repository was renamed from ecs-demo to ecs-platform-demo.

Relevant file:
.github/workflows/deploy.yml

Need:
Likely OIDC trust-policy issue and exact IAM condition to check.
```

### Context Included

- Workflow name
- Failed step
- Exact AWS error
- Relevant recent change
- One relevant file
- Clear output requested

### Approximate Input Size

| Item | Approximate tokens |
| --- | ---: |
| User prompt | 95 |
| Extra context | 0 |
| Total | 95 |

## Result

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Approximate input tokens | 7,825 | 95 | -7,730 |
| Context quality | Low | High | Improved |
| Failure signal | Buried in log | Explicit | Improved |
| Expected first answer | Parse logs | Check OIDC trust condition | More direct |

## Likely Diagnosis From The TokenSaver Prompt

The recent repository rename may have invalidated an IAM OIDC trust policy condition that matches the GitHub `sub` claim.

Check conditions similar to:

```json
"token.actions.githubusercontent.com:sub": "repo:OWNER/REPO:ref:refs/heads/main"
```

If the repository name changed, update the `repo:OWNER/REPO` portion to match the new repository path.

## Measurement Method

The token counts above are approximate, based on comparing the prompt/context text size for the two input shapes. They are intended to be reproducible as a method, not as a universal benchmark.

For a real project, measure using your AI tool's token dashboard or a tokenizer for the model you are using. Always record:

- tool and model
- before prompt/context
- after prompt/context
- whether the answer remained correct
- any extra follow-up prompts required

## Caveat

Savings vary by task. Do not remove context that changes correctness, such as exact errors, relevant files, commands, assumptions, security constraints, or verification results.
