# SafeSkill Iteration 7 Plan

## Iteration 7: Markdown risk report export

Goal: add a CLI command that scans a single skill and exports a human-readable Markdown risk report for review and sharing.

Architecture:
- Reuse the existing analysis pipeline for a single target.
- Add a report renderer that converts `StaticAnalysisReport` into Markdown.
- Add an export CLI command that writes the report to a user-provided path.

Scope:
1. Add failing CLI test for report export.
2. Add renderer module for Markdown output.
3. Wire export command into CLI and write output file.
4. Run targeted tests, then full suite.

Out of scope:
- HTML rendering
- Batch Markdown export
- Report templating/themes
