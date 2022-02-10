import configparser
from dataclasses import dataclass
from pathlib import Path

import typer

from hyperfocus import __app_name__
from hyperfocus.exceptions import ConfigError, ConfigDoesNotExistError

DIR_PATH = Path(typer.get_app_dir(__app_name__))
FILE_PATH = DIR_PATH / "config.ini"


def init(db_path: Path):
    try:
        DIR_PATH.mkdir(exist_ok=True)
        db_path.touch()
    except OSError:
        raise ConfigError("Configuration folder creation failed")
    config_parser = configparser.ConfigParser()
    config_parser["main"] = {
        "db_path": db_path,
    }
    try:
        with FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        raise ConfigError(f"Saving config to {FILE_PATH} failed")


@dataclass(frozen=True)
class Config:
    db_path: Path


def load() -> Config:
    if not FILE_PATH.exists():
        raise ConfigDoesNotExistError()
    config_parser = configparser.ConfigParser()
    config_parser.read(FILE_PATH)

    return Config(
        db_path=Path(config_parser["main"]["db_path"]),
    )


DEFAULT = Config(db_path=Path.home() / f".{__app_name__}.sqlite")
