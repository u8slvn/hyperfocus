from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type

from hyperfocus.config.exceptions import ConfigError


class ConfigPolicies:
    def __init__(self, policies: dict[str, Type[ConfigPolicy]] | None = None) -> None:
        self._policies = policies or {}

    def _check(self, section: str, key: str, value: str | None = None) -> None:
        policy = self._policies.get(section)
        if policy is None:
            return

        if value is not None:
            policy(key).check_input(value)
        else:
            policy(key).check_deletion()

    def check_input(self, section: str, key: str, value: str) -> None:
        self._check(section=section, key=key, value=value)

    def check_deletion(self, section: str, key: str) -> None:
        self._check(section=section, key=key)


class ConfigPolicy(ABC):
    section: str | None = None

    def __init__(self, key: str) -> None:
        self.key = key

    @property
    def option(self) -> str:
        return f"{self.section}.{self.key}"

    @abstractmethod
    def check_input(self, value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_deletion(self) -> None:
        raise NotImplementedError


class CorePolicy(ConfigPolicy):
    section = "core"

    def check_input(self, value: str) -> None:
        if self.key == "database":
            db_path = Path(value)
            if not db_path.parent.is_dir():
                raise ConfigError(
                    f"Config option '{self.option}' must be a valid path."
                )
        else:
            raise ConfigError(f"Unknown config option '{self.option}'.")

    def check_deletion(self) -> None:
        if self.key == "database":
            raise ConfigError(
                f"Deletion of config option '{self.option}' is forbidden."
            )


class AliasPolicy(ConfigPolicy):
    section = "alias"

    def check_input(self, value: str) -> None:
        from hyperfocus.console.cli import hyf

        commands = hyf.get_commands()

        if value not in commands:
            raise ConfigError("Alias must referred to an existing command.")

        if self.key in commands:
            raise ConfigError("Alias cannot override an existing command.")

    def check_deletion(self) -> None:
        pass
