# Repository Safety Assumptions

This repository provides reusable guidance, templates, and lightweight checks for reducing unnecessary AI context. It is guidance rather than an enforcement boundary, so adopting teams should apply it inside their existing data-handling, model-governance, and change-control practices.

## What this repository affects

The playbook can influence which source files, logs, prompts, documents, summaries, memory notes, and model choices are used during an AI-assisted task. It can also influence how token and context measurements are interpreted.

## Trust boundaries

Teams should make these boundaries explicit:

1. Repository content may be incomplete, stale, generated, or unsuitable for a particular AI service.
2. Local tools can still send selected material to a configured model endpoint.
3. Summaries and handoffs can retain information longer than the original task.
4. Markdown guidance can influence behaviour but does not replace organisational controls or human approval.
5. Token and context measurements are approximations unless collected with a consistent methodology.

## Operating assumptions

Safe adoption assumes that teams:

- classify information before using it as AI context;
- use approved model providers, accounts, regions, and retention settings;
- review generated summaries before treating them as durable facts;
- independently verify material code, infrastructure, and production changes;
- keep enough evidence to reproduce important benchmark claims.

## Known failure modes

Possible failure modes include selecting too little context, retaining stale information in a summary, copying instructions into a project with different data rules, choosing a lower-capability model for a high-risk task, or presenting a rough context estimate as an exact provider token count.

## Existing mitigations

The repository reduces these risks by prioritising relevant evidence over blanket context removal, separating active context from durable memory and searchable history, documenting approximation limits, keeping helper checks credential-free, and providing regression coverage for helper scripts and repository documentation.

## Residual limitations

The repository cannot determine whether a particular file is approved for a given model service, whether a generated summary is complete, or whether a model choice satisfies organisation-specific requirements. Those decisions remain with the adopting team.

## Review triggers

Revisit these assumptions when a new model provider or retention option is introduced, durable memory or automated compaction becomes part of the runtime, helper scripts begin reading new sources, benchmark methods change, or the repository gains automated write or deployment behaviour.

Before copying this guidance into another project, confirm the target project's approved AI usage boundary and independent verification path for high-impact changes. Token efficiency should not override correctness or change control.
