from pathlib import Path

from safeskill.models.finding import Finding, Severity, StaticAnalysisReport
from safeskill.models.skill_manifest import SkillManifest
from safeskill.renderers_html import HtmlReportRenderer



def test_html_renderer_formats_summary_and_findings() -> None:
    manifest = SkillManifest(
        source_path=Path("/tmp/SKILL.md"),
        name="demo-skill",
        title="Demo Skill",
        author=None,
        version=None,
        description="demo",
        scripts=[],
        references=[],
        urls=[],
    )
    report = StaticAnalysisReport(
        source_path=Path("/tmp/SKILL.md"),
        findings=[
            Finding(
                rule_id="dangerous-command.rm-rf",
                severity=Severity.CRITICAL,
                category="filesystem",
                confidence="high",
                summary="Detected destructive recursive delete command.",
                evidence="rm -rf /tmp/demo",
                source_excerpt="rm -rf /tmp/demo",
                location="scripts[0]",
            )
        ],
    )

    html = HtmlReportRenderer().render(manifest, report)

    assert "<html" in html
    assert "SafeSkill Risk Report" in html
    assert "Skill: Demo Skill" in html
    assert "Total Findings: 1" in html
    assert "Critical: 1" in html
    assert "dangerous-command.rm-rf" in html
    assert "scripts[0]" in html
