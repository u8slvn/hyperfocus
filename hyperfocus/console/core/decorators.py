from __future__ import annotations

from typing import Any, cast

import click

from hyperfocus.console.core.group import AliasGroup


def hyperfocus(**kwargs: Any):
    group = click.group(cls=AliasGroup, **kwargs)
    return cast(AliasGroup, group)
