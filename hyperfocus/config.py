import configparser
from pathlib import Path
from typing import Optional

import click

from hyperfocus import __app_name__
from hyperfocus.exceptions import ConfigError

DEFAULT_DB_PATH = Path.home() / f".{__app_name__}.sqlite"


class Config:
    _dir_path = Path(click.get_app_dir(__app_name__))
    _filename = "config.ini"
    file_path = _dir_path / _filename

    def __init__(self, db_path: str, dir_path: Optional[Path] = None):
        self._dir_path = dir_path or self._dir_path
        self.file_path = self._dir_path / self._filename
        self.db_path = Path(db_path)

    def make_directory(self):
        try:
            self._dir_path.mkdir(exist_ok=True)
        except OSError:
            raise ConfigError("Configuration folder creation failed")

    @classmethod
    def load(cls, file_path: Optional[Path] = None) -> "Config":
        file_path = file_path or cls.file_path
        if not file_path.exists():
            raise ConfigError("Config does not exist, please run init command first")
        config_parser = configparser.ConfigParser()
        config_parser.read(file_path)

        return cls(
            db_path=config_parser["main"]["db_file_path"],
        )

    def save(self):
        config_parser = configparser.ConfigParser()
        config_parser["main"] = {
            "db_file_path": str(self.db_path),
        }
        try:
            with self.file_path.open("w") as file:
                config_parser.write(file)
        except OSError:
            raise ConfigError(f"Saving config to {self.file_path} failed")
