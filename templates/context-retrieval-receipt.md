# Context Retrieval Receipt

Use this lightweight receipt when a meaningful answer depends on search, a structural index, code graph, durable project memory, retrieval cache, or an escalation from a smaller view to authoritative source.

Keep the receipt metadata-focused. Do not copy prompts, source code, secrets, customer data, or retrieved document contents into it unless they are already approved evidence for the task.

## Retrieval identity

- Task/run ID:
- Repository/project identifier:
- Authoritative source ref/commit:
- Retrieval system/tool:
- Retrieval mode: `search | outline | symbol/range | graph/index | full source | other`
- Query/purpose:

## Provenance and freshness

- Index/cache revision represented:
- Index/cache generated or refreshed at:
- Parser/indexer/schema version:
- Material exclusions or ignored paths:
- Freshness state: `fresh | stale | unknown | not applicable`
- Freshness check performed:
- Revision mismatch detected: `yes | no | unknown`

If the retrieval layer cannot prove which source revision it represents, record freshness as `unknown` and verify material conclusions against authoritative source.

## Relationship provenance

Complete this section when graph/index relationships materially influence the answer.

- Relationship classes observed: `extracted | inferred | ambiguous | mixed | not applicable`
- Material source anchors present: `yes | no | partial | not applicable`
- Confidence/uncertainty metadata present for inferred relationships: `yes | no | not applicable`
- Ambiguous relationships requiring review:
- Material inferred relationships independently verified against source: `yes | no | not required`
- Unsupported or unresolvable relationships observed:

`extracted` means directly derived from authoritative source or deterministic parsing. `inferred` means proposed by a model or heuristic. `ambiguous` means the evidence is conflicting or insufficient. A confidence score is metadata, not proof.

## Context returned

- Files/symbols/sections selected:
- Bytes/chars returned, if measurable:
- Input tokens attributable to this retrieval, if available:
- Tool/retrieval calls:
- Larger view avoided, if measured:
- Reason this view was sufficient:

Do not convert a tool-reported "bytes avoided" value into a token-saving claim unless total workflow tokens are independently measured.

## Escalation and fallback

- Larger view requested: `yes | no`
- Escalation reason:
- Authoritative-source fallback required: `yes | no`
- Fallback source/ref:
- Fallback result:

Typical fallback triggers include stale or unknown index state, incomplete relationships, inferred or ambiguous material relationships, missing source anchors, missing generated/runtime behaviour, security-sensitive conclusions, and decisions that depend on exact implementation details.

## Boundary and safety checks

- Intended repository/project boundary preserved: `yes | no | unknown`
- Excluded/sensitive paths respected: `yes | no | unknown`
- Cross-project or cross-tenant data observed: `yes | no`
- Secrets or confidential content collected only for measurement: `yes | no`
- Approval required before broader retrieval: `yes | no`

## Verification

- Verification method:
- Result: `pass | fail | partial | not run`
- Stale/incomplete retrieval affected the answer: `yes | no | unknown`
- Provenance uncertainty affected the answer: `yes | no | unknown`
- Final decision verified against authoritative source where required: `yes | no | not required`
- Notes:

## Interpretation

A smaller retrieval is not automatically better. Compare the complete workflow, including index build/refresh cost, retries, fallbacks, verification, correctness, task outcome, and provenance quality. A receipt is evidence about what context was consumed and why; it is not itself proof of a saving.
