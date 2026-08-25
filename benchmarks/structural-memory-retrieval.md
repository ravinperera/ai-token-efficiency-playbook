# Structural Memory Retrieval Benchmark

Use this protocol to compare codebase exploration strategies without assuming that a persistent index, graph, or context governor is automatically more efficient.

The goal is to answer the same repository-navigation question with comparable correctness and safety while measuring the complete workflow cost.

## Comparison Modes

Run at least these three modes against the same repository revision and task:

1. **Cold file-by-file exploration** — ordinary filename/text search followed by source-file reads without a prebuilt structural index.
2. **Search plus targeted ranges** — search first, then load only relevant symbols, ranges, diffs, or nearby source sections.
3. **Persistent structural retrieval** — query a prebuilt symbol index, AST outline, code graph, or equivalent structural memory before reading authoritative source where required.

A fourth mode may be added for a governed retrieval layer that automatically returns outlines, range-limited content, or refusals for oversized/noisy files.

## Choose A Reproducible Task

Use a task whose answer can be objectively checked, for example:

- identify every caller of a selected function and the files that must change for a signature update;
- trace an HTTP route from entry point to handler and persistence layer;
- identify the configuration path controlling a named runtime behaviour;
- locate the implementation and tests for a specific feature;
- determine the blast radius of changing a named class, resource, or interface.

Avoid tasks whose expected answer changes between runs. Pin the repository commit or tag.

## Keep The Runs Comparable

For each mode, keep these constant where possible:

- repository and revision;
- task wording and acceptance criteria;
- model/provider and settings;
- tool permissions and data boundary;
- machine class and network conditions;
- success criteria and verification method.

Record unavoidable differences instead of hiding them.

## Cold And Warm Runs

Persistent indexes introduce an up-front cost that ordinary reads may not have. Measure it separately.

Run:

```text
cold index: build/refresh required before the task
warm index: valid index already exists for the pinned revision
```

Do not present a warm-query result as the total cost of first use. Likewise, do not charge every later query the full historical indexing cost unless that reflects the real deployment model.

## Required Measurements

Capture at least:

- input/context tokens across all model turns;
- output tokens;
- bytes of source/tool content returned to the model where measurable;
- number of model turns;
- number of retrieval/tool calls;
- index build or refresh duration;
- query/retrieval latency;
- total elapsed time;
- task success;
- verification result;
- stale or incomplete-index failures;
- fallback source reads;
- incorrect file/symbol selections;
- estimated or measured cost where available.

If a tool reports "bytes avoided" or similar receipts, record them as tool telemetry, not as a substitute for measured total tokens.

## Freshness Test

A persistent index can be fast but wrong if it represents an old revision. Include at least one freshness scenario:

1. build the index at revision A;
2. make or select a relevant change at revision B;
3. run the structural query before refresh;
4. observe whether the tool detects staleness, refreshes, warns, or returns an incorrect/incomplete answer;
5. refresh and repeat.

Record the stale-state outcome explicitly. A workflow that saves tokens but silently reasons over old code is not an efficiency improvement.

## Correctness Scoring

Define the expected answer before comparing modes. A simple score can include:

```text
required files/symbols found
irrelevant files/symbols selected
call/dependency relationships correct
required tests/config identified
final answer passes independent verification
```

Do not compare token totals for runs that achieved materially different task quality without calling out the difference.

## Safety And Boundary Checks

Record whether each mode:

- stayed inside the intended repository/project;
- respected excluded paths and data classifications;
- attempted to read secrets, binaries, lockfiles, or generated artifacts unnecessarily;
- relied on stale cached state for a material conclusion;
- expanded context beyond what the task required.

A retrieval layer may be worth using even when total tokens are similar if it materially improves safety or boundary enforcement. Record that as a trade-off, not a token saving.

## Suggested Run Sequence

For each mode:

```text
1. reset the conversation/session to the same starting instructions
2. pin the repository revision
3. execute the same task
4. capture every model/tool interaction metric available
5. verify the answer independently
6. record failures and fallbacks
7. repeat enough times to expose variance
```

Where non-determinism is material, use multiple runs per mode and report median plus range rather than one best run.

## Interpreting Results

Compare complete workflow totals.

Good evidence looks like:

```text
Mode C used fewer total input tokens than Modes A and B at the same task-success level, including the measured warm-query overhead. Cold indexing cost is reported separately, and stale-index tests passed because the runtime detected revision mismatch.
```

Weak evidence looks like:

```text
The graph query returned 120 tokens, therefore the system saves 99%.
```

The second statement ignores indexing, tool envelopes, model turns, fallback reads, correctness, and workload differences.

## Reusable Data Template

Record individual runs in [`../templates/structural-memory-retrieval-measurement.csv`](../templates/structural-memory-retrieval-measurement.csv).

Do not publish a generalized saving percentage until comparable runs across representative tasks and repositories support it. Tool-vendor benchmark claims may be useful hypotheses, but this playbook treats them as unverified until independently reproduced.
