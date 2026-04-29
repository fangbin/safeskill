from pathlib import Path

from safeskill.parsers.skill_manifest_parser import SkillManifestParser



def test_parse_skill_file_extracts_title_description_and_metadata(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text(
        "---\n"
        "name: Demo Skill\n"
        "author: alice\n"
        "version: 1.2.3\n"
        "---\n\n"
        "# Demo Skill\n\n"
        "A short skill description.\n",
        encoding="utf-8",
    )

    manifest = SkillManifestParser().parse(skill_file)

    assert manifest.source_path == skill_file.resolve()
    assert manifest.name == "Demo Skill"
    assert manifest.title == "Demo Skill"
    assert manifest.author == "alice"
    assert manifest.version == "1.2.3"
    assert manifest.description == "A short skill description."



def test_parse_skill_directory_reads_skill_md(tmp_path: Path) -> None:
    skill_dir = tmp_path / "demo"
    skill_dir.mkdir()
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text("# Directory Skill\n", encoding="utf-8")

    manifest = SkillManifestParser().parse(skill_dir)

    assert manifest.source_path == skill_file.resolve()
    assert manifest.title == "Directory Skill"
    assert manifest.name == "Directory Skill"
