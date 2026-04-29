import json
from pathlib import Path

import pytest

from safeskill.marketplace_discovery import MarketplaceDiscoveryService



def test_discover_normalizes_github_marketplace_entries(tmp_path: Path) -> None:
    export_file = tmp_path / "marketplace.json"
    export_file.write_text(
        json.dumps(
            [
                {
                    "marketplace": "skillsmp",
                    "name": "demo-skill",
                    "repo_url": "https://github.com/example/demo-skill",
                }
            ]
        ),
        encoding="utf-8",
    )

    discovered = MarketplaceDiscoveryService().discover(str(export_file))

    assert discovered == [
        {
            "type": "github",
            "source": "https://github.com/example/demo-skill",
            "name": "demo-skill",
            "platform": "skillsmp",
        }
    ]



def test_discover_skips_entries_without_github_repo(tmp_path: Path) -> None:
    export_file = tmp_path / "marketplace.json"
    export_file.write_text(
        json.dumps(
            [
                {
                    "marketplace": "skillsllm",
                    "name": "web-only-skill",
                    "url": "https://skillsllm.com/skills/web-only-skill",
                }
            ]
        ),
        encoding="utf-8",
    )

    discovered = MarketplaceDiscoveryService().discover(str(export_file))

    assert discovered == []



def test_discover_smithery_listing_url_extracts_marketplace_entries(monkeypatch) -> None:
    html = '''
    <html><body>
      <a href="/skills/anthropics/pdf">anthropics/pdf</a>
      <a href="/skills/github/web-design-reviewer">github/web-design-reviewer</a>
      <a href="/pricing">Pricing</a>
    </body></html>
    '''
    service = MarketplaceDiscoveryService()
    monkeypatch.setattr(service, "_fetch_text", lambda url: html)

    discovered = service.discover("https://smithery.ai/skills")

    assert discovered == [
        {
            "marketplace": "smithery",
            "name": "anthropics/pdf",
            "marketplace_url": "https://smithery.ai/skills/anthropics/pdf",
        },
        {
            "marketplace": "smithery",
            "name": "github/web-design-reviewer",
            "marketplace_url": "https://smithery.ai/skills/github/web-design-reviewer",
        },
    ]



def test_discover_rejects_unsupported_live_marketplace_url() -> None:
    with pytest.raises(ValueError, match="Unsupported marketplace source"):
        MarketplaceDiscoveryService().discover("https://example.com/skills")
