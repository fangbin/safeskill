# SafeSkill Iteration 10 Plan

## Iteration 10: Semantic analyzer prototype

Goal: replace the placeholder semantic stub with a prototype semantic analyzer that detects high-level malicious instruction patterns beyond simple command signatures.

Architecture:
- Keep the existing analyzer interface and pipeline.
- Implement a lightweight heuristic semantic analyzer over manifest title, description, URLs, and script text.
- Detect prompt-injection style intent such as disabling safeguards or exfiltrating secrets.

Scope:
1. Add failing tests for semantic findings.
2. Implement semantic analyzer prototype.
3. Replace stub usage in CLI/pipeline with the real semantic analyzer.
4. Run targeted tests, then full suite.

Out of scope:
- LLM-based semantic classification
- Multi-language NLP
- Confidence calibration beyond fixed heuristics
