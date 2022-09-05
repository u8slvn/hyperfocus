from __future__ import annotations

from typing import Any, cast

import click

from hyperfocus.console.core.group import HyperFocus


def hyperfocus(**kwargs: Any) -> HyperFocus:
    context_settings = {
        "help_option_names": ["-h", "--help"],
    }
    cli = click.group(cls=HyperFocus, context_settings=context_settings, **kwargs)
    return cast(HyperFocus, cli)
