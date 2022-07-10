from __future__ import annotations

import click

from hyperfocus.config.config import Config
from hyperfocus.hyf_click.error_handler import hyf_error_handler
from hyperfocus.utils import wrap_methods


@wrap_methods(hyf_error_handler, ["make_context", "invoke"])
class HyfGroup(click.Group):
    def get_command(self, ctx: click.Context, cmd_name: str):
        cmd = click.Group.get_command(self, ctx=ctx, cmd_name=cmd_name)
        if cmd is not None:
            return cmd

        config = Config.load()
        option = f"alias.{cmd_name}"
        if option in config:
            cmd_name = config[option]

        return click.Group.get_command(self, ctx, cmd_name)

    def resolve_command(
        self, ctx: click.Context, args: list[str]
    ) -> tuple[str | None, click.Command | None, list[str]]:
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        cmd_name = cmd if cmd is None else cmd.name
        return cmd_name, cmd, args
