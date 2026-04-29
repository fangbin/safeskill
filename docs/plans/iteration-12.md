# SafeSkill Iteration 12 Plan

## Iteration 12: Marketplace discovery + scan-marketplace MVP

Goal: add a minimal marketplace discovery flow that converts curated marketplace listings into batch manifests and lets users scan discovered entries directly from a new CLI command.

Architecture:
- Introduce a small discovery service that reads a JSON marketplace export and normalizes entries into the structured GitHub batch target format added in iteration 11.
- Add a dedicated `scan-marketplace` CLI command that discovers entries, writes a temporary batch manifest, and reuses `BatchScanService` for analysis.
- Keep scope intentionally narrow: JSON discovery input only, no live crawling yet.

Tech Stack: Python, Typer, pytest, existing batch scan pipeline, temporary files

---

### Task 1: Add failing tests for marketplace discovery normalization

**Objective:** Prove a marketplace export can be normalized into GitHub scan targets.

**Files:**
- Create: `src/safeskill/marketplace_discovery.py`
- Create: `tests/test_marketplace_discovery.py`

**Step 1: Write failing test**

Add tests for a JSON file containing entries such as:

```json
[
  {
    "marketplace": "skillsmp",
    "name": "demo-skill",
    "repo_url": "https://github.com/example/demo-skill"
  }
]
```

Assert discovery returns structured items with:
- `type == "github"`
- `source == repo_url`
- `name == demo-skill`
- `platform == skillsmp`

Also add a test proving non-GitHub entries are skipped.

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_marketplace_discovery.py -v`
Expected: FAIL because discovery service does not exist yet.

**Step 3: Write minimal implementation**

Implement `MarketplaceDiscoveryService.discover(manifest_path)` to load JSON and normalize supported entries.

**Step 4: Run test to verify pass**

Run: `python3 -m pytest tests/test_marketplace_discovery.py -v`
Expected: PASS

### Task 2: Add failing CLI test for scan-marketplace

**Objective:** Prove users can scan a marketplace export directly without manually creating a batch manifest.

**Files:**
- Modify: `src/safeskill/cli.py`
- Modify: `tests/test_scan_marketplace_cli.py`

**Step 1: Write failing test**

Add a CLI test that:
- creates a JSON marketplace export with one GitHub repo entry
- monkeypatches marketplace discovery and GitHub fetching behavior as needed
- invokes `scan-marketplace <export.json>`
- asserts output includes `dangerous-command.curl-pipe-bash`

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_scan_marketplace_cli.py -v`
Expected: FAIL because command does not exist yet.

**Step 3: Write minimal implementation**

Implement `scan-marketplace` by:
- calling the discovery service
- writing discovered targets to a temporary JSON batch manifest
- passing that manifest into `BatchScanService`

**Step 4: Run test to verify pass**

Run: `python3 -m pytest tests/test_scan_marketplace_cli.py -v`
Expected: PASS

### Task 3: Regression tests and commit

**Objective:** Ensure marketplace discovery does not break existing scanning flows.

**Files:**
- Test: `tests/test_marketplace_discovery.py`
- Test: `tests/test_scan_marketplace_cli.py`
- Test: existing batch scan tests

**Step 1: Run targeted tests**

Run: `python3 -m pytest tests/test_marketplace_discovery.py tests/test_scan_marketplace_cli.py tests/test_scan_batch_cli.py -q`
Expected: PASS

**Step 2: Run full suite**

Run: `python3 -m pytest -q`
Expected: PASS

**Step 3: Commit**

```bash
git add src/safeskill/marketplace_discovery.py src/safeskill/cli.py tests/test_marketplace_discovery.py tests/test_scan_marketplace_cli.py docs/plans/iteration-12.md
git commit -m "feat: add marketplace discovery cli"
```
