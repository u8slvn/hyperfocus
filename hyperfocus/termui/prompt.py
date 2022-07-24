from __future__ import annotations

from typing import Any

import click

from hyperfocus.termui import icons, style
from hyperfocus.termui.markup import markup


_prompt_prefix = markup.resolve(f"[{style.SUCCESS}]{icons.PROMPT}[/]")


def _prompt_suffix(choice: str):
    return markup.resolve(f" [[{style.INFO}]{choice}[/]]: ")


def confirm(text: str, default: bool | None = None) -> bool:
    choice = "y/n" if default is None else ("Y/n" if default else "y/N")

    return click.confirm(
        text=f"{_prompt_prefix} {markup.resolve(text)}",
        default=default,
        show_default=False,
        prompt_suffix=_prompt_suffix(choice),
    )


def prompt(
    text: str, default: Any | None = None, type: click.ParamType | None = None
) -> Any:
    prompt_suffix = ": " if default is None else _prompt_suffix(default)
    return click.prompt(
        text=f"{_prompt_prefix} {markup.resolve(text)}",
        type=type,
        default=default,
        show_default=False,
        prompt_suffix=prompt_suffix,
    )
