import json
from pathlib import Path

from typer.testing import CliRunner

from safeskill.cli import app



def write_skill(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path



def test_scan_batch_outputs_reports_and_aggregate_summary(tmp_path: Path) -> None:
    skill_a_dir = tmp_path / "skill-a"
    skill_a_dir.mkdir()
    skill_a = write_skill(
        skill_a_dir / "SKILL.md",
        "# Skill A\n\n```bash\nrm -rf /tmp/demo\n```\n",
    )

    skill_b_dir = tmp_path / "skill-b"
    skill_b_dir.mkdir()
    skill_b = write_skill(
        skill_b_dir / "SKILL.md",
        "# Skill B\n\nSee http://192.168.1.10/payload\n",
    )

    batch_manifest = tmp_path / "batch.json"
    batch_manifest.write_text(
        json.dumps([str(skill_a), str(skill_b)]),
        encoding="utf-8",
    )

    result = CliRunner().invoke(app, ["scan-batch", str(batch_manifest)])

    assert result.exit_code == 0
    assert '"total_targets": 2' in result.stdout
    assert '"total_findings": 2' in result.stdout
    assert '"dangerous-command.rm-rf"' in result.stdout
    assert '"suspicious-url.raw-ip"' in result.stdout
