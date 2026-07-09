# Changelog

All notable changes to this project are documented here.

This project follows a lightweight, documentation-first changelog. Versions are intentionally simple because the repository provides guidance, templates, and checks rather than a packaged library.

## [Unreleased]

### Added

- Space for upcoming tool-specific instruction files, examples, templates, and hygiene checks.

### Changed

- Space for updates to guidance, checklists, and contributor workflow.

## [0.1.0] - 2026-07-09

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
