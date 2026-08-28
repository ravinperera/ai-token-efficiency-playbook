# Adapter Compatibility and Verification Status

This page records what the repository actually validates for each shipped AI-tool adapter. It deliberately separates **repository-level verification** from **live runtime compatibility** with a particular vendor client version.

Review date: **2026-08-28**

| Tool / adapter | Instruction file | Installer selector | Repository-validated | Live client version verified here | Known limitation |
| --- | --- | --- | --- | --- | --- |
| Codex / general coding agents | `AGENTS.md` | `codex` (also accepts `agents`) | Yes — installer tests and instruction-size/token-hygiene checks cover the shipped file. | No specific client version is pinned or exercised by repository CI. | Tools that use a different instruction-file discovery convention need a manual adapter. |
| Claude Code | `CLAUDE.md` | `claude` | Yes — installer tests and instruction-size/token-hygiene checks cover the shipped file. | No specific Claude Code version is pinned or exercised by repository CI. | Vendor parsing, precedence, and feature behaviour can change independently of this repository. |
| Gemini CLI / agents | `GEMINI.md` | `gemini` | Yes — installer tests and instruction-size/token-hygiene checks cover the shipped file. | No specific Gemini client version is pinned or exercised by repository CI. | Runtime instruction precedence and supported agent features remain tool-specific. |
| GitHub Copilot | `.github/copilot-instructions.md` | `copilot` | Yes — installer tests cover nested-path creation and token hygiene checks cover the shipped file. | No specific Copilot client/IDE version is pinned or exercised by repository CI. | Support and precedence can vary by IDE, Copilot surface, and repository configuration. |
| Cursor | `.cursor/rules/token-efficiency.mdc` | `cursor` | Yes — installer tests cover nested-path creation and token hygiene checks cover the shipped file. | No specific Cursor version is pinned or exercised by repository CI. | Cursor rule semantics and precedence are controlled by the client and can evolve. |

## What "repository-validated" means

The repository can verify properties it owns:

- the adapter file exists at the documented path;
- the installer maps a selector to the expected destination;
- nested directories are created where required;
- existing instruction files are not overwritten unless `--force` is explicit;
- unsupported selectors fail safely;
- the shipped instruction files remain inside the repository's default size threshold;
- helper regression tests and Markdown/token-hygiene workflows pass.

These checks are useful but **do not prove that every current or future version of an external AI client will discover, parse, prioritise, or obey the file exactly as intended**.

## Runtime verification guidance

When a specific client/version matters to an organisation:

1. record the client name, version, IDE/host if relevant, and date;
2. install the adapter into a disposable test repository;
3. run a small behaviour check that distinguishes the adapter from the tool's default behaviour;
4. record whether the instruction file was discovered and whether higher-priority organisation/user rules overrode it;
5. re-test after major client changes or when the vendor changes instruction-file semantics.

Do not convert a repository test date into a vendor compatibility claim. If a live version has not been exercised, record it as **not verified** rather than inferring compatibility from the filename alone.

## Maintenance rule

Re-review this matrix whenever an adapter path, installer selector, or validation behaviour changes. Runtime-version claims should only be added when there is reproducible evidence for that exact client/version and should include the verification date and test method.
