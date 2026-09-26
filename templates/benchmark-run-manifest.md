# Benchmark Run Manifest

Use this manifest alongside a benchmark result so another person can understand what was measured and reproduce the run as closely as practical.

Keep sensitive inputs out of the manifest. Refer to approved evidence by stable identifier, path, digest, or redacted fixture rather than copying secrets, customer data, private source, or full prompts.

## Run identity

- Run ID:
- Benchmark/case ID:
- Date/time:
- Trial number:
- Baseline or candidate approach:
- Operator/automation identifier, if useful:

## Task and source provenance

- Task/acceptance criteria revision:
- Repository/input source:
- Repository commit/tag or fixture digest:
- Changed files or fixture version:
- Required evidence/must-retain items:
- Verification method:

Pin source revisions whenever the task depends on mutable code, documents, indexes, or datasets.

## Model and client

- Provider:
- Model or capability tier:
- Model/version identifier reported by the provider, if available:
- Agent/client/tool:
- Agent/client/tool version:
- Reasoning/temperature/other material settings:
- Region/tenancy/data boundary relevant to the run:

Do not infer an exact backend model version when the provider does not expose one. Record `unknown` rather than guessing.

## Instructions, tools, and skills

- System/project instruction revision or digest:
- Prompt/template revision:
- Enabled tools/connectors and versions:
- Loaded skills/procedures and versions:
- Skill/tool manifest revisions:
- Material permissions/approval gates:

This section helps distinguish a model change from an instruction, tool, or skill change.

## Cache, memory, and retrieval state

- Session state: `fresh | continued | other`
- Prompt/cache state: `cold | warm | mixed | unknown`
- Persistent memory/index state:
- Memory/index revision and freshness:
- Preloaded context/resources:
- Retrieval fallback policy:

A warm-cache result should not be presented as a cold-start cost unless both conditions were measured.

## Environment

- Machine/runtime class:
- Operating system/runtime version where material:
- Network condition or remote-service dependency:
- Local/hosted execution:
- Concurrency or rate-limit conditions:
- Random seed, when supported and material:

Record only environment details that could plausibly affect latency, reproducibility, or outcome.

## Measurement and cost basis

- Telemetry source:
- Input tokens:
- Cached input/cache writes, if reported:
- Output tokens:
- Tool/retrieval calls:
- Attempts/retries/escalations:
- Elapsed time:
- Cost view: `billed | API-equivalent | allocated subscription | none`
- Pricing source/effective date:
- Currency:
- Estimated fields and assumptions:

Keep measured values separate from estimates. Do not present API-equivalent cost as actual cash spend on a fixed subscription.

## Outcome

- Task result: `pass | fail | partial`
- Verification result:
- Required evidence preserved: `yes | no | partial`
- Failure condition triggered: `yes | no`
- Safety/data-boundary exception: `yes | no`
- Notes/anomalies:

## Reproducibility status

- Raw/redacted fixture available: `yes | no`
- Manifest sufficient to repeat the run: `yes | no | partial`
- Known non-reproducible factors:
- Reviewer/check date:

## Interpretation

Compare complete workflows at equivalent task quality. A lower token count is not an improvement when correctness, safety, required evidence, verification, retries, or latency materially worsens. Publish the run manifest with comparative claims so model, tool, cache, pricing, and source-version differences remain visible.
