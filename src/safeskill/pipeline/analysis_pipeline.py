from __future__ import annotations

from typing import Protocol

from safeskill.models.analysis import AnalysisRequest, AnalysisResult
from safeskill.models.finding import StaticAnalysisReport
from safeskill.models.skill_manifest import SkillManifest


class Analyzer(Protocol):
    name: str

    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        ...


class AnalysisPipeline:
    def __init__(self, analyzers: list[Analyzer]) -> None:
        self.analyzers = analyzers

    def run(self, manifest: SkillManifest) -> StaticAnalysisReport:
        request = AnalysisRequest(manifest=manifest)
        findings = []
        for analyzer in self.analyzers:
            result = analyzer.analyze(request)
            findings.extend(result.findings)
        return StaticAnalysisReport(source_path=manifest.source_path, findings=findings)
