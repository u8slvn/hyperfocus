from __future__ import annotations

from typing import Any
from typing import Mapping

import click


class NotRequiredIf(click.Argument):
    def __init__(self, *args: Any, not_required_if: list[str], **kwargs: Any) -> None:
        self.not_required_if = not_required_if
        super().__init__(*args, **kwargs)

    def handle_parse_result(
        self, ctx: click.Context, opts: Mapping[str, Any], args: list[str]
    ) -> tuple[Any, list[str]]:
        current_opt: bool = self.name in opts

        for not_required_opt in self.not_required_if:
            other_opt: bool = not_required_opt in opts
            if all([current_opt, other_opt]):
                self.required = False

        return super().handle_parse_result(ctx, opts, args)
