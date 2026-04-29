from pathlib import Path

from safeskill.github_fetcher import GitHubSkillFetcher


class FakeGitClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Path]] = []

    def clone(self, repo_url: str, target_dir: Path) -> None:
        self.calls.append((repo_url, target_dir))
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "SKILL.md").write_text("# Demo\n", encoding="utf-8")



def test_github_skill_fetcher_clones_repo_into_temp_directory() -> None:
    git_client = FakeGitClient()

    repo_dir = GitHubSkillFetcher(git_client=git_client).fetch("https://github.com/example/demo-skill")

    assert len(git_client.calls) == 1
    repo_url, target_dir = git_client.calls[0]
    assert repo_url == "https://github.com/example/demo-skill"
    assert repo_dir == target_dir
    assert repo_dir.is_dir()
    assert (repo_dir / "SKILL.md").is_file()
