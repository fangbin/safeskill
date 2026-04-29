# SafeSkill Iteration Plan

## Iteration 5: Analyzer pipeline foundation

Goal: introduce a unified analyzer abstraction so static analysis becomes one stage in a composable pipeline, while reserving space for semantic and dynamic analyzers later.

### Feature scope
1. Add shared analysis models:
   - `AnalysisRequest`
   - `AnalysisResult`
2. Add analyzer protocol/interface.
3. Add pipeline executor that runs one or more analyzers and merges findings.
4. Adapt the current static analyzer to the shared analyzer interface.
5. Add a semantic analyzer stub returning no findings for now.
6. Update `safeskill scan <target>` to use the pipeline instead of directly calling static analyzer.
7. Full TDD coverage for models, pipeline, and CLI regression.

### TDD task breakdown
1. Write failing tests for shared analysis models.
2. Implement minimal models.
3. Write failing tests for pipeline execution and merged findings.
4. Implement pipeline executor.
5. Write failing tests for semantic stub behavior.
6. Implement semantic stub.
7. Write failing CLI regression test using pipeline.
8. Run targeted tests and full suite.
9. Commit and push.

### Non-goals for iteration 5
- real LLM integration
- dynamic execution
- benchmark orchestration
- HTML/SARIF export
