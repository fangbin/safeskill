from __future__ import annotations

from safeskill.adapters.input_adapter import InputAdapterService
from safeskill.analyzers.static_rules import StaticRuleAnalyzer
from safeskill.models.batch_scan import BatchScanReport
from safeskill.parsers.skill_manifest_parser import SkillManifestParser
from safeskill.pipeline.analysis_pipeline import AnalysisPipeline
from safeskill.semantic.stub_analyzer import SemanticStubAnalyzer


class BatchScanService:
    def __init__(self) -> None:
        self.input_adapter = InputAdapterService()
        self.parser = SkillManifestParser()
        self.pipeline = AnalysisPipeline(
            analyzers=[
                StaticRuleAnalyzer(),
                SemanticStubAnalyzer(),
            ]
        )

    def scan_manifest(self, manifest_path: str) -> BatchScanReport:
        targets = self.input_adapter.load_batch(manifest_path)
        reports = []
        for target in targets:
            manifest = self.parser.parse(target.resolved_path)
            reports.append(self.pipeline.run(manifest))
        return BatchScanReport(reports=reports)
