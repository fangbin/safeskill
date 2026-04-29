from __future__ import annotations

from safeskill.models.analysis import AnalysisRequest, AnalysisResult


class SemanticStubAnalyzer:
    name = "semantic-stub"

    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        return AnalysisResult(analyzer_name=self.name, findings=[])
