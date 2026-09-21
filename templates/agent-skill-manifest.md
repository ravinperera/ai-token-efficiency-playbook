# Agent Skill Manifest

Use this lightweight manifest to describe a reusable agent skill without embedding the skill's full instructions in always-on context. Keep it beside the skill, in a discovery registry, or in another location the runtime can query on demand.

## Identity

- **Skill name:**
- **Purpose:**
- **Owner/maintainer:**
- **Source repository/package:**
- **Immutable version, release, or commit:**
- **Retrieved/reviewed date:**
- **Licence:**

## Runtime And Dependencies

- **Supported agent/runtime:**
- **Operating-system/platform prerequisites:**
- **Required packages, binaries, APIs, databases, or services:**
- **Network access required:** yes / no / conditional
- **Authentication or credentials required:**

## Inputs And Outputs

- **Expected inputs:**
- **Expected outputs/artifacts:**
- **Authoritative source data:**
- **Known limitations / unsupported cases:**

## Permissions And External Actions

- **Read permissions required:**
- **Write permissions required:**
- **External actions the skill may request:**
- **Install/download requirements:**
- **Data egress or external-service use:**
- **Human approval required before:**

Discovery of this manifest does **not** grant any listed permission. The surrounding host, policy, and user authorization still decide what the agent may do.

## Reproducibility And Provenance

Record the fields needed to reproduce material work:

- **Tool/dependency versions:**
- **Configuration/parameters:**
- **Random seed, if relevant:**
- **Input dataset/artifact identifiers:**
- **Checksums or immutable artifact versions, if useful:**
- **Derived-output location/version:**
- **Citation/attribution requirements:**

Preserve authoritative raw evidence where exact reproduction or audit matters; do not retain only an agent-generated summary.

## Safety And Accountability

- **High-risk or regulated use cases:**
- **Required qualified-human/institutional review:**
- **Prohibited actions or data:**
- **Escalation / stop conditions:**

## Refresh And Retirement

Refresh or re-evaluate this manifest when the skill source, dependencies, APIs, permissions, data boundary, or supported runtime changes.

- **Freshness/review interval:**
- **Refresh trigger(s):**
- **Revocation/retirement condition:**
- **Replacement skill/version, if any:**

## Selection Note

Load this skill only when its purpose matches the current task and it is part of the minimum sufficient skill set. Do not keep it active after the task changes solely because it was useful earlier.
