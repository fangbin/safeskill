import json
from pathlib import Path

from typer.testing import CliRunner

from safeskill.cli import app



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
