from __future__ import annotations

import json

import typer
from typing_extensions import Annotated

from safeskill.adapters.input_adapter import InputAdapterService

app = typer.Typer(help="SafeSkill command line interface")


@app.command("inspect-input")
def inspect_input(target: Annotated[str, typer.Argument()]) -> None:
    resolved = InputAdapterService().resolve(target)
    typer.echo(json.dumps(resolved.model_dump(mode="json"), ensure_ascii=False))
