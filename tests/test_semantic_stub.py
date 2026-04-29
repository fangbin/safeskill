from pathlib import Path

from safeskill.models.analysis import AnalysisRequest
from safeskill.models.skill_manifest import SkillManifest
from safeskill.semantic.stub_analyzer import SemanticStubAnalyzer



def test_semantic_stub_returns_named_empty_result() -> None:
    manifest = SkillManifest(
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

    result = SemanticStubAnalyzer().analyze(AnalysisRequest(manifest=manifest))

    assert result.analyzer_name == "semantic-stub"
    assert result.findings == []
