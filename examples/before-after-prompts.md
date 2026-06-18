# Before And After Prompts

Copy these examples when you want the AI to solve the same task with less context and less output.

## Terraform Debugging

### Before

```text
My app is broken. Here are all the logs from the deployment and the whole config. Can you check everything and tell me what is wrong?
```

### After

```text
Debug in TokenSaver mode.
Command: terraform plan
Error: Unsupported attribute in ecs-service/main.tf:42
Relevant change: ALB target group output was renamed yesterday.
Relevant files: modules/ecs-service/main.tf, modules/alb/outputs.tf
Find likely cause and smallest fix.
```

## Pytest Failure

### Before

```text
Here is the whole test output and all files in the API folder. Why are tests failing?
```

### After

```text
Debug in TokenSaver mode.
Command: pytest tests/test_auth.py::test_expired_token -q
Error: AssertionError: expected 401, got 200
Recent change: auth middleware now skips OPTIONS requests.
Relevant files: app/auth.py, tests/test_auth.py
Find the likely regression and smallest test/code fix.
```

## CI Log Triage

### Before

```text
The build failed. I pasted the full GitHub Actions log below. Please review everything and tell me what happened.
```

### After

```text
Triage this CI failure in TokenSaver mode.
Workflow: deploy-prod
Failed step: terraform apply
Error: AccessDenied: sts:AssumeRoleWithWebIdentity
Relevant change: GitHub OIDC role trust policy edited today.
Need: likely IAM trust policy issue and exact field to check.
```

## Refactor Request

### Before

```text
Please refactor this repository to make it cleaner and explain all improvements you would make.
```

### After

```text
Refactor in TokenSaver mode.
Scope: only duplicate validation logic in src/validators/*.ts
Goal: reduce duplication without changing public API.
Do not reformat unrelated files.
Verify with: npm test -- validators
Return changed files and residual risk only.
```

## Code Review

### Before

```text
Please review this PR and give me a detailed explanation of everything that changed and whether it looks good.
```

### After

```text
Review in TokenSaver mode.
Focus only on bugs, security issues, regressions, and missing tests.
Findings first, with file/path references.
No praise summary. No walkthrough of unchanged code.
```

## Architecture

### Before

```text
Tell me everything about how I should design this system using AWS.
```

### After

```text
Architecture mode.
Recommend one AWS design for ECS service deployment across dev/staging/prod.
Include key trade-offs, risks, and next implementation step.
Keep concise and avoid service-by-service AWS overview.
```
