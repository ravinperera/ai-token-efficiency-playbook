# Document Conversion Context Measurement

Use this protocol to compare whole-document, converted-Markdown, and selected-context workflows without making unsupported token-saving claims.

## Research question

Does converting a text-heavy document to Markdown and selecting only the relevant sections reduce AI input context while preserving task accuracy?

## Comparison arms

Run the same task with the same model, AI tool, source document, instructions, and evaluation criteria.

### Arm A: Original document

Provide the complete original PDF, slide deck, spreadsheet, or image set.

### Arm B: Complete converted Markdown

Convert the source to Markdown and provide the complete converted output.

### Arm C: Selected Markdown

Search the converted output and provide only the smallest relevant sections.

### Arm D: Selected Markdown plus required visual

Provide the selected Markdown and only the source page, chart, or image needed for visual reasoning.

Not every experiment needs all four arms. Record why an arm was omitted.

## Control variables

Keep these constant:

- task prompt and acceptance criteria;
- model and model version;
- AI client or agent;
- source-document version;
- conversation state;
- system and repository instructions;
- available tools;
- temperature or sampling settings where configurable;
- validation method;
- number of runs per arm.

Use fresh sessions where possible to prevent hidden conversation history from affecting results.

## Source record

| Field | Value |
| --- | --- |
| Source identifier | TODO |
| File type | TODO |
| File size | TODO |
| Pages/slides/sheets/images | TODO |
| Data classification | Public / Internal / Confidential / Restricted |
| Conversion tool and version | TODO |
| Conversion mode | Local / approved cloud service |
| OCR used | Yes / No |
| Visual reasoning required | Yes / No |
| Relevant source locations | TODO |

Do not commit confidential source data or sensitive evidence to a public repository.

## Run record

Create one row per run.

| Field | Arm A | Arm B | Arm C | Arm D |
| --- | ---: | ---: | ---: | ---: |
| Input tokens | TODO | TODO | TODO | TODO |
| Output tokens | TODO | TODO | TODO | TODO |
| Total tokens | TODO | TODO | TODO | TODO |
| Estimated cost | TODO | TODO | TODO | TODO |
| Elapsed time | TODO | TODO | TODO | TODO |
| Conversion time | N/A | TODO | TODO | TODO |
| Human selection/review time | N/A | TODO | TODO | TODO |
| Task success | TODO | TODO | TODO | TODO |
| Factual accuracy score | TODO | TODO | TODO | TODO |
| Source references correct | TODO | TODO | TODO | TODO |
| Important visual detail retained | TODO | TODO | TODO | TODO |
| Follow-up prompts required | TODO | TODO | TODO | TODO |

## Suggested task-success rubric

Score each run from 0 to 4:

- **0 — Failed:** did not answer the requested task.
- **1 — Major gaps:** substantial findings missing or incorrect.
- **2 — Partially useful:** core answer present but important errors or omissions remain.
- **3 — Correct:** task completed with only minor issues.
- **4 — Correct and verifiable:** task completed accurately with source references and appropriate uncertainty.

## Conversion-quality checks

Record whether conversion preserved:

- headings and section order;
- lists and action items;
- table rows and columns;
- code or configuration blocks;
- links and references;
- page or slide boundaries;
- captions;
- important numbers and identifiers.

Record any:

- OCR errors;
- missing text;
- duplicated text;
- reordered content;
- lost table relationships;
- missing visuals;
- malformed characters;
- prompt-like instructions embedded in the document.

## Calculations

For comparable successful runs:

```text
input reduction = baseline input tokens - comparison input tokens
input reduction rate = input reduction / baseline input tokens
```

Also report the conversion and human-selection effort. A workflow that saves model tokens but requires excessive manual preparation may not improve the total engineering workflow.

Do not average failed runs away. Report failures and safety problems separately.

## Interpretation

A converted workflow is useful only when it:

- preserves the information needed for the task;
- does not introduce material conversion errors;
- maintains or improves task success;
- keeps visual evidence when visual reasoning is needed;
- handles sensitive data appropriately;
- reduces context or improves searchability enough to justify preparation effort.

## Confounders

Document these limitations:

- models may process images and text using different accounting methods;
- some AI tools do not expose exact multimodal token counts;
- OCR quality differs by language, scan quality, and layout;
- hidden system context and caching may vary;
- conversion tools can change between versions;
- selected Markdown may accidentally omit important surrounding context;
- conversion time and human review time are part of the total cost;
- repeated runs may benefit from warm caches.

## Reporting template

```markdown
## Document conversion experiment

- Source: <public or sanitised description>
- Task: <exact task>
- Tool/model: <tool and model>
- Converter/version: <converter and version>
- Runs per arm: <number>

### Result

| Arm | Median input tokens | Median total tokens | Success score | Preparation time |
| --- | ---: | ---: | ---: | ---: |
| Original document | TODO | TODO | TODO | TODO |
| Complete Markdown | TODO | TODO | TODO | TODO |
| Selected Markdown | TODO | TODO | TODO | TODO |
| Selected Markdown + visual | TODO | TODO | TODO | TODO |

### Findings

- TODO

### Conversion limitations

- TODO

### Safety and privacy notes

- TODO
```

## Integrity rule

Publish raw measurements, task prompts, selection rules, failed runs, and caveats where the source data can be shared safely. Do not convert one successful example into a universal percentage claim.