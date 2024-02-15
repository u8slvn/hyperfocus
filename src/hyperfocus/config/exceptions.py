from __future__ import annotations

from hyperfocus.exceptions import HyperfocusError


class ConfigError(HyperfocusError):
    pass


class ConfigFileError(ConfigError):
    pass
