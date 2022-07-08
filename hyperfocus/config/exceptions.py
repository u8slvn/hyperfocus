from hyperfocus.exceptions import HyperfocusException


class ConfigError(HyperfocusException):
    pass


class ConfigFileError(ConfigError):
    pass
