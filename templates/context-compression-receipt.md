# Context Compression Receipt

Use this receipt when context is compressed, compacted, deduplicated, or replaced with references while the authoritative evidence remains separately retrievable. Here, **reversible** means the workflow can return to that source; it does not mean the compact representation can reconstruct the original by itself.

## Source

- Task/session identifier:
- Source reference(s):
- Source revision/hash:
- Source type: conversation / log / file / retrieval result / tool output / other
- Project/tenant boundary:
- Created/observed at:

## Protection

- Recent context protected verbatim:
- Exact values or wording protected:
- Security/legal/financial/production evidence protected:
- Human-approved or citation-bound evidence protected:
- Reason these items must remain verbatim:

## Transform

- Compression method:
- Tool/version or procedure:
- Original size/tokens:
- Compressed size/tokens:
- Inflation check passed: Yes / No / Unknown
- If token counts are unavailable, proxy used:
- Categories omitted/deduplicated:
- Categories deliberately retained:

## Reversibility

- Authoritative original retained separately: Yes / No
- Retrieval mechanism:
- Smallest retrievable unit:
- Retrieval reference validated: Yes / No
- Access/authorisation rechecked at retrieval time: Yes / No / N/A
- Expected expiry/retention:
- Behaviour if source expires, is deleted, becomes unavailable, or access is revoked:

## Cache Behaviour

- Stable prefix intentionally preserved: Yes / No / Unknown
- Provider cache telemetry available: Yes / No
- Cached/read/write token classes recorded: Yes / No / N/A
- Recompression expected to invalidate cache: Yes / No / Unknown

## Verification

- Must-retain evidence check:
- Retrieval spot-check:
- Task verification:
- Compression/retrieval failures:
- Fallback to original required: Yes / No
- Reviewer/owner:

## Notes

Record measured savings only when raw and compressed runs are comparable. A smaller representation is not automatically cheaper if it breaks a useful cache, adds retrieval overhead, or loses required evidence.
