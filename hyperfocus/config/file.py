from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from hyperfocus.config.exceptions import ConfigFileError


class ConfigFile:
    def __init__(self, path: str | Path) -> None:
        if isinstance(path, str):
            path = Path(path)
        self._path = path
        self._parser = ConfigParser()

    @property
    def path(self) -> str:
        return str(self._path)

    def exists(self) -> bool:
        return self._path.exists()

    def read(self) -> dict[str, dict]:
        self._parser.read(self._path)
        return {s: dict(self._parser.items(s)) for s in self._parser.sections()}

    def write(self, config: dict[str, dict]) -> None:
        for section, items in config.items():
            self._parser[section] = items

        try:
            if not self.exists():
                self._path.touch(mode=0o600)

            with self._path.open("w") as file:
                self._parser.write(file)
        except OSError as error:
            raise ConfigFileError(str(error)) from error
