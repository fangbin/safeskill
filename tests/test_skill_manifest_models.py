from pathlib import Path

import pytest

from safeskill.models.skill_manifest import ResourceReference, ScriptBlock, SkillManifest



def test_script_block_and_reference_serialize_cleanly() -> None:
    script = ScriptBlock(language="bash", content="echo hello")
    reference = ResourceReference(label="Docs", url="https://example.com/docs")

    assert script.model_dump() == {"language": "bash", "content": "echo hello"}
    assert reference.model_dump() == {"label": "Docs", "url": "https://example.com/docs"}



def test_skill_manifest_requires_absolute_source_path() -> None:
    with pytest.raises(ValueError, match="absolute"):
        SkillManifest(
            source_path=Path("SKILL.md"),
            name="Demo Skill",
            title="Demo Skill",
            author=None,
            version=None,
            description="desc",
            scripts=[],
            references=[],
            urls=[],
        )
