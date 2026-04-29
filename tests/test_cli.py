from pathlib import Path

from typer.testing import CliRunner

from safeskill.cli import app



def test_inspect_input_outputs_normalized_json_for_directory(tmp_path: Path) -> None:
    skill_dir = tmp_path / "demo-skill"
    skill_dir.mkdir()

    result = CliRunner().invoke(app, [str(skill_dir)])

    assert result.exit_code == 0
    assert '"source_type": "local"' in result.stdout
    assert '"name": "demo-skill"' in result.stdout
