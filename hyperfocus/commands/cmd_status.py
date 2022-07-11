from __future__ import annotations

from typing import TYPE_CHECKING

from hyperfocus.commands import SessionHyperfocusCommand
from hyperfocus.commands.cmd_task import TaskCommand


if TYPE_CHECKING:
    from hyperfocus.session import Session


class StatusCommand(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)
        self._task_command = TaskCommand(session)

    def execute(self) -> None:
        self._task_command.show_tasks()
