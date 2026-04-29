# SafeSkill Iteration 9 Plan

## Iteration 9: GitHub repository skill pull and scan

Goal: add a CLI command that clones a GitHub repository containing a skill and scans its `SKILL.md` directly, enabling remote repository analysis.

Architecture:
- Add a GitHub-oriented fetch service that clones a repository into a temporary directory.
- Reuse existing manifest parsing and analysis pipeline after clone.
- Add a CLI command that accepts a GitHub repo URL and returns the same JSON scan report as local scan.

Scope:
1. Add failing CLI test for GitHub repo scan.
2. Add repository fetch abstraction to support test doubles.
3. Wire remote fetch + local scan into a new CLI command.
4. Run targeted tests, then full suite.

Out of scope:
- Authentication for private repos
- GitHub API metadata enrichment
- Batch remote repo scanning
