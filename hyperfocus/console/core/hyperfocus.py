from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from click import group

from hyperfocus.console.core.error_handler import hyf_error_handler
from hyperfocus.console.core.group import AliasGroup
from hyperfocus.utils import wrap_methods


if TYPE_CHECKING:
    from click import Command


def hyperfocus(**kwargs: Any) -> Hyperfocus:
    context_settings = {
        "help_option_names": ["-h", "--help"],
    }
    cli = group(cls=Hyperfocus, context_settings=context_settings, **kwargs)
    return cast(Hyperfocus, cli)


@wrap_methods(hyf_error_handler, ["make_context", "invoke"])
class Hyperfocus(AliasGroup):
    def add_commands(self, commands: list[Command]) -> None:
        for command in commands:
            self.add_command(command)

    def get_commands(self) -> list[str]:
        return [command for command in self.commands.keys()]
