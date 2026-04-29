from __future__ import annotations

import json
from pathlib import Path

import typer
from typing_extensions import Annotated

from safeskill.adapters.input_adapter import InputAdapterService
from safeskill.analyzers.static_rules import StaticRuleAnalyzer
from safeskill.github_fetcher import GitHubSkillFetcher
from safeskill.parsers.skill_manifest_parser import SkillManifestParser
from safeskill.pipeline.analysis_pipeline import AnalysisPipeline
from safeskill.pipeline.batch_scan_service import BatchScanService
from safeskill.renderers_html import HtmlReportRenderer
from safeskill.renderers_markdown import MarkdownReportRenderer
from safeskill.semantic.stub_analyzer import SemanticStubAnalyzer

app = typer.Typer(help="SafeSkill command line interface")


def build_default_pipeline() -> AnalysisPipeline:
    return AnalysisPipeline(
        analyzers=[
            StaticRuleAnalyzer(),
            SemanticStubAnalyzer(),
        ]
    )


def build_batch_scan_service() -> BatchScanService:
    return BatchScanService(github_fetcher=GitHubSkillFetcher())


def write_output(output_path: str, content: str) -> str:
    output = Path(output_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return str(output)


@app.command("inspect-input")
def inspect_input(target: Annotated[str, typer.Argument()]) -> None:
    resolved = InputAdapterService().resolve(target)
    typer.echo(json.dumps(resolved.model_dump(mode="json"), ensure_ascii=False))


@app.command("parse-manifest")
def parse_manifest(target: Annotated[str, typer.Argument()]) -> None:
    manifest = SkillManifestParser().parse_path(target)
    typer.echo(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False))


@app.command("scan")
def scan(target: Annotated[str, typer.Argument()]) -> None:
    manifest = SkillManifestParser().parse_path(target)
    report = build_default_pipeline().run(manifest)
    typer.echo(json.dumps(report.model_dump(mode="json"), ensure_ascii=False))


@app.command("scan-github")
def scan_github(repo_url: Annotated[str, typer.Argument()]) -> None:
    repo_dir = GitHubSkillFetcher().fetch(repo_url)
    manifest = SkillManifestParser().parse(repo_dir)
    report = build_default_pipeline().run(manifest)
    typer.echo(json.dumps(report.model_dump(mode="json"), ensure_ascii=False))


@app.command("scan-batch")
def scan_batch(manifest_path: Annotated[str, typer.Argument()]) -> None:
    report = build_batch_scan_service().scan_manifest(manifest_path)
    typer.echo(json.dumps(report.model_dump(mode="json"), ensure_ascii=False))


@app.command("report-markdown")
def report_markdown(
    target: Annotated[str, typer.Argument()],
    output_path: Annotated[str, typer.Argument()],
) -> None:
    manifest = SkillManifestParser().parse_path(target)
    report = build_default_pipeline().run(manifest)
    markdown = MarkdownReportRenderer().render(manifest, report)
    typer.echo(write_output(output_path, markdown))


@app.command("report-html")
def report_html(
    target: Annotated[str, typer.Argument()],
    output_path: Annotated[str, typer.Argument()],
) -> None:
    manifest = SkillManifestParser().parse_path(target)
    report = build_default_pipeline().run(manifest)
    html = HtmlReportRenderer().render(manifest, report)
    typer.echo(write_output(output_path, html))
