from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type

from hyperfocus.config.exceptions import ConfigError


class OptionPolicies:
    def __init__(self, policies: dict[str, Type[OptionPolicy]] | None = None):
        self._policies = policies or {}

    def check(self, section: str, key: str, value: str) -> None:
        policy = self._policies.get(section)
        if policy is not None:
            policy(key, value).validate()


class OptionPolicy(ABC):
    section: str | None = None

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    @property
    def option(self) -> str:
        return f"{self.section}.{self.key}"

    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError


class CorePolicy(OptionPolicy):
    section = "core"

    def validate(self) -> None:
        if self.key == "database":
            db_path = Path(self.value)
            if not db_path.parent.is_dir():
                raise ConfigError(
                    f"Config option '{self.option}' must be a valid path."
                )
        else:
            raise ConfigError(f"Unknown config option '{self.option}'.")


class AliasPolicy(OptionPolicy):
    section = "alias"

    def validate(self) -> None:
        from hyperfocus import cli

        if self.value not in cli.get_commands():
            raise ConfigError("Alias must referred to an existing command name.")
