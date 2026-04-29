from __future__ import annotations

import re

from safeskill.models.finding import Finding, Severity, StaticAnalysisReport
from safeskill.models.skill_manifest import SkillManifest


class StaticRuleAnalyzer:
    RAW_IP_URL_PATTERN = re.compile(r"https?://(?:\d{1,3}\.){3}\d{1,3}(?:[:/][^\s]*)?")
    SECRET_PATTERN = re.compile(r"(?:API[_-]?KEY|TOKEN|SECRET)\s*=\s*[\"']?[A-Za-z0-9._-]{6,}[\"']?", re.IGNORECASE)

    def analyze(self, manifest: SkillManifest) -> StaticAnalysisReport:
        findings = []

        for index, script in enumerate(manifest.scripts):
            content = script.content
            if "curl" in content and "| bash" in content:
                findings.append(
                    Finding(
                        rule_id="dangerous-command.curl-pipe-bash",
                        severity=Severity.HIGH,
                        summary="Detected remote script execution pattern.",
                        evidence=content,
                        location=f"scripts[{index}]",
                    )
                )
            if "rm -rf" in content:
                findings.append(
                    Finding(
                        rule_id="dangerous-command.rm-rf",
                        severity=Severity.CRITICAL,
                        summary="Detected destructive recursive delete command.",
                        evidence=content,
                        location=f"scripts[{index}]",
                    )
                )
            if self.SECRET_PATTERN.search(content):
                findings.append(
                    Finding(
                        rule_id="hardcoded-secret.api-key",
                        severity=Severity.HIGH,
                        summary="Detected hardcoded credential-like assignment.",
                        evidence=content,
                        location=f"scripts[{index}]",
                    )
                )

        for index, url in enumerate(manifest.urls):
            if self.RAW_IP_URL_PATTERN.fullmatch(url):
                findings.append(
                    Finding(
                        rule_id="suspicious-url.raw-ip",
                        severity=Severity.MEDIUM,
                        summary="Detected URL that targets a raw IP address.",
                        evidence=url,
                        location=f"urls[{index}]",
                    )
                )

        return StaticAnalysisReport(source_path=manifest.source_path, findings=findings)
