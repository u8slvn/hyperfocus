from __future__ import annotations

from typing import Generator, cast

import click

from hyperfocus.termui import formatter, style
from hyperfocus.termui.components import UIComponent
from hyperfocus.termui.markup import markup


def echo(text: str | UIComponent, nl: bool = True) -> None:
    if isinstance(text, UIComponent):
        text = cast(str, text.resolve())
    click.echo(markup.resolve(text), nl=nl)


def pager_echo(text: Generator) -> None:
    def echo(text: Generator) -> Generator[str, None, None]:
        for line in text:
            yield markup.resolve(line)

    click.echo_via_pager(echo(text))


def banner(text: str) -> None:
    # TODO: move to components
    echo(f"[{style.BANNER}]> {text}[/]")


def config(config: dict[str, str]) -> None:
    # TODO: move to components
    echo(formatter.config(config))
