from pathlib import Path

from typer.testing import CliRunner

from safeskill.cli import app



def test_parse_manifest_outputs_manifest_json(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text("# Demo Skill\n\nSee https://example.com\n", encoding="utf-8")

    result = CliRunner().invoke(app, ["parse-manifest", str(skill_file)])

    assert result.exit_code == 0
    assert '"title": "Demo Skill"' in result.stdout
    assert '"urls": ["https://example.com"]' in result.stdout
