from __future__ import annotations

import functools
import re

import click
from click import Parameter

from hyperfocus import printer
from hyperfocus.config import Config
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
class HyfGroup(click.Group):
    def get_command(self, ctx: click.Context, cmd_name: str):
        cmd = click.Group.get_command(self, ctx=ctx, cmd_name=cmd_name)
        if cmd is not None:
            return cmd

        config = Config.load()
        variable = f"alias.{cmd_name}"
        if variable in config:
            cmd_name = config[variable]

        return click.Group.get_command(self, ctx, cmd_name)

    def resolve_command(
        self, ctx: click.Context, args: list[str]
    ) -> tuple[str | None, click.Command | None, list[str]]:
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        cmd_name = cmd if cmd is None else cmd.name
        return cmd_name, cmd, args


class NotRequiredIf(click.Argument):
    def __init__(self, *args, not_required_if: list[str], **kwargs):
        self.not_required_if = not_required_if
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts

        for not_required_opt in self.not_required_if:
            other_opt: bool = not_required_opt in opts
            if all([current_opt, other_opt]):
                self.required = False

        return super().handle_parse_result(ctx, opts, args)


class NotRequired(click.Option):
    def __init__(self, *args, not_required: list[str], **kwargs):
        self.not_required = not_required
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        params = {p.name: p for p in ctx.command.get_params(ctx)}
        current_opt: bool = self.name in opts

        for not_required_opt in self.not_required:
            other_option: bool = not_required_opt in opts and opts[not_required_opt]
            if all([current_opt, other_option]):
                param: Parameter = params[not_required_opt]
                raise click.exceptions.UsageError(
                    f"Unnecessary {param.param_type_name} "
                    f"'{param.human_readable_name}' provided",
                    ctx,
                )

        return super().handle_parse_result(ctx, opts, args)
