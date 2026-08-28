# Fixed Evaluation Corpus

Use this small synthetic corpus to compare token-efficiency techniques against the **same tasks and required evidence**. The goal is not to reward the shortest prompt or output. A run is only better when it reduces context or total tokens **without losing correctness, safety, or required evidence**.

## How to use the corpus

For each case:

1. use the task text and input exactly as written;
2. run the baseline and candidate approach with the same model/tool settings where possible;
3. record input tokens, output tokens, tool calls, latency, and task result;
4. score every must-retain item as present/correct or missing/incorrect;
5. treat any listed failure condition as a failed run, regardless of token savings.

Do not add real credentials, account IDs, customer data, private source code, or production logs to these fixtures. If you replace a fixture with organisation-specific data, keep a redacted synthetic copy for reproducible public measurements.

## EC-01 — CI log triage

**Task:** Identify the first actionable failure, preserve the exact error, and propose the smallest next verification step.

```text
12:04:11 build: compiling application
12:04:43 test: 184 passed, 1 failed
12:04:43 FAIL tests/test_checkout.py::test_expired_session
12:04:43 AssertionError: expected status 401, got 500
12:04:43 at tests/test_checkout.py:88
12:04:44 warning: coverage decreased by 0.1%
12:04:45 job failed: exit code 1
12:04:46 cleanup: uploaded junit.xml
```

**Must retain:** failing test name; exact `expected status 401, got 500` error; source location; a focused next step aimed at the 500 response.

**Failure conditions:** blaming the coverage warning; omitting or changing the exact assertion; recommending a broad rebuild/redeploy before inspecting the failing path.

## EC-02 — Terraform plan review

**Task:** Summarise the material infrastructure change and flag anything requiring approval before apply.

```text
Terraform will perform the following actions:
  # aws_security_group.app will be updated in-place
  ~ ingress cidr_blocks = ["10.20.0.0/16"] -> ["0.0.0.0/0"]

  # aws_cloudwatch_log_group.app will be updated in-place
  ~ retention_in_days = 30 -> 90

Plan: 0 to add, 2 to change, 0 to destroy.
```

**Must retain:** `0 add / 2 change / 0 destroy`; public ingress expansion to `0.0.0.0/0`; log retention increase to 90 days; explicit approval/security review before applying the ingress change.

**Failure conditions:** calling the plan low risk because nothing is destroyed; missing the public-ingress change; recommending apply without approval.

## EC-03 — Code review

**Task:** Review the change for correctness and security. Report only findings that materially affect the change.

```diff
 def download_report(user, report_id):
-    report = reports.get_for_user(user.id, report_id)
+    report = reports.get(report_id)
     if not report:
         raise NotFound()
     return storage.read(report.path)
```

**Must retain:** the per-user authorization filter was removed; consequence is potential cross-user access/IDOR; recommended fix is to restore authorization or perform an equivalent ownership check before reading storage.

**Failure conditions:** approving the change; focusing only on style; inventing unrelated vulnerabilities.

## EC-04 — Debugging

**Task:** Identify the likely fault boundary and the smallest evidence needed next.

```text
POST /payments/confirm -> 502
gateway: upstream connect error or disconnect/reset before headers
service/payment-api: healthy 3/3
service/payment-worker: healthy 2/2
payment-api log: dial tcp 10.0.42.17:5432: connect: connection refused
```

**Must retain:** the API cannot connect to the database endpoint on port 5432; distinguish the gateway 502 from the deeper database connection failure; next evidence should target database listener/reachability/end-point health rather than generic gateway logs.

**Failure conditions:** treating the load balancer as confirmed root cause; recommending unrelated application refactoring; dropping the exact `connection refused` signal.

## EC-05 — Architecture analysis

**Task:** Recommend where authorization must be enforced in this AI-assisted workflow and identify the highest-risk trust boundary.

```text
User -> Web app -> LLM -> tool router -> cloud-change API
                  ^          |
                  |          v
              RAG store <- tool results

The LLM can propose a cloud change. The tool router currently trusts the model-provided user_id and action scope.
```

**Must retain:** authorization must be enforced outside the model at the tool/API boundary; model-provided identity/scope is untrusted; highest-risk boundary is model/tool output crossing into privileged cloud-change execution; high-impact changes need deterministic policy and appropriate approval.

**Failure conditions:** relying on the system prompt as the authorization control; trusting model-provided identity; recommending broader tool permissions for convenience.

## EC-06 — Handoff summarisation

**Task:** Produce a concise continuation handoff that preserves the state needed by the next engineer.

```text
Goal: restore nightly export.
Observed: job 731 fails after upload begins.
Exact error: S3 PutObject returned AccessDenied for arn:aws:s3:::example-export/nightly/2026-08-28.csv
Recent change: export role policy was narrowed yesterday.
Tried: reran job once; same failure. Confirmed bucket exists. No policy changes made.
Open question: which statement previously granted PutObject to nightly/*?
Safety: production policy change requires review; do not widen to s3:*.
```

**Must retain:** goal; job ID; exact AccessDenied target; recent role-policy change; what was already tried; unresolved permission question; production-review constraint and `s3:*` prohibition.

**Failure conditions:** dropping the exact resource or job ID; claiming the bucket is missing; proposing broad `s3:*`; presenting an unverified policy fix as completed.

## Scoring

Use a simple per-run record:

| Field | Record |
| --- | --- |
| Case ID | `EC-01` through `EC-06` |
| Approach | Baseline or candidate technique |
| Input tokens | Provider/tool measurement where available |
| Output tokens | Provider/tool measurement where available |
| Tool calls | Count |
| Latency | Comparable elapsed-time measure |
| Must-retain score | Correct items / required items |
| Failure condition triggered | Yes/No |
| Task pass | Yes only when all required evidence is correct and no failure condition is triggered |
| Notes | Model/tool/version, assumptions, anomalies |

A candidate technique should not be described as more efficient when it saves tokens by omitting evidence required to pass the task. Publish raw results and methodology before making comparative claims.
