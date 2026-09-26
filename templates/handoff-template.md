# Handoff Template

Use this for agent-to-agent, agent-to-human, or session-to-session transfers. Prefer durable repository/artifact references over replaying conversation history.

## Summary

Describe the completed work and intended next step in one or two sentences.

## Ownership And Scope

- Handoff ID or task: _Add a stable issue, task, or work-item identifier._
- Sender/owner: _Who produced the handoff._
- Recipient/next owner: _Who should act next._
- Allowed next action: _Review, test, continue implementation, merge, publish, or another bounded action._
- Merge/release authority: _State who may accept or integrate the work; do not infer authority from possession of the handoff._

## Authoritative State

- Repository/project: _Add the authoritative repository or workspace._
- Isolated workspace: _Branch, worktree, sandbox, or `not applicable`._
- Base revision: _Commit SHA, tag, artifact version, or other starting state._
- Handoff revision: _Commit SHA, artifact hash/version, or exact immutable output to inspect._
- Changed paths or artifacts: _List only what the recipient needs to inspect._

Prefer references to durable state over repasting files, diffs, logs, or prior discussion. If the work is not committed or otherwise immutable, say so explicitly.

## Freshness And Conflict Check

- Base still current: _Yes, no, or not checked._
- Known concurrent work/conflict risk: _List only material overlap._
- Revalidation needed after rebase/merge: _Name checks that must be repeated if the authoritative state changes._

## Known Facts

- _Add only facts the recipient cannot cheaply recover from the authoritative state._

## Error Or Signal

Paste the smallest useful error message or signal.

## Validation

- Command or check: _Add validation performed._
- Result: _Pass, fail, or not run._
- Evidence revision: _Bind the result to the handoff commit/artifact when material._

## Approval Gates And Blockers

- Required approval/review: _Name the gate or `none`._
- Current status: _Pending, approved, rejected, or not applicable._
- Blocker: _Add only unresolved conditions that prevent the next permitted action._

Do not replace required approval evidence with an agent-generated statement that approval occurred.

## Already Tried

- _Add an attempted step only when it prevents repeated work._

## Open Questions

- _Add an unresolved question only when the recipient must answer it before continuing._

## Recipient Acceptance

Before continuing, the recipient should confirm that the referenced state exists, the task is still current, required approvals remain valid, and the next action is inside their authority. If the base or handoff revision has materially changed, re-establish the authoritative state instead of continuing from stale conversational context.
