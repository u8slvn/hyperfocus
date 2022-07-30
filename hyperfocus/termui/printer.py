from __future__ import annotations

from typing import cast

import click

from hyperfocus.termui import formatter, style
from hyperfocus.termui.components import UIComponent
from hyperfocus.termui.markup import markup


def echo(text: str | UIComponent, nl: bool = True) -> None:
    if isinstance(text, UIComponent):
        text = cast(str, text.resolve())
    click.echo(markup.resolve(text), nl=nl)


def banner(text: str) -> None:
    echo(f"[{style.BANNER}]> {text}[/]")


def config(config: dict[str, str]) -> None:
    echo(formatter.config(config))
