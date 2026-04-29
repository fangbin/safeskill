# SafeSkill Iteration 8 Plan

## Iteration 8: HTML risk report export

Goal: add a CLI command that scans a single skill and exports a human-readable HTML risk report for browser viewing and sharing.

Architecture:
- Reuse the existing analysis pipeline for a single target.
- Add an HTML report renderer parallel to the Markdown renderer.
- Add an export CLI command that writes a self-contained HTML file.

Scope:
1. Add failing CLI test for HTML report export.
2. Add renderer module for HTML output.
3. Wire export command into CLI and write output file.
4. Run targeted tests, then full suite.

Out of scope:
- CSS themes beyond an inline minimal style
- Batch HTML export
- Interactive filtering/search
