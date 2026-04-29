from __future__ import annotations

import json
from pathlib import Path
from typing import List

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

        return [self.resolve(str(item)) for item in payload]
