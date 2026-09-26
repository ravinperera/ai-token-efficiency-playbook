# Agent Adapter Manifest

Use one record per tool-specific instruction or agent adapter when a canonical policy/agent definition is rendered, converted, copied, or maintained across multiple AI clients.

## Canonical Source

- Policy/agent name: _Stable logical identifier._
- Canonical source path: _Repository path or source record._
- Repository/ref: _Repository plus immutable commit/tag when reproducibility matters._
- Canonical source hash: _Hash or `not recorded`._

## Target Adapter

- Target tool/client: _Codex, Claude Code, Copilot, Cursor, Gemini, or other._
- Adapter path/destination: _Exact installed or repository path._
- Scope: _Repository, project, user, workspace, or other._
- Transform/renderer: _Manual thin adapter, script/tool name, or `none`._
- Transform/renderer version: _Version/commit or `not applicable`._
- Provider-specific override delta: _Only intentional differences from the canonical source; use `none` when there are none._
- Rendered/adapter hash: _Hash or `not recorded`._

## Drift And Verification

- Drift state: _Current, source-outdated, locally modified, missing, foreign/unmanaged, or unknown._
- Repository validation: _Checks run and result._
- Live client version tested: _Exact client/host version or `not verified`._
- Live verification date: _YYYY-MM-DD or `not verified`._
- Behaviour verified: _Small observable check showing discovery/precedence when available._
- Known precedence/compatibility limitation: _Keep concise._

## Maintenance

- Last reconciled: _YYYY-MM-DD._
- Reconcile when: _Canonical source, transform, client semantics, destination, or provider override changes._
- Owner: _Person/team responsible for resolving drift._

## Rules

- Keep shared policy in one canonical source; do not duplicate full policy into every adapter merely for convenience.
- Make provider-specific differences explicit and minimal.
- Do not treat a matching rendered hash as proof that a client discovered, prioritised, or obeyed the file.
- If multiple copies changed independently, resolve the conflict deliberately rather than silently choosing the newest file.
- Record `unknown` or `not verified` instead of inventing provenance or compatibility evidence.
