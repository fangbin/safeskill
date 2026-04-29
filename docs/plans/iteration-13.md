# SafeSkill Iteration 13 Plan

## Iteration 13: discover-marketplace export command

Goal: add a dedicated CLI command that converts a marketplace export into a normalized batch manifest file users can inspect, edit, reuse, and feed into `scan-batch`.

Architecture:
- Reuse `MarketplaceDiscoveryService` to normalize marketplace exports.
- Add a `discover-marketplace <input> <output>` command that writes normalized structured targets to disk.
- Keep `scan-marketplace` as a convenience command, while `discover-marketplace` becomes the explicit export step.

Tech Stack: Python, Typer, pytest, existing file output helper, existing marketplace discovery service

---

### Task 1: Add failing CLI test for discover-marketplace

**Objective:** Prove the CLI can write a normalized batch manifest from marketplace export input.

**Files:**
- Create: `tests/test_discover_marketplace_cli.py`
- Modify: `src/safeskill/cli.py`

**Step 1: Write failing test**

Add a test that:
- writes a marketplace export JSON with one GitHub entry
- invokes `discover-marketplace <input.json> <output.json>`
- asserts exit code is 0
- asserts output file exists
- asserts file contains a normalized GitHub batch target with `type`, `source`, `name`, `platform`

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_discover_marketplace_cli.py -v`
Expected: FAIL because the command does not exist yet.

**Step 3: Write minimal implementation**

Implement the CLI command by:
- calling `MarketplaceDiscoveryService.discover()`
- serializing discovered targets as JSON
- writing to the given output path with existing output helper

**Step 4: Run test to verify pass**

Run: `python3 -m pytest tests/test_discover_marketplace_cli.py -v`
Expected: PASS

### Task 2: Add regression coverage for reuse with scan-batch

**Objective:** Ensure exported manifests remain compatible with existing batch scan flow.

**Files:**
- Test: `tests/test_discover_marketplace_cli.py`
- Test: existing batch and marketplace tests

**Step 1: Add compatibility assertion**

Extend tests or rely on existing structure checks to ensure output matches the structured GitHub target schema already consumed by `scan-batch`.

**Step 2: Run targeted tests**

Run: `python3 -m pytest tests/test_discover_marketplace_cli.py tests/test_scan_marketplace_cli.py tests/test_scan_batch_cli.py -q`
Expected: PASS

### Task 3: Full regression and commit

**Objective:** Verify no existing CLI behaviors regress.

**Files:**
- Modify: `src/safeskill/cli.py`
- Create: `docs/plans/iteration-13.md`

**Step 1: Run full suite**

Run: `python3 -m pytest -q`
Expected: PASS

**Step 2: Commit**

```bash
git add src/safeskill/cli.py tests/test_discover_marketplace_cli.py docs/plans/iteration-13.md
git commit -m "feat: add marketplace export command"
```
