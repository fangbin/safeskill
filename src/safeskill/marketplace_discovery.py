from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MarketplaceDiscoveryService:
    def discover(self, manifest_path: str) -> list[dict[str, str]]:
        manifest = Path(manifest_path).expanduser().resolve()
        if not manifest.is_file():
            raise ValueError(f"Marketplace export not found: {manifest_path}")

        payload = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Marketplace export must contain a JSON array")

        discovered: list[dict[str, str]] = []
        for item in payload:
            normalized = self._normalize_entry(item)
            if normalized is not None:
                discovered.append(normalized)
        return discovered

    def _normalize_entry(self, item: Any) -> dict[str, str] | None:
        if not isinstance(item, dict):
            return None

        repo_url = item.get("repo_url")
        if not isinstance(repo_url, str) or not repo_url.startswith("https://github.com/"):
            return None

        return {
            "type": "github",
            "source": repo_url,
            "name": str(item.get("name") or ""),
            "platform": str(item.get("marketplace") or "unknown"),
        }
