from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from hyperfocus.database.models import TaskStatus
from hyperfocus.termui import formatter, icons, style
from hyperfocus.termui.markup import markup


if TYPE_CHECKING:
    from hyperfocus.database.models import Task


class UIComponent(ABC):
    @abstractmethod
    def resolve(self) -> str:
        raise NotImplementedError


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

    def __init__(self, tasks: list[Task]):
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
