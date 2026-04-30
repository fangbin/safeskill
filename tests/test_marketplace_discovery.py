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
    listing_html = '''
    <html><body>
      <a href="/skills/anthropics/pdf">anthropics/pdf</a>
      <a href="/skills/github/web-design-reviewer">github/web-design-reviewer</a>
      <a href="/pricing">Pricing</a>
    </body></html>
    '''
    detail_html = {
        "https://smithery.ai/skills/anthropics/pdf": '<a href="https://github.com/anthropics/skills/tree/main/skills/pdf">Source</a>',
        "https://smithery.ai/skills/github/web-design-reviewer": '<a href="https://github.com/example/web-design-reviewer">GitHub</a>',
    }
    service = MarketplaceDiscoveryService()

    def fake_fetch(url: str) -> str:
        if url == "https://smithery.ai/skills":
            return listing_html
        return detail_html[url]

    monkeypatch.setattr(service, "_fetch_text", fake_fetch)

    discovered = service.discover("https://smithery.ai/skills")

    assert discovered == [
        {
            "type": "github",
            "source": "https://github.com/anthropics/skills/tree/main/skills/pdf",
            "name": "anthropics/pdf",
            "platform": "smithery",
        },
        {
            "type": "github",
            "source": "https://github.com/example/web-design-reviewer",
            "name": "github/web-design-reviewer",
            "platform": "smithery",
        },
    ]



def test_discover_smithery_listing_skips_detail_pages_without_github_repo(monkeypatch) -> None:
    listing_html = '''
    <html><body>
      <a href="/skills/anthropics/pdf">anthropics/pdf</a>
      <a href="/skills/example/no-repo">example/no-repo</a>
    </body></html>
    '''
    detail_html = {
        "https://smithery.ai/skills/anthropics/pdf": '<a href="https://github.com/anthropics/skills/tree/main/skills/pdf">Source</a>',
        "https://smithery.ai/skills/example/no-repo": '<p>No repository listed</p>',
    }
    service = MarketplaceDiscoveryService()

    def fake_fetch(url: str) -> str:
        if url == "https://smithery.ai/skills":
            return listing_html
        return detail_html[url]

    monkeypatch.setattr(service, "_fetch_text", fake_fetch)

    discovered = service.discover("https://smithery.ai/skills")

    assert discovered == [
        {
            "type": "github",
            "source": "https://github.com/anthropics/skills/tree/main/skills/pdf",
            "name": "anthropics/pdf",
            "platform": "smithery",
        }
    ]



def test_extract_github_repo_url_prefers_repository_section_over_org_link() -> None:
    html = '''
    <a href="https://github.com/smithery-ai" aria-label="GitHub Organization">Org</a>
    <img src="https://github.com/anthropics.png"/>
    <span>Repository</span>
    <a href="https://github.com/anthropics/skills/tree/main/skills/pdf">anthropics/skills</a>
    '''

    repo_url = MarketplaceDiscoveryService()._extract_github_repo_url(html)

    assert repo_url == "https://github.com/anthropics/skills/tree/main/skills/pdf"



def test_discover_rejects_unsupported_live_marketplace_url() -> None:
    with pytest.raises(ValueError, match="Unsupported marketplace source"):
        MarketplaceDiscoveryService().discover("https://example.com/skills")
