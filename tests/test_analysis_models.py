from pathlib import Path

from safeskill.models.analysis import AnalysisRequest, AnalysisResult
from safeskill.models.finding import Finding, Severity
from safeskill.models.skill_manifest import SkillManifest



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



def test_analysis_request_wraps_manifest() -> None:
    manifest = build_manifest()

    request = AnalysisRequest(manifest=manifest)

    assert request.manifest is manifest



def test_analysis_result_serializes_analyzer_name_and_findings() -> None:
    finding = Finding(
        rule_id="demo.rule",
        severity=Severity.LOW,
        category="demo",
        confidence="low",
        summary="demo",
        evidence="demo",
        source_excerpt="demo",
        location="description",
    )
    result = AnalysisResult(analyzer_name="static", findings=[finding])

    assert result.model_dump() == {
        "analyzer_name": "static",
        "findings": [finding.model_dump()],
    }
