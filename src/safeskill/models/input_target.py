from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class SourceType(str, Enum):
    LOCAL = "local"
    SKILL_FILE = "skill_file"
    BATCH = "batch"
    GITHUB = "github"
    BENCHMARK = "benchmark"
    INSTALLED = "installed"


class TargetMetadata(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None


class InputTarget(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    source_type: SourceType
    source: str
    resolved_path: Path
    metadata: TargetMetadata

    @field_validator("resolved_path")
    @classmethod
    def validate_resolved_path(cls, value: Path) -> Path:
        if not value.is_absolute():
            raise ValueError("resolved_path must be absolute")
        return value
