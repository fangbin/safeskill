from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse
from typing import Any, List

from safeskill.models.input_target import InputTarget, SourceType, TargetMetadata


class InputAdapterService:
    def resolve(self, raw_target: str) -> InputTarget:
        candidate = Path(raw_target).expanduser()
        resolved = candidate.resolve()

        if resolved.is_dir():
            return InputTarget(
                source_type=SourceType.LOCAL,
                source=raw_target,
                resolved_path=resolved,
                metadata=TargetMetadata(name=resolved.name),
            )

        if resolved.is_file() and resolved.name == "SKILL.md":
            return InputTarget(
                source_type=SourceType.SKILL_FILE,
                source=raw_target,
                resolved_path=resolved,
                metadata=TargetMetadata(name=resolved.parent.name),
            )

        raise ValueError(f"Unsupported input target: {raw_target}")

    def load_batch(self, manifest_path: str) -> List[InputTarget]:
        manifest = Path(manifest_path).expanduser().resolve()
        if not manifest.is_file():
            raise ValueError(f"Batch manifest not found: {manifest_path}")

        payload = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Batch manifest must contain a JSON array")

        return [self._resolve_batch_item(item) for item in payload]

    def _resolve_batch_item(self, item: Any) -> InputTarget:
        if isinstance(item, str):
            return self.resolve(item)
        if isinstance(item, dict):
            return self._resolve_structured_target(item)
        raise ValueError(f"Unsupported batch item: {item!r}")

    def _resolve_structured_target(self, item: dict[str, Any]) -> InputTarget:
        target_type = item.get("type")
        source = item.get("source")
        if target_type != SourceType.GITHUB.value:
            raise ValueError(f"Unsupported structured batch target type: {target_type}")
        if not isinstance(source, str) or not source:
            raise ValueError("Structured batch target must include a non-empty source")

        parsed = urlparse(source)
        repo_path = parsed.path.strip("/") or "unknown/unknown"
        resolved_path = Path("/virtual/github") / repo_path
        return InputTarget(
            source_type=SourceType.GITHUB,
            source=source,
            resolved_path=resolved_path,
            metadata=TargetMetadata(
                name=item.get("name"),
                author=item.get("author"),
                platform=item.get("platform"),
                version=item.get("version"),
            ),
        )
