# Before And After Prompts

## Debugging

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
Find likely cause and smallest fix.
```

## Code Review

### Before

```text
Please review this PR and give me a detailed explanation of everything that changed and whether it looks good.
```

### After

```text
Review in TokenSaver mode. Focus only on bugs, security issues, regressions, and missing tests. Findings first. No praise summary.
```

## Architecture

### Before

```text
Tell me everything about how I should design this system using AWS.
```

### After

```text
Architecture mode. Recommend one AWS design for ECS service deployment across dev/staging/prod. Include trade-offs, risks, and next implementation step. Keep concise.
```
