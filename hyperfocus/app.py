from __future__ import annotations

import functools
import re

import click

from hyperfocus import printer
from hyperfocus.exceptions import HyperfocusException
from hyperfocus.utils import wrap_methods


def app_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HyperfocusException as error:
            printer.error(text=error.message, event=error.event)
            raise click.exceptions.Exit(1)
        except click.ClickException as error:
            message = error.format_message().rstrip(".")
            split_error_name = re.findall(r"[A-Z][^A-Z]*", type(error).__name__)
            event = " ".join(split_error_name).lower()
            printer.error(text=message, event=event)

    return wrapper


@wrap_methods(app_error_handler, ["make_context", "invoke"])
class Hyperfocus(click.Group):
    pass
    # def get_command(self, ctx: click.Context, cmd_name: str):
    #     cmd = click.Group.get_command(self, ctx=ctx, cmd_name=cmd_name)
    #     if cmd is not None:
    #         return cmd
    #
    #     config = Config.load()
    #     if cmd_name in config.get_section("alias"):
    #         cmd_name = config[f"alias.{cmd_name}"]
    #
    #     return click.Group.get_command(self, ctx, cmd_name)
    #
    # def resolve_command(
    #     self, ctx: click.Context, args: list[str]
    # ) -> tuple[str | None, click.Command | None, list[str]]:
    #     # always return the command's name, not the alias
    #     _, cmd, args = super().resolve_command(ctx, args)
    #     cmd_name = cmd if cmd is None else cmd.name
    #     return cmd_name, cmd, args
