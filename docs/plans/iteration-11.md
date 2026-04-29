# SafeSkill Iteration 11 Plan

## Iteration 11: Marketplace skill download and analysis MVP

Goal: enable SafeSkill to consume a batch manifest containing GitHub-hosted marketplace skill entries, fetch them, and run the existing analysis pipeline automatically.

Architecture:
- Extend batch manifest parsing to support structured remote entries alongside existing local path strings.
- Reuse the existing GitHub fetcher for remote skill retrieval inside batch scanning.
- Keep the CLI surface minimal by upgrading `scan-batch` instead of adding a new command in this iteration.

Tech Stack: Python, Typer, pytest, existing `GitHubSkillFetcher`, existing `AnalysisPipeline`

---

### Task 1: Add failing adapter tests for structured GitHub batch entries

**Objective:** Prove batch manifests can describe marketplace/GitHub targets before implementation.

**Files:**
- Modify: `tests/test_batch_input_adapter.py`
- Modify: `src/safeskill/adapters/input_adapter.py`
- Modify: `src/safeskill/models/input_target.py`

**Step 1: Write failing test**

Add a test that writes a batch JSON like:

```json
[
  {
    "type": "github",
    "source": "https://github.com/example/demo-skill",
    "name": "demo-skill",
    "platform": "skillsmp"
  }
]
```

and asserts:
- `source_type == SourceType.GITHUB`
- `source == repo url`
- metadata contains `name` and `platform`

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_batch_input_adapter.py -v`
Expected: FAIL because `load_batch()` only accepts string paths today.

**Step 3: Write minimal implementation**

Implement structured batch item parsing in `InputAdapterService`.

**Step 4: Run test to verify pass**

Run: `python3 -m pytest tests/test_batch_input_adapter.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_batch_input_adapter.py src/safeskill/adapters/input_adapter.py src/safeskill/models/input_target.py
git commit -m "feat: support github batch targets"
```

### Task 2: Add failing batch scan CLI test for GitHub marketplace entries

**Objective:** Prove `scan-batch` can fetch remote GitHub skills and analyze them.

**Files:**
- Modify: `tests/test_scan_batch_cli.py`
- Modify: `src/safeskill/pipeline/batch_scan_service.py`
- Modify: `src/safeskill/cli.py` if wiring changes are needed

**Step 1: Write failing test**

Add a CLI test that:
- creates a fake repo directory with `SKILL.md`
- writes a batch manifest with a structured GitHub entry
- monkeypatches the fetcher/service so no real network is used
- asserts `scan-batch` output includes findings from the fetched skill

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_scan_batch_cli.py::test_scan_batch_fetches_github_targets_and_outputs_findings -v`
Expected: FAIL because batch scanning currently tries to treat every manifest item as a local path.

**Step 3: Write minimal implementation**

Teach `BatchScanService` to:
- detect `SourceType.GITHUB`
- fetch via `GitHubSkillFetcher`
- parse fetched repo directory
- run the existing pipeline

**Step 4: Run test to verify pass**

Run: `python3 -m pytest tests/test_scan_batch_cli.py::test_scan_batch_fetches_github_targets_and_outputs_findings -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_scan_batch_cli.py src/safeskill/pipeline/batch_scan_service.py src/safeskill/cli.py
git commit -m "feat: analyze github marketplace skills in batch scans"
```

### Task 3: Run regression tests

**Objective:** Verify local batch scanning still works and GitHub batch scanning integrates cleanly.

**Files:**
- Test: `tests/test_batch_input_adapter.py`
- Test: `tests/test_scan_batch_cli.py`
- Test: full suite

**Step 1: Run targeted tests**

Run: `python3 -m pytest tests/test_batch_input_adapter.py tests/test_scan_batch_cli.py -q`
Expected: PASS

**Step 2: Run full suite**

Run: `python3 -m pytest -q`
Expected: PASS

**Step 3: Commit final polished state**

```bash
git add tests/test_batch_input_adapter.py tests/test_scan_batch_cli.py src/safeskill/adapters/input_adapter.py src/safeskill/models/input_target.py src/safeskill/pipeline/batch_scan_service.py docs/plans/iteration-11.md
git commit -m "feat: add marketplace batch scan mvp"
```
