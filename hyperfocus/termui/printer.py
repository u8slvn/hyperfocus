from __future__ import annotations

from typing import cast

import click

from hyperfocus.database.models import Task
from hyperfocus.termui import formatter, style
from hyperfocus.termui.components import UIComponent
from hyperfocus.termui.markup import markup


def echo(text: str | UIComponent, nl: bool = True) -> None:
    if isinstance(text, UIComponent):
        text = cast(str, text.resolve())
    click.echo(markup.resolve(text), nl=nl)


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> None:
    formatted_task = formatter.task(
        task=task, show_details=show_details, show_prefix=show_prefix
    )
    echo(text=formatted_task)


def task_details(task: Task) -> None:
    echo(formatter.task_details(task))


def banner(text: str) -> None:
    echo(f"[{style.BANNER}]> {text}[/]")


def config(config: dict[str, str]) -> None:
    echo(formatter.config(config))
