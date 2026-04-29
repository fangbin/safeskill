from __future__ import annotations

from safeskill.adapters.input_adapter import InputAdapterService
from safeskill.analyzers.static_rules import StaticRuleAnalyzer
from safeskill.github_fetcher import GitHubSkillFetcher
from safeskill.models.batch_scan import BatchScanReport
from safeskill.models.input_target import InputTarget, SourceType
from safeskill.parsers.skill_manifest_parser import SkillManifestParser
from safeskill.pipeline.analysis_pipeline import AnalysisPipeline
from safeskill.semantic.stub_analyzer import SemanticStubAnalyzer


class BatchScanService:
    def __init__(
        self,
        input_adapter: InputAdapterService | None = None,
        parser: SkillManifestParser | None = None,
        pipeline: AnalysisPipeline | None = None,
        github_fetcher: GitHubSkillFetcher | None = None,
    ) -> None:
        self.input_adapter = input_adapter or InputAdapterService()
        self.parser = parser or SkillManifestParser()
        self.pipeline = pipeline or AnalysisPipeline(
            analyzers=[
                StaticRuleAnalyzer(),
                SemanticStubAnalyzer(),
            ]
        )
        self.github_fetcher = github_fetcher or GitHubSkillFetcher()

    def scan_manifest(self, manifest_path: str) -> BatchScanReport:
        targets = self.input_adapter.load_batch(manifest_path)
        reports = []
        for target in targets:
            manifest = self.parser.parse(self._resolve_target_path(target))
            reports.append(self.pipeline.run(manifest))
        return BatchScanReport(reports=reports)

    def _resolve_target_path(self, target: InputTarget):
        if target.source_type == SourceType.GITHUB.value:
            return self.github_fetcher.fetch(target.source)
        return target.resolved_path
