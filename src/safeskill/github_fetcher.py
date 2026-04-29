from __future__ import annotations

import tempfile
from pathlib import Path

from safeskill.terminal_git import GitClient


class GitHubSkillFetcher:
    def __init__(self, git_client: GitClient | None = None) -> None:
        self.git_client = git_client or GitClient()

    def fetch(self, repo_url: str) -> Path:
        target_dir = Path(tempfile.mkdtemp(prefix="safeskill-github-"))
        self.git_client.clone(repo_url, target_dir)
        return target_dir
