from __future__ import annotations

import click

from hyperfocus.console.core.parameters import NotRequired, NotRequiredIf
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import printer
from hyperfocus.termui.components import SuccessNotification


@click.command(help="Get and set options")
@click.argument(
    "option",
    cls=NotRequiredIf,
    not_required_if=["list"],
    metavar="<option>",
    type=click.STRING,
)
@click.argument(
    "value",
    cls=NotRequiredIf,
    not_required_if=["list", "unset"],
    metavar="<value>",
    type=click.STRING,
)
@click.option(
    "--unset",
    cls=NotRequired,
    not_required=["value", "list"],
    is_flag=True,
    help="Unset an option",
)
@click.option(
    "--list",
    cls=NotRequired,
    not_required=["option", "value", "unset"],
    is_flag=True,
    help="Show the whole config",
)
def config(option: str | None, value: str | None, list: bool, unset: bool) -> None:
    session = get_current_session()
    if list:
        printer.config(session.config.options)
        return

    if unset and option is not None:
        del session.config[option]
    elif option is not None and value is not None:
        session.config[option] = value

    session.config.save()
    printer.echo(SuccessNotification("Config updated"))
