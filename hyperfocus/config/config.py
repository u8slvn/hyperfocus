from __future__ import annotations

import contextlib
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from hyperfocus.config.exceptions import ConfigError
from hyperfocus.config.file import ConfigFile
from hyperfocus.locations import CONFIG_DIR, CONFIG_PATH


_loaded_config: Config | None = None


class Config:
    default_config: dict[str, dict] = {
        "core": {
            "database": "",
        },
        "alias": {},
    }

    def __init__(self) -> None:
        self._config = deepcopy(self.default_config)
        self._config_file: ConfigFile = ConfigFile(CONFIG_PATH)

    @staticmethod
    def make_directory() -> None:
        try:
            CONFIG_DIR.mkdir(exist_ok=True)
        except OSError as error:
            raise ConfigError(f"Configuration folder creation failed: {error}")

    def merge(self, config: dict[str, Any]) -> None:
        self._config.update(config)

    @property
    def config(self) -> dict[str, dict]:
        return self._config

    @property
    def config_file(self) -> ConfigFile:
        return self._config_file

    def set_config_file(self, config_file: ConfigFile) -> None:
        self._config_file = config_file

    @classmethod
    def load(cls, config_path: Path | None = None, reload: bool = False) -> Config:
        global _loaded_config

        if _loaded_config is None or reload:
            config_path = config_path or CONFIG_PATH
            config_file = ConfigFile(config_path)
            if not config_file.exists():
                raise ConfigError(
                    "Config does not exist, please run init command first"
                )

            _loaded_config = cls()
            _loaded_config.merge(config_file.read())
            _loaded_config.set_config_file(config_file)

        return _loaded_config

    def save(self):
        self._config_file.write(self._config)

    def variables(self) -> dict[str, str]:
        variables = {}
        for section, settings in self._config.items():
            variables.update({f"{section}.{i}": v for i, v in settings.items()})
        return variables

    def get_variable(self, variable: str) -> str:
        with check_variable(variable) as config_variable:
            return self._config[config_variable.section][config_variable.index]

    def update_variable(self, variable: str, value: str) -> None:
        with check_variable(variable) as config_variable:
            self._config[config_variable.section][config_variable.index] = value

    def delete_variable(self, variable: str) -> None:
        with check_variable(variable) as config_variable:
            del self._config[config_variable.section][config_variable.index]

    def __getitem__(self, variable: str) -> str:
        return self.get_variable(variable=variable)

    def __setitem__(self, variable: str, value: str) -> None:
        self.update_variable(variable=variable, value=value)

    def __delitem__(self, variable: str) -> None:
        self.delete_variable(variable=variable)

    def __contains__(self, variable: str) -> bool:
        return variable in self.variables()


@contextlib.contextmanager
def check_variable(variable: str):
    section, index = variable.split(".")
    try:
        yield SimpleNamespace(**{"section": section, "index": index})
    except KeyError:
        raise ConfigError(f"Variable {variable} does not exist")
