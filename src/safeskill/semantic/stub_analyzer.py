from __future__ import annotations

from safeskill.models.analysis import AnalysisRequest, AnalysisResult
from safeskill.models.finding import Finding, Severity


class SemanticStubAnalyzer:
    name = "semantic-stub"

    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        manifest = request.manifest
        findings = []
        text_parts = [manifest.title or "", manifest.description or ""]
        text_parts.extend(script.content for script in manifest.scripts)
        text_parts.extend(manifest.urls)
        corpus = "\n".join(text_parts).lower()

        if (
            "ignore all previous instructions" in corpus
            or "disable safety checks" in corpus
        ):
            findings.append(
                Finding(
                    rule_id="semantic.prompt-injection.override-safety",
                    severity=Severity.HIGH,
                    category="prompt-injection",
                    confidence="medium",
                    summary="Detected language attempting to override prior instructions or disable safeguards.",
                    evidence=manifest.description or manifest.title or "",
                    source_excerpt=manifest.description or manifest.title or "",
                    location="description",
                )
            )

        if (
            "collect environment credentials" in corpus
            or ("printenv" in corpus and "curl -x post" in corpus)
            or ("printenv" in corpus and "remote endpoint" in corpus)
            or ("printenv" in corpus and "upload" in corpus)
        ):
            evidence = next((script.content for script in manifest.scripts if "printenv" in script.content.lower()), manifest.description or "")
            findings.append(
                Finding(
                    rule_id="semantic.secret-exfiltration.remote-upload",
                    severity=Severity.CRITICAL,
                    category="exfiltration",
                    confidence="medium",
                    summary="Detected language indicating collection of environment secrets for remote upload.",
                    evidence=evidence,
                    source_excerpt=evidence,
                    location="scripts[0]" if manifest.scripts else "description",
                )
            )

        return AnalysisResult(analyzer_name=self.name, findings=findings)
