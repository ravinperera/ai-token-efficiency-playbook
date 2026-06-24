# Case Study: Terraform Debug

This case study shows how to debug Terraform failures without pasting an entire plan, provider install log, or CI transcript.

## Scenario

A Terraform apply failed while creating an ECS service because the task definition and target group configuration did not match the service settings.

The original request pasted the complete CI log, full `terraform plan`, and unrelated module output. The TokenSaver version included only the failing resource, exact error, relevant module files, and recent change.

## Before

### Prompt Shape

```text
Terraform apply failed in GitHub Actions. Here is the full log and plan. Please check everything and fix it.

<full CI log>
<terraform init output>
<complete terraform plan>
<provider download output>
<full module tree pasted>
```

### Context Included

- Successful setup and provider download logs
- Complete plan for unrelated resources
- Full module tree instead of relevant files
- No statement of the recent change
- No exact target resource called out

### Approximate Input Size

| Item | Approximate tokens |
| --- | ---: |
| User prompt | 30 |
| CI and Terraform output | 12,400 |
| Pasted module files | 4,100 |
| Total | 16,530 |

## After

### TokenSaver Prompt

```text
Debug this Terraform ECS failure in TokenSaver mode.

Command:
terraform apply

Failed resource:
aws_ecs_service.tra_backend

Error:
InvalidParameterException: The target group with targetGroupArn ... does not have an associated load balancer.

Recent change:
Split ECS task and service into separate Terraform components.

Relevant files:
- infrastructure/components/terraform/aws/tra-backend-service/main.tf
- infrastructure/stacks/tra_backend/dev/default/eu-west-2.yaml

Need:
Likely root cause and the smallest Terraform change to fix it.
```

### Context Included

- Exact command
- Failed resource
- Exact provider error
- Recent architectural change
- Two relevant files only
- Clear output requested

### Approximate Input Size

| Item | Approximate tokens |
| --- | ---: |
| User prompt | 125 |
| Relevant file snippets | 1,300 |
| Total | 1,425 |

## Result

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Approximate input tokens | 16,530 | 1,425 | -15,105 |
| Relevant signal | Low | High | Improved |
| Expected first answer | Parse all Terraform output | Check ALB target group dependency/wiring | More direct |

## Measurement Method

Counts are approximate and based on the included prompt/context text. Reproduce the method by saving the before and after prompt bodies and running a token counter such as `scripts/count-tokens.py`.

Do not treat this as a fixed saving percentage. The point is to preserve correctness while removing low-value output.

## Caveat

Keep exact provider errors, resource names, module names, and relevant variables. Removing those can make the answer faster but wrong.
