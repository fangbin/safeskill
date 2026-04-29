import json
from pathlib import Path

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
