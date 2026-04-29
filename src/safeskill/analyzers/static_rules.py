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
                findings.append(self._make_finding(
                    rule_id="dangerous-command.curl-pipe-bash",
                    severity=Severity.HIGH,
                    category="execution",
                    confidence="high",
                    summary="Detected remote script execution pattern.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))
            if "rm -rf" in content:
                findings.append(self._make_finding(
                    rule_id="dangerous-command.rm-rf",
                    severity=Severity.CRITICAL,
                    category="filesystem",
                    confidence="high",
                    summary="Detected destructive recursive delete command.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))
            if "wget" in content and "| sh" in content:
                findings.append(self._make_finding(
                    rule_id="dangerous-command.wget-pipe-sh",
                    severity=Severity.HIGH,
                    category="execution",
                    confidence="high",
                    summary="Detected wget pipe-to-shell execution pattern.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))
            if "chmod 777" in content:
                findings.append(self._make_finding(
                    rule_id="dangerous-command.chmod-777",
                    severity=Severity.MEDIUM,
                    category="permissions",
                    confidence="high",
                    summary="Detected overly permissive chmod pattern.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))
            if "sudo" in content:
                findings.append(self._make_finding(
                    rule_id="dangerous-command.sudo",
                    severity=Severity.MEDIUM,
                    category="privilege",
                    confidence="medium",
                    summary="Detected privileged execution request.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))
            if "bash -c" in content and "$(curl" in content:
                findings.append(self._make_finding(
                    rule_id="dangerous-command.bash-c-curl",
                    severity=Severity.HIGH,
                    category="execution",
                    confidence="high",
                    summary="Detected subshell curl execution pattern.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))
            if "nc " in content and " -e " in content:
                findings.append(self._make_finding(
                    rule_id="dangerous-command.netcat-shell",
                    severity=Severity.HIGH,
                    category="network",
                    confidence="high",
                    summary="Detected netcat shell execution pattern.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))
            if self.SECRET_PATTERN.search(content):
                findings.append(self._make_finding(
                    rule_id="hardcoded-secret.api-key",
                    severity=Severity.HIGH,
                    category="secret",
                    confidence="medium",
                    summary="Detected hardcoded credential-like assignment.",
                    evidence=content,
                    location=f"scripts[{index}]",
                ))

        for index, url in enumerate(manifest.urls):
            if self.RAW_IP_URL_PATTERN.fullmatch(url):
                findings.append(self._make_finding(
                    rule_id="suspicious-url.raw-ip",
                    severity=Severity.MEDIUM,
                    category="network",
                    confidence="high",
                    summary="Detected URL that targets a raw IP address.",
                    evidence=url,
                    location=f"urls[{index}]",
                ))

        return StaticAnalysisReport(source_path=manifest.source_path, findings=findings)

    def _make_finding(
        self,
        *,
        rule_id: str,
        severity: Severity,
        category: str,
        confidence: str,
        summary: str,
        evidence: str,
        location: str,
    ) -> Finding:
        return Finding(
            rule_id=rule_id,
            severity=severity,
            category=category,
            confidence=confidence,
            summary=summary,
            evidence=evidence,
            source_excerpt=evidence,
            location=location,
        )
