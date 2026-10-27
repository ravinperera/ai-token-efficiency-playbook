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

## Index Lifecycle And Workload Break-Even

A fast warm query does not establish that a persistent index pays for itself. For a reuse claim, **freeze a complete workload** before measuring: task IDs and acceptance criteria, the ordered sequence of repository revisions, expected index invalidations, the number of queries, and an observation cutoff. Run the same tasks against search/range retrieval without carrying answers or agent state between modes.

Track the index lifecycle separately from query performance:

- Record initial build, incremental refresh, forced rebuild, failed build, and stale-index detection events, including the source revision, event identifier, time, and any known model/tool cost. Count each event once even when several tasks share it.
- For each task, record cold/warm index state, query time, fallback source reads, verification, retries, and the outcome. Keep failed, cancelled, and pending tasks in the declared workload instead of reporting only successful warm queries.
- Run a revision-change scenario that invalidates a relevant relationship and observe whether the index refreshes or safely falls back. A cheaper but incorrect stale-index answer is not a passing result.
- Distinguish first-use, steady-state, and mixed-change workloads. Report observed event frequency; do not assume one build remains valid forever or that every query incurs a full rebuild.

Compare **complete workload totals** at equivalent task correctness and safety:

```text
indexed total = build + refresh/rebuild + queries + fallback reads + verification + retries
search total  = discovery/search + source reads + verification + retries
```

Use the same unit for each term (such as elapsed seconds or a consistently priced cost view). Do not add token counts to elapsed time, double-count cached input, or describe measured query-only tokens as end-to-end cost. For a simplified fixed-cost model with positive per-task savings, the illustrative break-even task count is `(build + refresh cost) / (search cost per task - indexed query cost per task)`. If per-task savings are zero or negative, that expression has no positive break-even; if refresh frequency rises with task count, use the observed workload totals instead.

**Fictional arithmetic only, not measured results:** a 20-minute build, one 4-minute refresh, and four tasks taking 8 minutes each with search versus 3 minutes each with indexed queries yield 32 minutes for search and 36 for indexed retrieval. For eight tasks under the *same single-refresh assumption*, totals become 64 versus 48 minutes. Neither result is generalizable without matched quality, revision, caching, and real telemetry.

Use one row per task in the existing [structural retrieval measurement CSV](../templates/structural-memory-retrieval-measurement.csv). Record build/refresh time on the run that incurred it (zero only for a measured zero; otherwise `unknown`) and use `notes` plus a linked [benchmark run manifest](../templates/benchmark-run-manifest.md) to identify any shared, pre-task setup event. Keep unallocated setup cost visible in the workload total rather than inventing per-task usage; disclose incomplete cost coverage. Report cold-query, warm-query, and full-workload findings separately.

## Relationship Provenance Test

When a structural system mixes deterministic parsing with semantic/model-derived relationships, test provenance quality separately from graph-query speed.

Classify material relationships as:

- **extracted** — directly derived from authoritative source or deterministic parsing with a resolvable source anchor;
- **inferred** — proposed by a model or heuristic and supported by source anchors plus confidence/uncertainty metadata where available;
- **ambiguous** — conflicting or insufficient evidence that requires source retrieval or review.

Include at least one task where an inferred or ambiguous relationship could change the answer. Record whether the system:

1. exposes the provenance class rather than flattening all relationships into one certainty level;
2. provides a usable source anchor for material relationships;
3. avoids presenting an inferred relationship as an authoritative source fact;
4. escalates ambiguous or unsupported relationships to source retrieval/review;
5. preserves the distinction after caching, refresh, export, or graph reconstruction.

A high confidence score does not convert an inference into extracted evidence.

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
- material relationships by provenance class where graph results matter;
- unsupported inferred relationships;
- ambiguous relationships escalated for review;
- missing or broken source anchors;
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
relationship provenance labels correct where applicable
material source anchors resolve correctly
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
- treated inferred or ambiguous relationships as facts without verification;
- expanded context beyond what the task required.

A retrieval layer may be worth using even when total tokens are similar if it materially improves safety, provenance, or boundary enforcement. Record that as a trade-off, not a token saving.

## Suggested Run Sequence

For each mode:

```text
1. reset the conversation/session to the same starting instructions
2. pin the repository revision
3. execute the same task
4. capture every model/tool interaction metric available
5. verify relationship provenance/source anchors when graph results matter
6. verify the answer independently
7. record failures and fallbacks
8. repeat enough times to expose variance
```

Where non-determinism is material, use multiple runs per mode and report median plus range rather than one best run.

## Interpreting Results

Compare complete workflow totals.

Good evidence looks like:

```text
Mode C used fewer total input tokens than Modes A and B at the same task-success level, including the measured warm-query overhead. Cold indexing cost is reported separately, stale-index tests passed because the runtime detected revision mismatch, and material inferred relationships were source-verified before use.
```

Weak evidence looks like:

```text
The graph query returned 120 tokens, therefore the system saves 99%.
```

The second statement ignores indexing, tool envelopes, model turns, fallback reads, correctness, provenance quality, and workload differences.

## Reusable Data Template

Record individual runs in [`../templates/structural-memory-retrieval-measurement.csv`](../templates/structural-memory-retrieval-measurement.csv).

Do not publish a generalized saving percentage until comparable runs across representative tasks and repositories support it. Tool-vendor benchmark claims may be useful hypotheses, but this playbook treats them as unverified until independently reproduced.

## Pattern Reference

The explicit distinction between extracted, inferred, and ambiguous relationships was informed by [rhanka/graphify](https://github.com/rhanka/graphify), reviewed 2026-09-23. Graphify is MIT-licensed and combines deterministic structural parsing with semantic extraction that retains relationship provenance. This benchmark adopts the vendor-neutral verification principle only; it does not copy Graphify's implementation or treat its published token estimates as local evidence.
