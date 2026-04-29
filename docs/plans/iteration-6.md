# SafeSkill Iteration 6 Plan

## Iteration 6: Batch scan CLI

Goal: add a batch scanning command that accepts a JSON array of skill targets and returns one analysis report per target, so SafeSkill can scan multiple agent skills in a single invocation.

Architecture:
- Reuse `InputAdapterService.load_batch_manifest()` to resolve batch input files.
- Reuse existing `SkillManifestParser` + `AnalysisPipeline` for each target.
- Add a new CLI command that outputs a JSON object with per-target reports and aggregate totals.

Scope:
1. Add failing CLI test for `scan-batch`.
2. Implement a batch scan service/model with aggregate summary.
3. Wire the new command into `src/safeskill/cli.py`.
4. Run targeted tests, then full suite.

Out of scope:
- Parallel execution
- Semantic analyzer beyond stub
- HTML/Markdown reporting
