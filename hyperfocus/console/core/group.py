from __future__ import annotations

import click
from click import Command

from hyperfocus.config.config import Config
from hyperfocus.console.core.error_handler import hyf_error_handler
from hyperfocus.utils import wrap_methods


@wrap_methods(hyf_error_handler, ["make_context", "invoke"])
class AliasGroup(click.Group):
    def get_command(self, ctx: click.Context, cmd_name: str) -> Command | None:
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

    def add_commands(self, commands: list[Command]) -> None:
        for command in commands:
            self.add_command(command)

    def get_commands(self) -> list[str]:
        return [command for command in self.commands.keys()]
