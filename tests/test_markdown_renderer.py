from pathlib import Path

from safeskill.models.finding import Finding, Severity, StaticAnalysisReport
from safeskill.models.skill_manifest import SkillManifest
from safeskill.renderers_markdown import MarkdownReportRenderer



def test_markdown_renderer_formats_summary_and_findings() -> None:
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

    markdown = MarkdownReportRenderer().render(manifest, report)

    assert "# SafeSkill Risk Report" in markdown
    assert "## Skill: Demo Skill" in markdown
    assert "Total Findings: 1" in markdown
    assert "Critical: 1" in markdown
    assert "### 1. dangerous-command.rm-rf" in markdown
    assert "Location: `scripts[0]`" in markdown
