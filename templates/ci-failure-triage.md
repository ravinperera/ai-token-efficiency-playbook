# CI Failure Triage Template

Use this template when asking an AI assistant to debug a failed CI/CD workflow without pasting the full raw log.

```text
Triage this CI failure in TokenSaver mode.

Goal:
<what the workflow was trying to do>

Workflow:
<workflow name>

Failed job:
<job name>

Failed step:
<step name>

Exact error:
<paste the smallest exact error message or stack trace excerpt>

Relevant recent change:
<PR, commit, dependency, environment, secret, IAM, Terraform, Docker, or config change that may be related>

Relevant files:
- <path/to/workflow.yml>
- <path/to/config-or-code>

What I already checked:
- <command or check and result>
- <command or check and result>

Need:
<the specific output you want: likely root cause, exact file to inspect, patch suggestion, rollback advice, or next verification step>
```

## What to include

Include the smallest context that preserves correctness:

- exact error text
- failed workflow, job, and step names
- relevant changed files
- recent dependency, secret, permission, branch, image, or environment changes
- commands already tried and their results
- the output format you need

## What to avoid

Avoid sending:

- full successful setup logs
- full dependency install output
- repeated environment variables
- complete Terraform plans unless the diff is the failure signal
- secrets, tokens, customer data, tenant IDs, or internal hostnames
- screenshots when plain text is available

If the first answer is not enough, add the next smallest useful log excerpt instead of pasting the full run.
