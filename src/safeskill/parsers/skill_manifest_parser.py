from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Optional

from safeskill.models.skill_manifest import ResourceReference, ScriptBlock, SkillManifest


class SkillManifestParser:
    FRONTMATTER_CLOSING = "\n---\n"
    TITLE_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)
    LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    CODE_BLOCK_PATTERN = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)
    URL_PATTERN = re.compile(r"https?://[^\s)]+")

    def parse_path(self, target: str) -> SkillManifest:
        return self.parse(Path(target))

    def parse(self, target: Path) -> SkillManifest:
        resolved = target.expanduser().resolve()
        skill_file = self._resolve_skill_file(resolved)
        raw_text = skill_file.read_text(encoding="utf-8")
        metadata, body = self._split_frontmatter(raw_text)
        title = self._extract_title(body)
        description = self._extract_description(body)
        name = metadata.get("name") or title
        references = self._extract_references(body)
        scripts = self._extract_scripts(body)
        urls = self._extract_urls(body)

        return SkillManifest(
            source_path=skill_file,
            name=name,
            title=title,
            author=metadata.get("author"),
            version=metadata.get("version"),
            description=description,
            scripts=scripts,
            references=references,
            urls=urls,
        )

    def _resolve_skill_file(self, resolved: Path) -> Path:
        if resolved.is_dir():
            candidate = resolved / "SKILL.md"
            if candidate.is_file():
                return candidate.resolve()
        elif resolved.is_file() and resolved.name == "SKILL.md":
            return resolved

        raise ValueError(f"Unsupported skill target: {resolved}")

    def _split_frontmatter(self, raw_text: str) -> tuple[Dict[str, str], str]:
        if not raw_text.startswith("---\n"):
            return {}, raw_text

        closing = raw_text.find(self.FRONTMATTER_CLOSING, 4)
        if closing == -1:
            return {}, raw_text

        frontmatter = raw_text[4:closing]
        body = raw_text[closing + len(self.FRONTMATTER_CLOSING) :]
        metadata: Dict[str, str] = {}
        for line in frontmatter.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
        return metadata, body

    def _extract_title(self, body: str) -> Optional[str]:
        match = self.TITLE_PATTERN.search(body)
        if match:
            return match.group(1).strip()
        return None

    def _extract_description(self, body: str) -> Optional[str]:
        lines = body.splitlines()
        after_title = False
        for line in lines:
            stripped = line.strip()
            if not after_title and stripped.startswith("# "):
                after_title = True
                continue
            if after_title and stripped:
                return stripped
        return None

    def _extract_references(self, body: str) -> list[ResourceReference]:
        return [
            ResourceReference(label=label.strip(), url=url.strip())
            for label, url in self.LINK_PATTERN.findall(body)
        ]

    def _extract_scripts(self, body: str) -> list[ScriptBlock]:
        scripts = []
        for language, content in self.CODE_BLOCK_PATTERN.findall(body):
            scripts.append(
                ScriptBlock(language=language.strip(), content=content.strip())
            )
        return scripts

    def _extract_urls(self, body: str) -> list[str]:
        seen = []
        for url in self.URL_PATTERN.findall(body):
            if url not in seen:
                seen.append(url)
        return seen
