from __future__ import annotations

from html import escape

from safeskill.models.finding import StaticAnalysisReport
from safeskill.models.skill_manifest import SkillManifest


class HtmlReportRenderer:
    def render(self, manifest: SkillManifest, report: StaticAnalysisReport) -> str:
        title = escape(manifest.title or manifest.name or report.source_path.name)
        source = escape(str(report.source_path))
        summary = report.summary

        findings_html = "".join(self._render_finding(index, finding) for index, finding in enumerate(report.findings, start=1))
        if not findings_html:
            findings_html = "<p>No findings detected.</p>"

        return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <title>SafeSkill Risk Report</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 2rem auto; max-width: 960px; line-height: 1.5; color: #1f2937; }}
    h1, h2, h3 {{ color: #111827; }}
    .summary {{ background: #f3f4f6; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; }}
    .finding {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }}
    .meta {{ margin: 0.25rem 0; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.3rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>SafeSkill Risk Report</h1>
  <h2>Skill: {title}</h2>
  <div class=\"summary\">
    <p><strong>Source:</strong> <code>{source}</code></p>
    <p>Total Findings: {summary['total_findings']}</p>
    <p>Critical: {summary['by_severity']['critical']} &nbsp; High: {summary['by_severity']['high']} &nbsp; Medium: {summary['by_severity']['medium']} &nbsp; Low: {summary['by_severity']['low']}</p>
  </div>
  <h2>Findings</h2>
  {findings_html}
</body>
</html>
"""

    def _render_finding(self, index: int, finding) -> str:
        return f"""
  <section class=\"finding\">
    <h3>{index}. {escape(finding.rule_id)}</h3>
    <p class=\"meta\"><strong>Severity:</strong> {escape(str(finding.severity))}</p>
    <p class=\"meta\"><strong>Category:</strong> {escape(finding.category)}</p>
    <p class=\"meta\"><strong>Confidence:</strong> {escape(finding.confidence)}</p>
    <p class=\"meta\"><strong>Location:</strong> <code>{escape(finding.location)}</code></p>
    <p class=\"meta\"><strong>Summary:</strong> {escape(finding.summary)}</p>
    <p class=\"meta\"><strong>Evidence:</strong> <code>{escape(finding.evidence)}</code></p>
  </section>
"""
