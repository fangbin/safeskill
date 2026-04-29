from pathlib import Path

from safeskill.pipeline.analysis_pipeline import AnalysisPipeline
from safeskill.models.analysis import AnalysisRequest, AnalysisResult
from safeskill.models.finding import Finding, Severity
from safeskill.models.skill_manifest import SkillManifest


class FakeAnalyzer:
    def __init__(self, name: str, findings: list[Finding]) -> None:
        self.name = name
        self._findings = findings

    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        return AnalysisResult(analyzer_name=self.name, findings=self._findings)



def build_manifest() -> SkillManifest:
    return SkillManifest(
        source_path=Path("/tmp/SKILL.md"),
        name="Demo",
        title="Demo",
        author=None,
        version=None,
        description=None,
        scripts=[],
        references=[],
        urls=[],
    )



def test_pipeline_merges_findings_from_multiple_analyzers() -> None:
    manifest = build_manifest()
    finding_a = Finding(
        rule_id="a",
        severity=Severity.LOW,
        category="demo",
        confidence="low",
        summary="a",
        evidence="a",
        source_excerpt="a",
        location="description",
    )
    finding_b = Finding(
        rule_id="b",
        severity=Severity.HIGH,
        category="demo",
        confidence="high",
        summary="b",
        evidence="b",
        source_excerpt="b",
        location="scripts[0]",
    )
    pipeline = AnalysisPipeline(
        analyzers=[
            FakeAnalyzer("static", [finding_a]),
            FakeAnalyzer("semantic", [finding_b]),
        ]
    )

    report = pipeline.run(manifest)

    assert [finding.rule_id for finding in report.findings] == ["a", "b"]
    assert report.summary["total_findings"] == 2
