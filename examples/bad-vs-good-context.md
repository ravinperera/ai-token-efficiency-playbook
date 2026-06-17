# Bad Vs Good Context

## Bad Context

```text
Here is my whole repository structure, all Terraform files, all workflow logs, and previous conversation. Please figure out why deployment failed.
```

Why bad:

- too broad
- too much irrelevant data
- unclear failure signal
- forces the model to spend tokens filtering noise

## Good Context

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
