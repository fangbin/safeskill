from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Finding(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    rule_id: str
    severity: Severity
    summary: str
    evidence: str
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
