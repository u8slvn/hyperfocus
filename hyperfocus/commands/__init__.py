from abc import ABC

from hyperfocus.session import Session


class HyperfocusCommand(ABC):
    pass


class SessionHyperfocusCommand(HyperfocusCommand, ABC):
    def __init__(self, session: Session) -> None:
        self._session = session
