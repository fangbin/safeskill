from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel, ConfigDict, computed_field

from safeskill.models.finding import Severity, StaticAnalysisReport


class BatchScanReport(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    reports: List[StaticAnalysisReport]

    @computed_field(return_type=int)
    @property
    def total_targets(self) -> int:
        return len(self.reports)

    @computed_field(return_type=dict)
    @property
    def summary(self) -> dict:
        counts = {severity.value: 0 for severity in Severity}
        total_findings = 0
        for report in self.reports:
            total_findings += len(report.findings)
            for finding in report.findings:
                counts[finding.severity] += 1
        return {
            "total_targets": len(self.reports),
            "total_findings": total_findings,
            "by_severity": counts,
        }

    @computed_field(return_type=List[str])
    @property
    def source_paths(self) -> List[str]:
        return [str(Path(report.source_path)) for report in self.reports]
