from typing import Optional


class HyperfocusException(Exception):
    def __init__(self, message: str, event: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.event = event or "error"


class TaskError(HyperfocusException):
    pass


class ConfigError(HyperfocusException):
    pass


class DatabaseError(HyperfocusException):
    pass


class SessionError(HyperfocusException):
    pass
