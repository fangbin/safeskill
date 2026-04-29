import json
from pathlib import Path

import pytest

from safeskill.adapters.input_adapter import InputAdapterService
from safeskill.models.input_target import SourceType



def test_load_batch_manifest_returns_multiple_targets(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skill-a"
    skill_dir.mkdir()
    skill_file_dir = tmp_path / "skill-b"
    skill_file_dir.mkdir()
    skill_file = skill_file_dir / "SKILL.md"
    skill_file.write_text("# Skill B\n", encoding="utf-8")
    manifest = tmp_path / "batch.json"
    manifest.write_text(json.dumps([str(skill_dir), str(skill_file)]), encoding="utf-8")

    targets = InputAdapterService().load_batch(str(manifest))

    assert [target.source_type for target in targets] == [
        SourceType.LOCAL,
        SourceType.SKILL_FILE,
    ]
    assert [target.metadata.name for target in targets] == ["skill-a", "skill-b"]



def test_load_batch_manifest_rejects_non_array_payload(tmp_path: Path) -> None:
    manifest = tmp_path / "batch.json"
    manifest.write_text(json.dumps({"target": "/tmp/foo"}), encoding="utf-8")

    with pytest.raises(ValueError, match="JSON array"):
        InputAdapterService().load_batch(str(manifest))
