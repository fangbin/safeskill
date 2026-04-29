from __future__ import annotations

import json

import typer
from typing_extensions import Annotated

from safeskill.adapters.input_adapter import InputAdapterService
from safeskill.analyzers.static_rules import StaticRuleAnalyzer
from safeskill.parsers.skill_manifest_parser import SkillManifestParser

app = typer.Typer(help="SafeSkill command line interface")


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
    report = StaticRuleAnalyzer().analyze(manifest)
    typer.echo(json.dumps(report.model_dump(mode="json"), ensure_ascii=False))
