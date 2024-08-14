from __future__ import annotations

from typing import Any
from typing import Mapping

import click


class NotRequired(click.Option):
    def __init__(self, *args: Any, not_required: list[str], **kwargs: Any) -> None:
        self.not_required = not_required
        super().__init__(*args, **kwargs)

    def handle_parse_result(
        self, ctx: click.Context, opts: Mapping[str, Any], args: list[str]
    ) -> tuple[Any, list[str]]:
        params = {p.name: p for p in ctx.command.get_params(ctx)}
        current_opt: bool = self.name in opts

        for not_required_opt in self.not_required:
            other_option: bool = not_required_opt in opts and opts[not_required_opt]
            if all([current_opt, other_option]):
                param: click.Parameter = params[not_required_opt]
                raise click.exceptions.UsageError(
                    f"Unnecessary {param.param_type_name} "
                    f"'{param.human_readable_name}' provided",
                    ctx=ctx,
                )

        return super().handle_parse_result(ctx, opts, args)
