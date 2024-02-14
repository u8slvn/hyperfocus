from __future__ import annotations

import contextlib
import re

from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from typing import Generator
from typing import cast

from hyperfocus.config.exceptions import ConfigError
from hyperfocus.config.exceptions import ConfigFileError
from hyperfocus.config.file import ConfigFile
from hyperfocus.config.policy import AliasPolicy
from hyperfocus.config.policy import ConfigPolicies
from hyperfocus.config.policy import CorePolicy
from hyperfocus.locations import CONFIG_DIR


_loaded_config: Config | None = None


class Config:
    default_config: dict[str, dict[str, Any]] = {
        "core": {
            "database": "",
            "force_color": False,
        },
        "alias": {},
    }
    _policies = ConfigPolicies(
        {
            "core": CorePolicy,
            "alias": AliasPolicy,
        }
    )
    _dir = CONFIG_DIR
    _filename = "config.ini"

    def __init__(self) -> None:
        self._config = deepcopy(self.default_config)
        config_path = self._build_config_path()
        self._config_file = ConfigFile(config_path, model=self.default_config)

    @classmethod
    def _build_config_path(cls) -> Path:
        return cls._dir / cls._filename

    @classmethod
    def make_directory(cls) -> None:
        try:
            cls._dir.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise ConfigError(f"Configuration folder creation failed: {error}")

    def merge(self, config: dict[str, Any]) -> None:
        self._config.update(config)

    @property
    def config(self) -> dict[str, dict[str, Any]]:
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
            config_path = config_path or cls._build_config_path()
            config_file = ConfigFile(config_path, model=cls.default_config)
            if not config_file.exists():
                raise ConfigError(
                    "Config does not exist, please run init command first."
                )

            _loaded_config = cls()
            _loaded_config.merge(config_file.read())
            _loaded_config.set_config_file(config_file)

        return _loaded_config

    def save(self) -> None:
        try:
            self._config_file.write(self._config)
        except ConfigFileError as error:
            raise ConfigError(
                f"Saving config to {self._config_file.path} failed: {error}."
            )

    @property
    def options(self) -> dict[str, str]:
        options = {}
        for section, settings in self._config.items():
            options.update({f"{section}.{i}": v for i, v in settings.items()})
        return options

    def __getitem__(self, option: str) -> Any:
        with self.secured_option(option=option) as opt:
            return cast(str, self._config[opt.section][opt.key])

    def __setitem__(self, option: str, value: str) -> None:
        with self.secured_option(option=option) as opt:
            self._policies.check_input(section=opt.section, key=opt.key, value=value)
            self._config[opt.section][opt.key] = value

    def __delitem__(self, option: str) -> None:
        with self.secured_option(option=option) as opt:
            self._policies.check_deletion(section=opt.section, key=opt.key)
            del self._config[opt.section][opt.key]

    def __contains__(self, option: str) -> bool:
        return option in self.options

    @staticmethod
    @contextlib.contextmanager
    def secured_option(option: str) -> Generator[SimpleNamespace, None, None]:
        match = re.match(r"^(?P<section>[A-Za-z0-9]+).(?P<key>\w+)$", option)
        if match is None:
            raise ConfigError(f"Bad format config option '{option}'.")

        try:
            yield SimpleNamespace(**match.groupdict())
        except KeyError:
            raise ConfigError(f"Variable '{option}' does not exist.")
