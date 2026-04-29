# SafeSkill Iteration Plan

## Iteration 2: SkillManifest parser MVP

Goal: implement the parsing/normalization layer for local skill directories and single `SKILL.md` files with full automated tests.

### Feature scope
1. Add normalized manifest models:
   - `SkillManifest`
   - `ScriptBlock`
   - `ResourceReference`
2. Parse a local skill directory into a manifest.
3. Parse a single `SKILL.md` file into a manifest.
4. Extract from markdown:
   - title
   - frontmatter-ish metadata keys when present (`name`, `author`, `version`)
   - fenced code blocks as scripts
   - markdown links as references
   - URLs embedded in text
5. CLI command:
   - `safeskill parse-manifest <target>`
   - prints normalized JSON manifest
6. Tests for every delivered behavior.

### TDD task breakdown
1. Write failing model tests for manifest structures.
2. Implement minimal manifest models.
3. Write failing parser tests for title/metadata extraction.
4. Implement markdown parser.
5. Write failing parser tests for code block/reference/URL extraction.
6. Implement extraction details.
7. Write failing CLI test for `parse-manifest`.
8. Implement CLI command.
9. Run full suite.
10. Commit.

### Non-goals for iteration 2
- semantic analysis
- static rule scoring
- dynamic sandbox execution
- benchmark sync
- HTML reports
