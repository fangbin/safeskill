# SafeSkill Iteration Plan

## Iteration 1: Project scaffold + input adapters MVP

Goal: deliver the first runnable vertical slice of the architecture with tests-first coverage.

### Feature scope
1. Python project scaffold with `src/` layout and pytest configuration.
2. Core normalized data models:
   - `SourceType`
   - `TargetMetadata`
   - `InputTarget`
3. Input adapter layer MVP:
   - local directory adapter
   - single `SKILL.md` file adapter
   - batch manifest adapter
4. CLI entrypoint:
   - `safeskill inspect-input <target>`
   - prints normalized JSON for one target
5. Tests for every delivered behavior.

### TDD task breakdown
1. Add project packaging/test config.
2. Write failing tests for normalized input models.
3. Implement minimal models to pass tests.
4. Write failing tests for local directory + skill file adapters.
5. Implement minimal adapter resolution logic.
6. Write failing tests for batch manifest adapter.
7. Implement batch manifest loading.
8. Write failing CLI test for `inspect-input`.
9. Implement CLI command.
10. Run full test suite.
11. Commit.

### Non-goals for iteration 1
- static threat rules
- semantic analysis
- dynamic execution sandbox
- marketplace sync
- HTML reporting
