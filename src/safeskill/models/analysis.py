from __future__ import annotations

from pydantic import BaseModel

from safeskill.models.finding import Finding
from safeskill.models.skill_manifest import SkillManifest


class AnalysisRequest(BaseModel):
    manifest: SkillManifest


class AnalysisResult(BaseModel):
    analyzer_name: str
    findings: list[Finding]
