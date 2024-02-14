from __future__ import annotations

from collections import defaultdict
from configparser import ConfigParser
from pathlib import Path
from typing import Any

from hyperfocus.config.exceptions import ConfigFileError


class ConfigFile:
    def __init__(self, path: str | Path, model: dict[str, dict[str, Any]]) -> None:
        if isinstance(path, str):
            path = Path(path)
        self._path = path
        self._parser = ConfigParser()
        self._model = model

    @property
    def path(self) -> str:
        return str(self._path)

    def exists(self) -> bool:
        return self._path.exists()

    def read(self) -> dict[str, dict[str, Any]]:
        self._parser.read(self._path)
        config: dict[str, dict[str, Any]] = defaultdict(dict)

        for section in self._parser.sections():
            for option in self._parser.options(section=section):
                value_type = type(self._model.get(section, {}).get(option, ""))

                value: Any
                if value_type is bool:
                    value = self._parser.getboolean(section=section, option=option)
                else:
                    value = self._parser.get(section=section, option=option)

                config[section][option] = value

        return config

    def write(self, config: dict[str, dict[str, Any]]) -> None:
        for section, items in config.items():
            self._parser[section] = items

        try:
            if not self.exists():
                self._path.touch(mode=0o600)

            with self._path.open("w") as file:
                self._parser.write(file)
        except OSError as error:
            raise ConfigFileError(str(error)) from error
