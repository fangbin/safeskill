# SafeSkill Iteration 14 Plan

## Iteration 14: Real marketplace discovery integration

Goal: connect SafeSkill to one real marketplace source so discovery can work from a live marketplace URL instead of only pre-exported JSON.

Architecture:
- Start with the easiest proven target: Smithery skill listing pages, which expose stable skill URLs in server-rendered HTML.
- Extend `MarketplaceDiscoveryService` to accept either a local JSON export or a live marketplace URL.
- For Smithery live URLs, fetch HTML, extract skill detail links, and normalize them into marketplace records that can later be enriched.
- Keep MVP narrow: support listing-page discovery from `https://smithery.ai/skills`, returning marketplace entries with `marketplace`, `name`, and `marketplace_url`. Skip repo resolution if not directly available yet.

Tech Stack: Python, urllib, regex/HTML parsing, pytest, existing discovery + CLI pipeline

---

### Task 1: Research and lock first live marketplace target

**Objective:** Choose a real marketplace with stable HTML that can be discovered without browser automation in production code.

**Files:**
- Modify: `docs/plans/iteration-14.md`

**Decision:**
- Use `smithery.ai/skills` first.
- Reason: listing page is reachable without auth, server HTML contains skill links, and link structure is regular (`/skills/<namespace>/<name>`).

### Task 2: Add failing tests for live Smithery discovery

**Objective:** Prove discovery from a live marketplace HTML snapshot works before implementation.

**Files:**
- Modify: `tests/test_marketplace_discovery.py`
- Modify: `src/safeskill/marketplace_discovery.py`

**Step 1: Write failing test**

Add a test that monkeypatches HTML fetch to return a Smithery-like listing page containing anchors such as:

```html
<a href="/skills/anthropics/pdf">anthropics/pdf</a>
<a href="/skills/github/web-design-reviewer">github/web-design-reviewer</a>
```

Assert discovery returns:
- `marketplace == "smithery"`
- `name == "anthropics/pdf"`
- `marketplace_url == "https://smithery.ai/skills/anthropics/pdf"`

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_marketplace_discovery.py -v`
Expected: FAIL because discovery only supports local JSON exports today.

**Step 3: Write minimal implementation**

Implement live URL handling in `MarketplaceDiscoveryService`:
- detect `https://smithery.ai/skills`
- fetch HTML
- extract unique skill links
- normalize to marketplace records

**Step 4: Run test to verify pass**

Run: `python3 -m pytest tests/test_marketplace_discovery.py -v`
Expected: PASS

### Task 3: Add failing CLI test for discover-marketplace live URL export

**Objective:** Prove `discover-marketplace` can export normalized discovery results from a real marketplace URL.

**Files:**
- Modify: `tests/test_discover_marketplace_cli.py`
- Modify: `src/safeskill/cli.py` only if needed

**Step 1: Write failing test**

Monkeypatch marketplace discovery fetch to return Smithery HTML and run:

```bash
discover-marketplace https://smithery.ai/skills output.json
```

Assert the output file contains discovered Smithery entries.

**Step 2: Run test to verify failure**

Run: `python3 -m pytest tests/test_discover_marketplace_cli.py -v`
Expected: FAIL until live URL discovery is implemented.

**Step 3: Run regression tests**

Run: `python3 -m pytest tests/test_marketplace_discovery.py tests/test_discover_marketplace_cli.py tests/test_scan_marketplace_cli.py -q`
Expected: PASS

### Task 4: Full regression and commit

**Objective:** Keep previous JSON-based marketplace flows working.

**Files:**
- Modify: `src/safeskill/marketplace_discovery.py`
- Modify: `docs/plans/iteration-14.md`

**Step 1: Run full suite**

Run: `python3 -m pytest -q`
Expected: PASS

**Step 2: Commit**

```bash
git add src/safeskill/marketplace_discovery.py tests/test_marketplace_discovery.py tests/test_discover_marketplace_cli.py docs/plans/iteration-14.md
git commit -m "feat: add smithery live discovery"
```
