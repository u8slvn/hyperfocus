from __future__ import annotations

from typing import Any

import click


class IntListParamType(click.ParamType):
    """Int List Parameter Type.

    A custom click parameter type for a list of integers.
    """

    name = "integer_list"

    def convert(
        self,
        value: Any,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> Any:
        if isinstance(value, list) and all(isinstance(item, int) for item in value):
            return value

        try:
            items = value.split()
            return [int(item) for item in items]
        except (ValueError, AttributeError):
            self.fail(f"{value!r} is not a list of integers", param, ctx)


INT_LIST = IntListParamType()
