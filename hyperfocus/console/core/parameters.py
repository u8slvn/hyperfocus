from __future__ import annotations

from typing import Any

import click
from click import Parameter


class NotRequiredIf(click.Argument):
    def __init__(self, *args, not_required_if: list[str], **kwargs) -> None:
        self.not_required_if = not_required_if
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args) -> tuple[Any, list[str]]:
        current_opt: bool = self.name in opts

        for not_required_opt in self.not_required_if:
            other_opt: bool = not_required_opt in opts
            if all([current_opt, other_opt]):
                self.required = False

        return super().handle_parse_result(ctx, opts, args)


class NotRequired(click.Option):
    def __init__(self, *args, not_required: list[str], **kwargs) -> None:
        self.not_required = not_required
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args) -> tuple[Any, list[str]]:
        params = {p.name: p for p in ctx.command.get_params(ctx)}
        current_opt: bool = self.name in opts

        for not_required_opt in self.not_required:
            other_option: bool = not_required_opt in opts and opts[not_required_opt]
            if all([current_opt, other_option]):
                param: Parameter = params[not_required_opt]
                raise click.exceptions.UsageError(
                    f"Unnecessary {param.param_type_name} "
                    f"'{param.human_readable_name}' provided",
                    ctx=ctx,
                )

        return super().handle_parse_result(ctx, opts, args)
