# Bad Vs Good Context

Use these examples to replace broad, expensive prompts with small context packets that preserve the failure signal.

## Example 1: Terraform Deployment Failure

### Bad Context

```text
Here is my whole repository structure, all Terraform files, all workflow logs, and previous conversation. Please figure out why deployment failed.
```

Why bad:

- too broad
- too much irrelevant data
- unclear failure signal
- forces the model to spend tokens filtering noise

### Good Context

```text
Deployment failed after splitting ECS task and service components.

Command:
atmos terraform plan aws/tra-backend-service -s dev/eu-west-2

Error:
Unsupported attribute: module.alb.target_group_arn is not exposed.

Relevant files:
- infrastructure/components/terraform/aws/tra-backend-service/main.tf
- infrastructure/components/terraform/aws/alb/outputs.tf

Need:
Smallest Terraform fix.
```

Why good:

- clear change
- exact command
- exact error
- relevant files only
- clear requested outcome

## Example 2: Full Log Vs Compressed Log

### Bad Context

```text
Here are 4,000 lines from GitHub Actions. Please check what failed.
```

### Good Context

```text
CI failure triage.

Workflow:
.github/workflows/deploy.yml

Failed step:
Configure AWS credentials

Error:
AccessDenied: Not authorized to perform sts:AssumeRoleWithWebIdentity

Relevant recent change:
Renamed GitHub repo from ecs-demo to ecs-platform-demo.

Need:
Check likely OIDC trust-policy mismatch.
```

Why good:

- keeps the exact failing API call
- includes the changed condition that likely caused the break
- avoids making the model parse unrelated build logs

## Example 3: Whole Repo Vs Targeted Files

### Bad Context

```text
I uploaded the whole backend repo. Please improve auth and fix the failing tests.
```

### Good Context

```text
Task:
Fix failing expired-token test only.

Command:
pytest tests/test_auth.py::test_expired_token -q

Error:
AssertionError: expected 401, got 200

Relevant files:
- app/auth.py
- app/middleware.py
- tests/test_auth.py

Constraints:
Do not change token format or public API.
```

Why good:

- isolates one failing behavior
- limits file reads
- states constraints that protect correctness

## Example 4: Screenshot-Only Vs Decision Context

### Bad Context

```text
Here is a screenshot. What should I do?
```

### Good Context

```text
Question:
Should I cancel these pending GitHub org invitations?

Screenshot shows:
- GitHub org People > Pending invitations
- 15 invitations
- created by SCIM

Need:
Explain why they appeared and safest next action.
```

Why good:

- explains what decision is needed
- extracts important facts from the screenshot
- avoids forcing the model to infer the goal
