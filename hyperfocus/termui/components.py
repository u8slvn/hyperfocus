from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from hyperfocus.database.models import TaskStatus
from hyperfocus.termui import formatter, icons, style
from hyperfocus.termui.formatter import task_status
from hyperfocus.termui.markup import markup


if TYPE_CHECKING:
    from hyperfocus.database.models import Task


class UIComponent(ABC):
    """
    Base class of UIComponent all components must inherit from it.

    An UIComponent is a formatter with much more complex logic.
    """

    @abstractmethod
    def resolve(self) -> str:
        raise NotImplementedError


class TaskDetails(UIComponent):
    def __init__(self, task: Task):
        self._task = task

    def resolve(self) -> str:
        task_info = {
            "Task": f"#{self._task.id}",
            "Status": (
                f"{task_status(TaskStatus(self._task.status))} "
                f"{TaskStatus(self._task.status).name.title()}"
            ),
            "Title": self._task.title,
            "Details": self._task.details or "...",
            "History": "",
        }
        full_details = []
        for info, value in task_info.items():
            full_details.append(f"[{style.INFO}]{info}[/]: {value}")

        task = self._task
        bullet_point = f" [{style.INFO}]{icons.LIST}[/] "
        history = [
            f"{bullet_point}{formatter.date_with_time(task.created_at)} " f"- add task"
        ]
        while True:
            task = task.parent_task
            if task is None:
                break
            step = (
                f"{bullet_point}{formatter.date_with_time(task.created_at)} "
                f"- continue task"
            )
            history.append(step)
        history[-1] = history[-1].replace("continue", "create")

        return "\n".join(full_details) + "\n" + "\n".join(history)


class TasksTable(UIComponent):
    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = tasks
        self._headers = ["#", "tasks", "details"]
        self._columns = [[h] for h in self._headers]
        self._alignments = ["right", "", "center"]

    def _add_cells(self, *values) -> None:
        for i, value in enumerate(values):
            self._columns[i].append(value)

    def resolve(self) -> str:
        for task in self._tasks:
            details = icons.DETAILS if task.details else icons.NO_DETAILS
            self._add_cells(str(task.id), formatter.task(task), details)

        def col_len(text: str) -> int:
            return len(markup.remove(text))

        max_col_length = [col_len(max(col, key=col_len)) for col in self._columns]
        separator = "-".join([(length + 2) * "-" for length in max_col_length])

        render_rows = []
        for row in zip(*self._columns):
            render_cells = []

            for n_cell, cell in enumerate(row):
                alignment = self._alignments[n_cell]
                width = max_col_length[n_cell]

                cell_space = width - col_len(cell)

                if alignment == "center":
                    right = left = int(cell_space / 2)
                elif alignment == "right":
                    right = cell_space
                    left = 0
                else:
                    right = 0
                    left = cell_space

                render_cells.append(f" {right * ' '}{cell}{left * ' '} ")

            render_rows.append(f" {' '.join(render_cells)} ")

            if len(render_rows) == 1:
                render_rows.append(f" {separator} ")

        return "\n" + "\n".join(render_rows) + "\n"


class ProgressBar(UIComponent):
    width = 30

    def __init__(self, tasks: list[Task]) -> None:
        self._done_tasks = list(
            filter(lambda task: task.status == TaskStatus.DONE, tasks)
        )
        self._todo_tasks = list(
            filter(lambda task: task.status == TaskStatus.TODO, tasks)
        )

    def resolve(self) -> str:
        done_tasks = len(self._done_tasks)
        total = done_tasks + len(self._todo_tasks)
        if total == 0:
            return ""

        percent_done = done_tasks * 100 / total
        done_count = round((percent_done * self.width) / 100)
        todo_count = self.width - done_count

        prefix = f"[{style.SUCCESS}] {icons.TASK_STATUS} {int(percent_done)}%[/] "
        done = (
            f"[{style.SUCCESS}]{icons.PROGRESSBAR * done_count}[/]"
            if done_count
            else ""
        )
        todo = icons.PROGRESSBAR_EMPTY * todo_count

        return f"{prefix}[{done}{todo}]\n"


class NewDay(UIComponent):
    def __init__(self, date: datetime.date) -> None:
        self._date = date

    def resolve(self) -> str:
        return (
            f"[{style.NEW_DAY}]> {icons.NEW_DAY} {formatter.date(self._date)}: "
            f"A new day starts, good luck![/]"
        )


class Notification(UIComponent):
    level = "unknown"

    def __init__(self, text: str):
        self._text = text

    def resolve(self) -> str:
        color, icon = {
            "success": (style.SUCCESS, icons.SUCCESS),
            "info": (style.INFO, icons.INFO),
            "warning": (style.WARNING, icons.WARNING),
            "error": (style.ERROR, icons.ERROR),
        }.get(self.level, (style.DEFAULT, icons.NOTIFICATION))
        prefix = f"[{color}]{icon}({self.level})[/]"

        return f"{prefix} {self._text}"


class SuccessNotification(Notification):
    level = "success"


class InfoNotification(Notification):
    level = "info"


class WarningNotification(Notification):
    level = "warning"


class ErrorNotification(Notification):
    level = "error"
