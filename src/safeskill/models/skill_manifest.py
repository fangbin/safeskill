from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, field_validator


class ScriptBlock(BaseModel):
    language: str
    content: str


class ResourceReference(BaseModel):
    label: str
    url: str


class SkillManifest(BaseModel):
    source_path: Path
    name: Optional[str]
    title: Optional[str]
    author: Optional[str]
    version: Optional[str]
    description: Optional[str]
    scripts: List[ScriptBlock]
    references: List[ResourceReference]
    urls: List[str]

    @field_validator("source_path")
    @classmethod
    def validate_source_path(cls, value: Path) -> Path:
        if not value.is_absolute():
            raise ValueError("source_path must be absolute")
        return value
