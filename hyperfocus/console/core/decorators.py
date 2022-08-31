from __future__ import annotations

from typing import Any, cast

import click

from hyperfocus.console.core.group import HyperFocus


def hyperfocus(**kwargs: Any) -> HyperFocus:
    cli = click.group(cls=HyperFocus, **kwargs)
    return cast(HyperFocus, cli)
