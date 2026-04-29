# SafeSkill Iteration Plan

## Iteration 3: Static rule engine MVP

Goal: add a first-pass static analyzer that converts parsed manifests into structured findings with automated test coverage.

### Feature scope
1. Add normalized finding models:
   - `Severity`
   - `Finding`
   - `StaticAnalysisReport`
2. Implement static rules for:
   - dangerous shell command patterns
   - suspicious URLs / remote execution patterns
   - hardcoded secret/token patterns
3. Analyze these surfaces:
   - extracted script blocks
   - manifest description/title text
   - extracted URLs
4. CLI command:
   - `safeskill scan <target>`
   - parse manifest and print findings JSON
5. Tests for all shipped rules and CLI behavior.

### TDD task breakdown
1. Write failing tests for finding/report models.
2. Implement minimal models.
3. Write failing tests for dangerous command findings.
4. Implement command rules.
5. Write failing tests for suspicious URL and secret findings.
6. Implement URL and secret rules.
7. Write failing CLI test for `scan`.
8. Implement CLI command.
9. Run full suite.
10. Commit and push.

### Non-goals for iteration 3
- severity scoring aggregation beyond static severities
- semantic analysis
- dynamic runtime validation
- SARIF/HTML reporting
