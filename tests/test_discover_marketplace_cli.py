import json
from pathlib import Path

from typer.testing import CliRunner

from safeskill.cli import app
import safeskill.cli as cli_module



def test_discover_marketplace_writes_normalized_batch_manifest(tmp_path: Path) -> None:
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
    output_file = tmp_path / "normalized-batch.json"

    result = CliRunner().invoke(app, ["discover-marketplace", str(export_file), str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()
    assert str(output_file.resolve()) in result.stdout

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload == [
        {
            "type": "github",
            "source": "https://github.com/example/demo-skill",
            "name": "demo-skill",
            "platform": "skillsmp",
        }
    ]



def test_discover_marketplace_writes_live_smithery_listing_export(tmp_path: Path, monkeypatch) -> None:
    html = '''
    <html><body>
      <a href="/skills/anthropics/pdf">anthropics/pdf</a>
      <a href="/skills/github/web-design-reviewer">github/web-design-reviewer</a>
    </body></html>
    '''

    discovery = cli_module.build_marketplace_discovery_service()
    monkeypatch.setattr(discovery, "_fetch_text", lambda url: html)
    monkeypatch.setattr(cli_module, "build_marketplace_discovery_service", lambda: discovery)

    output_file = tmp_path / "smithery-export.json"
    result = CliRunner().invoke(app, ["discover-marketplace", "https://smithery.ai/skills", str(output_file)])

    assert result.exit_code == 0
    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload == [
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
