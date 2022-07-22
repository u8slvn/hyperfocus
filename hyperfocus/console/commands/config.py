from __future__ import annotations

import click

from hyperfocus.console.commands import SessionHyperfocusCommand
from hyperfocus.console.core.parameters import NotRequired, NotRequiredIf
from hyperfocus.session import Session, get_current_session
from hyperfocus.termui import printer


class ConfigCmd(SessionHyperfocusCommand):
    def execute(
        self, option: str | None, value: str | None, list_: bool, unset: bool
    ) -> None:
        if list_:
            self._show_config()
        elif unset and option is not None:
            self._delete_option(option=option)
        elif option is not None and value is not None:
            self._edit_option(option=option, value=value)

    def _show_config(self) -> None:
        printer.config(self._session.config.options)

    def _save_config(self) -> None:
        self._session.config.save()
        printer.success("Config updated", event="success")

    def _delete_option(self, option: str) -> None:
        del self._session.config[option]
        self._save_config()

    def _edit_option(self, option: str, value) -> None:
        self._session.config[option] = value
        self._save_config()


@click.command(help="Get and set options")
@click.argument(
    "option",
    cls=NotRequiredIf,
    not_required_if=["list_"],
    metavar="<option>",
    type=click.STRING,
)
@click.argument(
    "value",
    cls=NotRequiredIf,
    not_required_if=["list_", "unset"],
    metavar="<value>",
    type=click.STRING,
)
@click.option(
    "--unset",
    cls=NotRequired,
    not_required=["value", "list_"],
    is_flag=True,
    help="Unset an option",
)
@click.option(
    "--list",
    "list_",
    cls=NotRequired,
    not_required=["option", "value", "unset"],
    is_flag=True,
    help="Show the whole config",
)
def config(option: str | None, value: str | None, list_: bool, unset: bool) -> Session:
    session = get_current_session()
    ConfigCmd(session).execute(option=option, value=value, list_=list_, unset=unset)

    return session
