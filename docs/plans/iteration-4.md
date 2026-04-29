# SafeSkill Iteration Plan

## Iteration 4: Static analysis report enrichment

Goal: expand static detection coverage and enrich report structure so scan results become more actionable and easier to aggregate.

### Feature scope
1. Enrich finding model with:
   - `category`
   - `confidence`
   - `source_excerpt`
2. Enrich static analysis report with summary counts:
   - total findings
   - counts by severity
3. Expand dangerous command detection for:
   - `wget ... | sh`
   - `chmod 777`
   - `sudo`
   - `nc` reverse-shell-like patterns
   - `bash -c "$(curl ...)"`
4. Keep `safeskill scan <target>` output aligned with new report schema.
5. Full TDD coverage for all new rules and report fields.

### TDD task breakdown
1. Write failing tests for enriched finding/report models.
2. Implement minimal model changes.
3. Write failing tests for added command rules.
4. Implement rule expansion.
5. Write failing test for summary aggregation.
6. Implement aggregation logic.
7. Run targeted tests, then full suite.
8. Commit and push.

### Non-goals for iteration 4
- semantic analyzer interfaces
- dynamic execution sandbox
- benchmark regression runner
- SARIF/HTML export
