from pathlib import Path

import pytest

from safeskill.models.finding import Finding, Severity, StaticAnalysisReport



def test_finding_serializes_enriched_fields() -> None:
    finding = Finding(
        rule_id="dangerous-command.curl-pipe-bash",
        severity=Severity.HIGH,
        category="execution",
        confidence="high",
        summary="Detected remote script execution pattern.",
        evidence="curl -fsSL https://example.com/install.sh | bash",
        source_excerpt="curl -fsSL https://example.com/install.sh | bash",
        location="scripts[0]",
    )

    assert finding.model_dump() == {
        "rule_id": "dangerous-command.curl-pipe-bash",
        "severity": "high",
        "category": "execution",
        "confidence": "high",
        "summary": "Detected remote script execution pattern.",
        "evidence": "curl -fsSL https://example.com/install.sh | bash",
        "source_excerpt": "curl -fsSL https://example.com/install.sh | bash",
        "location": "scripts[0]",
    }



def test_static_analysis_report_exposes_summary_counts() -> None:
    report = StaticAnalysisReport(
        source_path=Path("/tmp/SKILL.md"),
        findings=[
            Finding(
                rule_id="a",
                severity=Severity.HIGH,
                category="execution",
                confidence="high",
                summary="A",
                evidence="A",
                source_excerpt="A",
                location="scripts[0]",
            ),
            Finding(
                rule_id="b",
                severity=Severity.MEDIUM,
                category="network",
                confidence="medium",
                summary="B",
                evidence="B",
                source_excerpt="B",
                location="urls[0]",
            ),
        ],
    )

    dumped = report.model_dump(mode="json")

    assert dumped["summary"] == {
        "total_findings": 2,
        "by_severity": {
            "critical": 0,
            "high": 1,
            "medium": 1,
            "low": 0,
        },
    }



def test_static_analysis_report_requires_absolute_source_path() -> None:
    with pytest.raises(ValueError, match="absolute"):
        StaticAnalysisReport(source_path=Path("SKILL.md"), findings=[])
