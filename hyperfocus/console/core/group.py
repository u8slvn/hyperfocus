from __future__ import annotations

from typing import Any
from typing import Callable
from typing import cast
from typing import overload

import click

from hyperfocus.config.config import Config


class AliasGroup(click.Group):
    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
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
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.default_command = None
        super().__init__(*args, **kwargs)

    @overload
    def command(self, __func: Callable[..., Any]) -> click.Command: ...

    @overload
    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Command]: ...

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Command]:
        default_command = kwargs.pop("default_command", False)
        decorator = super().command(*args, **kwargs)

        if default_command:

            def new_decorator(f: Callable[..., Any]) -> click.Command:
                command = decorator(f)
                self.default_command = command.name
                return cast(click.Command, command)

            return new_decorator

        return cast(click.Command, decorator)

    def resolve_command(
        self, ctx: click.Context, args: Any
    ) -> tuple[str | None, click.Command | None, list[str]]:
        try:
            return super().resolve_command(ctx, args)
        except click.UsageError:
            args.insert(0, self.default_command)
            return super().resolve_command(ctx, args)
