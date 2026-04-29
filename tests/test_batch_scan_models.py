from pathlib import Path

from safeskill.models.finding import Finding, Severity, StaticAnalysisReport
from safeskill.models.batch_scan import BatchScanReport



def test_batch_scan_report_aggregates_target_and_finding_counts() -> None:
    report_a = StaticAnalysisReport(
        source_path=Path("/tmp/a/SKILL.md"),
        findings=[
            Finding(
                rule_id="a",
                severity=Severity.HIGH,
                category="execution",
                confidence="high",
                summary="a",
                evidence="a",
                source_excerpt="a",
                location="scripts[0]",
            )
        ],
    )
    report_b = StaticAnalysisReport(
        source_path=Path("/tmp/b/SKILL.md"),
        findings=[
            Finding(
                rule_id="b",
                severity=Severity.MEDIUM,
                category="network",
                confidence="high",
                summary="b",
                evidence="b",
                source_excerpt="b",
                location="urls[0]",
            )
        ],
    )

    batch = BatchScanReport(reports=[report_a, report_b])

    assert batch.total_targets == 2
    assert batch.summary["total_findings"] == 2
    assert batch.summary["by_severity"]["high"] == 1
    assert batch.summary["by_severity"]["medium"] == 1
    assert batch.source_paths == ["/tmp/a/SKILL.md", "/tmp/b/SKILL.md"]
