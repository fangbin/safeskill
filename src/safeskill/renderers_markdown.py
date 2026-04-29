from __future__ import annotations

from safeskill.models.finding import StaticAnalysisReport
from safeskill.models.skill_manifest import SkillManifest


class MarkdownReportRenderer:
    def render(self, manifest: SkillManifest, report: StaticAnalysisReport) -> str:
        lines = [
            "# SafeSkill Risk Report",
            "",
            f"## Skill: {manifest.title or manifest.name or report.source_path.name}",
            "",
            f"- Source: `{report.source_path}`",
            f"- Total Findings: {report.summary['total_findings']}",
            f"- Critical: {report.summary['by_severity']['critical']}",
            f"- High: {report.summary['by_severity']['high']}",
            f"- Medium: {report.summary['by_severity']['medium']}",
            f"- Low: {report.summary['by_severity']['low']}",
            "",
            "## Findings",
            "",
        ]

        if not report.findings:
            lines.extend([
                "No findings detected.",
                "",
            ])
            return "\n".join(lines)

        for index, finding in enumerate(report.findings, start=1):
            lines.extend([
                f"### {index}. {finding.rule_id}",
                "",
                f"- Severity: {finding.severity}",
                f"- Category: {finding.category}",
                f"- Confidence: {finding.confidence}",
                f"- Location: `{finding.location}`",
                f"- Summary: {finding.summary}",
                f"- Evidence: `{finding.evidence}`",
                "",
            ])

        return "\n".join(lines)
