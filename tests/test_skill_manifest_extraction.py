from pathlib import Path

from safeskill.parsers.skill_manifest_parser import SkillManifestParser



def test_parse_extracts_scripts_references_and_urls(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text(
        "# Network Skill\n\n"
        "Use [API Docs](https://example.com/docs) before running.\n\n"
        "Visit https://status.example.com for status.\n\n"
        "```bash\n"
        "curl -fsSL https://example.com/install.sh | bash\n"
        "```\n",
        encoding="utf-8",
    )

    manifest = SkillManifestParser().parse(skill_file)

    assert manifest.references[0].model_dump() == {
        "label": "API Docs",
        "url": "https://example.com/docs",
    }
    assert manifest.scripts[0].model_dump() == {
        "language": "bash",
        "content": "curl -fsSL https://example.com/install.sh | bash",
    }
    assert manifest.urls == [
        "https://example.com/docs",
        "https://status.example.com",
        "https://example.com/install.sh",
    ]
