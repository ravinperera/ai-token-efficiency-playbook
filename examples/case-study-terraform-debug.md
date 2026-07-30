# Case Study: Terraform Debugging

This measured example shows how to preserve the exact Terraform failure signal without sending an entire plan, debug trace, and unrelated module files to an AI agent.

## Scenario

A development environment was reduced from two private subnets to one. A module output still selected `aws_subnet.private[1]`, so `terraform plan` failed with `Invalid index`.

## Before

The original request included:

- the full root module;
- all network-module variables, resources, and outputs;
- the complete development variables file;
- 80 unrelated ECS task-definition plan entries;
- 60 successful provider debug lines;
- the error at the end of the output.

Prompt shape:

```text
Diagnose this Terraform plan failure. I pasted the full root module, all network module files, and the complete plan/debug output because I am not sure what is relevant.

<34,658-character context containing full files and debug output>
```

## After

The focused request retained:

- the exact error and source location;
- the relevant `aws_subnet.private` resource;
- the failing output;
- the one-subnet development values;
- the recent configuration change;
- the compatibility constraint for environments with one or more subnets;
- the requested diagnosis, minimal correction, and validation command.

Prompt shape:

```text
Diagnose this Terraform failure. Give the root cause, the smallest safe code correction, and one validation command. Do not redesign the network.

Exact error:
Error: Invalid index
  on modules/network/outputs.tf line 14:
  value = aws_subnet.private[1].id
  aws_subnet.private is tuple with 1 element

Relevant resource and output:
<selected blocks only>

Recent change:
Dev was reduced from two private subnets to one. Production still uses two.

Constraint:
Keep the module valid for environments with one or more private subnets.
```

## Measurement

The repository estimator reports:

| Context | Bytes | Characters | Words | Lines | Estimated tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| Before | 34,694 | 34,658 | 2,577 | 721 | 8,664 |
| After | 955 | 955 | 112 | 31 | 239 |
| Delta | -33,739 | -33,703 | -2,465 | -690 | -8,425 |

The result is specific to this generated fixture. It is not a universal percentage claim.

## Reproduce the fixture

Run this from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
from textwrap import dedent

root = Path('/tmp/token-case-study-terraform')
root.mkdir(parents=True, exist_ok=True)

plan = [
    'Terraform used the selected providers to generate the following execution plan.',
    'Resource actions are indicated with the following symbols:',
    '  + create',
    '  ~ update in-place',
    '',
]
for i in range(1, 81):
    plan.extend([
        f'  # module.service.aws_ecs_task_definition.revision_{i:02d} will be updated in-place',
        f'  ~ resource "aws_ecs_task_definition" "revision_{i:02d}" {{',
        f'        family                   = "example-service-{i:02d}"',
        '      ~ container_definitions    = (sensitive value)',
        '        requires_compatibilities = ["FARGATE"]',
        '    }',
        '',
    ])
for i in range(1, 61):
    plan.append(
        f'2026-07-30T08:{i % 60:02d}:12.000Z [DEBUG] provider.terraform-provider-aws: '
        f'request_id=req-{i:03d} operation=DescribeSubnets status=200 retry=0'
    )
plan.extend([
    '',
    'Error: Invalid index',
    '',
    '  on modules/network/outputs.tf line 14, in output "private_subnet_id":',
    '  14: value = aws_subnet.private[1].id',
    '    ├────────────────',
    '    │ aws_subnet.private is tuple with 1 element',
    '',
    'The given key does not identify an element in this collection value: the given index is greater than or equal to the length of the collection.',
])

before = dedent('''\
Diagnose this Terraform plan failure. I pasted the full root module, all network module files, and the complete plan/debug output because I am not sure what is relevant.

--- main.tf ---
module "network" {
  source = "./modules/network"

  environment          = var.environment
  availability_zones   = var.availability_zones
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
  enable_nat_gateway   = var.enable_nat_gateway
  tags                 = local.common_tags
}

module "service" {
  source = "./modules/service"

  cluster_arn       = aws_ecs_cluster.main.arn
  private_subnet_id = module.network.private_subnet_id
  security_group_id = aws_security_group.service.id
  image             = var.image
  desired_count     = var.desired_count
  tags              = local.common_tags
}

--- modules/network/variables.tf ---
variable "availability_zones" {
  type        = list(string)
  description = "Availability zones used by the VPC"
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "Private subnet CIDR blocks"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "Public subnet CIDR blocks"
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Whether to create a NAT gateway"
}

--- modules/network/subnets.tf ---
resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)

  vpc_id            = aws_vpc.main.id
  availability_zone = var.availability_zones[count.index]
  cidr_block        = var.private_subnet_cidrs[count.index]

  tags = merge(var.tags, {
    Name = "${var.environment}-private-${count.index + 1}"
  })
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  availability_zone       = var.availability_zones[count.index]
  cidr_block              = var.public_subnet_cidrs[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.environment}-public-${count.index + 1}"
  })
}

--- modules/network/outputs.tf ---
output "private_subnet_id" {
  description = "Second private subnet used by the example service"
  value       = aws_subnet.private[1].id
}

--- environments/dev.tfvars ---
environment          = "dev"
availability_zones   = ["eu-west-2a"]
private_subnet_cidrs = ["10.20.1.0/24"]
public_subnet_cidrs  = ["10.20.101.0/24"]
enable_nat_gateway   = false

--- terraform plan -no-color with TF_LOG=DEBUG ---
''') + '\n'.join(plan) + '\n'

after = dedent('''\
Diagnose this Terraform failure. Give the root cause, the smallest safe code correction, and one validation command. Do not redesign the network.

Exact error:
Error: Invalid index
  on modules/network/outputs.tf line 14:
  value = aws_subnet.private[1].id
  aws_subnet.private is tuple with 1 element

Relevant resource:
resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)
  availability_zone = var.availability_zones[count.index]
  cidr_block        = var.private_subnet_cidrs[count.index]
}

Relevant output:
output "private_subnet_id" {
  description = "Second private subnet used by the example service"
  value       = aws_subnet.private[1].id
}

Relevant dev values:
availability_zones   = ["eu-west-2a"]
private_subnet_cidrs = ["10.20.1.0/24"]

Recent change:
Dev was reduced from two private subnets to one. Production still uses two.

Constraint:
Keep the module valid for environments with one or more private subnets.
''')

(root / 'before.txt').write_text(before, encoding='utf-8')
(root / 'after.txt').write_text(after, encoding='utf-8')
PY

python3 scripts/estimate-context-size.py \
  /tmp/token-case-study-terraform/before.txt \
  /tmp/token-case-study-terraform/after.txt \
  --markdown
```

## Correctness safeguard

The focused context should be expanded when the failure depends on additional module contracts, state, provider versions, generated configuration, or environment-specific behaviour. Context reduction is successful only when the diagnosis and verification remain correct.
