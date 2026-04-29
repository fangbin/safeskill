from __future__ import annotations

from pathlib import Path

from safeskill.terminal_runner import run_command


class GitClient:
    def clone(self, repo_url: str, target_dir: Path) -> None:
        run_command([
            "git",
            "clone",
            "--depth",
            "1",
            repo_url,
            str(target_dir),
        ])
