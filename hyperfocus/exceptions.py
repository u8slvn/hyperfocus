class HyperfocusException(Exception):
    """Hyperfocus base exception."""

    message: str = "Something went wrong"

    def __init__(self, message: str = None):
        super().__init__(message or self.message)


class ConfigError(HyperfocusException):
    message = "Config error"


class ConfigDoesNotExistError(ConfigError):
    message = "Config does not exist, please run init command first"


class DatabaseError(HyperfocusException):
    message = "Database error"


class DatabaseDoesNotExists(DatabaseError):
    message = "Database does not exist, please run init command first"


class DatabaseNotinitializedError(DatabaseError):
    message = "Database not initialized, please run init command first"
