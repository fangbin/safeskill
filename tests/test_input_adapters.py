from pathlib import Path

import pytest

from safeskill.adapters.input_adapter import InputAdapterService
from safeskill.models.input_target import SourceType



def test_resolve_directory_target_returns_local_input_target(tmp_path: Path) -> None:
    skill_dir = tmp_path / "demo-skill"
    skill_dir.mkdir()

    target = InputAdapterService().resolve(str(skill_dir))

    assert target.source_type == SourceType.LOCAL
    assert target.source == str(skill_dir)
    assert target.resolved_path == skill_dir.resolve()
    assert target.metadata.model_dump() == {
        "name": "demo-skill",
        "author": None,
        "platform": None,
        "version": None,
    }



def test_resolve_skill_file_returns_skill_file_target(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text("# Example\n", encoding="utf-8")

    target = InputAdapterService().resolve(str(skill_file))

    assert target.source_type == SourceType.SKILL_FILE
    assert target.source == str(skill_file)
    assert target.resolved_path == skill_file.resolve()
    assert target.metadata.name == tmp_path.name



def test_resolve_rejects_non_skill_file_inputs(tmp_path: Path) -> None:
    other_file = tmp_path / "notes.md"
    other_file.write_text("nope", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported input target"):
        InputAdapterService().resolve(str(other_file))
