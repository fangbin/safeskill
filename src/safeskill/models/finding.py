from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, computed_field, field_validator


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Finding(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    rule_id: str
    severity: Severity
    category: str
    confidence: str
    summary: str
    evidence: str
    source_excerpt: str
    location: str


class StaticAnalysisReport(BaseModel):
    source_path: Path
    findings: List[Finding]

    @field_validator("source_path")
    @classmethod
    def validate_source_path(cls, value: Path) -> Path:
        if not value.is_absolute():
            raise ValueError("source_path must be absolute")
        return value

    @computed_field(return_type=Dict[str, object])
    @property
    def summary(self) -> Dict[str, object]:
        counts = {severity.value: 0 for severity in Severity}
        for finding in self.findings:
            counts[finding.severity] += 1
        return {
            "total_findings": len(self.findings),
            "by_severity": counts,
        }
