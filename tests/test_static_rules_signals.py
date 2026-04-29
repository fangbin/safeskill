from pathlib import Path

from safeskill.analyzers.static_rules import StaticRuleAnalyzer
from safeskill.models.skill_manifest import ScriptBlock, SkillManifest



def test_analyzer_flags_suspicious_raw_ip_url(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text("# Demo\n", encoding="utf-8")
    manifest = SkillManifest(
        source_path=skill_file.resolve(),
        name="Demo",
        title="Demo",
        author=None,
        version=None,
        description="Download from http://192.168.1.10/payload",
        scripts=[],
        references=[],
        urls=["http://192.168.1.10/payload"],
    )

    report = StaticRuleAnalyzer().analyze(manifest)

    assert report.findings[0].rule_id == "suspicious-url.raw-ip"
    assert report.findings[0].severity == "medium"
    assert report.findings[0].location == "urls[0]"



def test_analyzer_flags_hardcoded_secret_pattern(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text("# Demo\n", encoding="utf-8")
    manifest = SkillManifest(
        source_path=skill_file.resolve(),
        name="Demo",
        title="Demo",
        author=None,
        version=None,
        description=None,
        scripts=[ScriptBlock(language="bash", content='export OPENAI_API_KEY="sk-test-secret"')],
        references=[],
        urls=[],
    )

    report = StaticRuleAnalyzer().analyze(manifest)

    assert report.findings[0].rule_id == "hardcoded-secret.api-key"
    assert report.findings[0].severity == "high"
    assert report.findings[0].location == "scripts[0]"
