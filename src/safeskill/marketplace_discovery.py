from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urljoin


class MarketplaceDiscoveryService:
    SMITHERY_LISTING_URL = "https://smithery.ai/skills"
    SMITHERY_LINK_PATTERN = re.compile(r'href=["\'](/skills/[^"\'#?]+/[^"\'#?]+)["\']')

    def discover(self, source: str) -> list[dict[str, str]]:
        if source.startswith("http://") or source.startswith("https://"):
            return self._discover_live_source(source)

        manifest = Path(source).expanduser().resolve()
        if not manifest.is_file():
            raise ValueError(f"Marketplace export not found: {source}")

        payload = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Marketplace export must contain a JSON array")

        discovered: list[dict[str, str]] = []
        for item in payload:
            normalized = self._normalize_entry(item)
            if normalized is not None:
                discovered.append(normalized)
        return discovered

    def _discover_live_source(self, source: str) -> list[dict[str, str]]:
        normalized_source = source.rstrip("/")
        if normalized_source != self.SMITHERY_LISTING_URL:
            raise ValueError(f"Unsupported marketplace source: {source}")

        html = self._fetch_text(source)
        discovered = []
        seen = set()
        for href in self.SMITHERY_LINK_PATTERN.findall(html):
            full_url = urljoin(self.SMITHERY_LISTING_URL, href)
            name = href.removeprefix("/skills/")
            if full_url in seen:
                continue
            seen.add(full_url)
            discovered.append(
                {
                    "marketplace": "smithery",
                    "name": name,
                    "marketplace_url": full_url,
                }
            )
        return discovered

    def _fetch_text(self, url: str) -> str:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", "ignore")

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
