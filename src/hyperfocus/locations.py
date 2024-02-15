from __future__ import annotations

from pathlib import Path

import click

from hyperfocus import __app_name__


CONFIG_DIR = Path(click.get_app_dir(__app_name__))

DEFAULT_DB_PATH = Path.home() / f".{__app_name__}.sqlite"
