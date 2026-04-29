from pathlib import Path

import pytest

from safeskill.models.input_target import InputTarget, SourceType, TargetMetadata



def test_target_metadata_defaults_to_none_fields() -> None:
    metadata = TargetMetadata()

    assert metadata.name is None
    assert metadata.author is None
    assert metadata.platform is None
    assert metadata.version is None



def test_input_target_serializes_path_and_metadata() -> None:
    target = InputTarget(
        source_type=SourceType.LOCAL,
        source="/tmp/example-skill",
        resolved_path=Path("/tmp/example-skill"),
        metadata=TargetMetadata(name="Example Skill", author="alice"),
    )

    dumped = target.model_dump(mode="json")

    assert dumped == {
        "source_type": "local",
        "source": "/tmp/example-skill",
        "resolved_path": "/tmp/example-skill",
        "metadata": {
            "name": "Example Skill",
            "author": "alice",
            "platform": None,
            "version": None,
        },
    }



def test_input_target_rejects_non_absolute_resolved_path() -> None:
    with pytest.raises(ValueError, match="absolute"):
        InputTarget(
            source_type=SourceType.SKILL_FILE,
            source="SKILL.md",
            resolved_path=Path("SKILL.md"),
            metadata=TargetMetadata(),
        )
