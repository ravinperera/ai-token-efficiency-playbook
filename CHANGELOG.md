# Changelog

All notable changes to this project are documented here.

This project follows a lightweight, documentation-first changelog. Versions are intentionally simple because the repository provides guidance, templates, and checks rather than a packaged library.

## [Unreleased]

No changes recorded since the first tagged release.

## [0.1.0] - 2026-10-01

First tagged public release. The July baseline below records earlier development, not a previously published GitHub release.

### Included

- Canonical guidance for context hygiene, progressive retrieval, reversible compression, selective skill loading, minimum-necessary implementation, governed model routing/fallback and multi-agent handoffs, monitoring and recovery.
- Instruction adapters for Codex/general coding agents, Claude Code, Gemini CLI, GitHub Copilot and Cursor, with an explicit repository-validation versus live-client compatibility matrix.
- Overwrite-protected installer with source-ref pinning, context-size/token-estimation helpers, and Markdown/local-link and token-hygiene checks with regression tests and GitHub Actions.
- Templates for routing decisions, adapter/skill provenance, continuation handoffs, retrieval/compression receipts, benchmark manifests and token/cost measurement.
- Fixed synthetic evaluation corpus and reproducible benchmark protocols for routing/fallback, orchestration, retrieval, compression, resource discovery, document conversion and minimum-necessary implementation. Protocols are not measured model benchmark results; existing fixture-based case studies retain their stated measurement limitations.
- Original visual overview and accessible text companion, plus practical examples, contributor guidance and safety assumptions.

See the [v0.1.0 release notes](docs/releases/v0.1.0.md) for scope and limitations. This is operating guidance and local tooling, not an implemented orchestration runtime, a universal savings claim or production certification.

## Historical untagged baseline - 2026-07-09

This entry preserves the original development summary. No release tag or GitHub release was published for this baseline date; it is not a separate version.

### Added

- Core token-efficiency playbook with canonical guidance for context hygiene, CLI output compression, coding agents, and model routing.
- Tool adapters for Codex/general agents, Claude Code, Gemini CLI, GitHub Copilot, and Cursor.
- Examples covering before/after prompts, bad versus good context, and CI log triage.
- Templates for token-savings measurement, CI failure triage, and concise handoffs.
- Lightweight `scripts/check-token-hygiene.sh` validation for instruction files and noisy examples.
- GitHub Actions workflow to run token hygiene checks on pull requests and pushes to `main`.
- GitHub issue templates, a pull request checklist, and CODEOWNERS for repository hygiene.

[Unreleased]: https://github.com/ravinperera/ai-token-efficiency-playbook/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ravinperera/ai-token-efficiency-playbook/releases/tag/v0.1.0
