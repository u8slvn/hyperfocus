from __future__ import annotations

from typing import Any, Callable, overload

import click
from click import Command

from hyperfocus.config.config import Config
from hyperfocus.console.core.error_handler import hyf_error_handler
from hyperfocus.utils import wrap_methods


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


class DefaultCommandGroup(click.Group):
    def __init__(self, *args, **kwargs) -> None:
        self.default_command = None
        super().__init__(*args, **kwargs)

    @overload
    def command(self, __func: Callable[..., Any]) -> Command:
        ...

    @overload
    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], Command]:
        ...

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], Command]:
        default_command = kwargs.pop("default_command", False)
        decorator = super().command(*args, **kwargs)

        if default_command:

            def new_decorator(f):
                command = decorator(f)
                self.default_command = command.name
                return command

            return new_decorator

        return decorator

    def resolve_command(
        self, ctx: click.Context, args: Any
    ) -> tuple[str | None, Command | None, list[str]]:
        try:
            return super().resolve_command(ctx, args)
        except click.UsageError:
            args.insert(0, self.default_command)
            return super().resolve_command(ctx, args)


@wrap_methods(hyf_error_handler, ["make_context", "invoke"])
class HyperFocus(AliasGroup):
    def add_commands(self, commands: list[Command]) -> None:
        for command in commands:
            self.add_command(command)

    def get_commands(self) -> list[str]:
        return [command for command in self.commands.keys()]
