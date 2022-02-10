from datetime import datetime
from pathlib import Path
from typing import List, Optional

import typer

from hyperfocus import config, printer
from hyperfocus.database import database
from hyperfocus.models import DailyTracker, Status, Task, MODELS


class AppService:
    @staticmethod
    def initialize(db_path: Path):
        config.init(db_path=db_path)
        typer.secho(
            printer.notification(
                text=f"Config file created successfully in {config.FILE_PATH}",
                action="init",
                status=printer.NotificationStatus.INFO,
            )
        )
        database.connect(config=config.load())
        database.init_models(models=MODELS)
        typer.secho(
            printer.notification(
                text=f"Database initialized successfully in {db_path}",
                action="init",
                status=printer.NotificationStatus.INFO,
            )
        )


class DailyTrackerService:
    def __init__(self):
        database.connect(config=config.load())
        now = datetime.now().date()
        self._base, new_day = DailyTracker.get_or_create(date=now)
        if new_day:
            self._start_new_day()

    def _start_new_day(self):
        typer.echo(f"✨ {self.date}")
        typer.echo("✨ A new day starts, good luck!\n")

    @property
    def date(self) -> str:
        return printer.date(self._base.date)

    def add_task(self, title: str, details: Optional[str] = None) -> None:
        details = details.strip() if isinstance(details, str) else details
        task = Task(
            id=self._base.next_task_id,
            title=title.strip(),
            details=details,
            status=Status.TODO.value,
            daily_tracker=self._base,
        )
        task.save()
        self._base.task_increment += 1
        self._base.save()
        typer.secho(
            printer.notification(
                text=printer.task(task=task, show_prefix=True),
                action="created",
                status=printer.NotificationStatus.SUCCESS,
            )
        )

    def _get_task(self, id: int) -> Task:
        task = Task.get_or_none(Task.id == id, Task.daily_tracker == self._base)
        if not task:
            typer.secho(
                printer.notification(
                    text="Task id does not exist",
                    action="not found",
                    status=printer.NotificationStatus.ERROR,
                )
            )
            raise typer.Exit(1)

        return task

    def update_task(self, id: int, status: Status) -> None:
        task = self._get_task(id=id)
        if task.status == status.value:
            typer.secho(
                printer.notification(
                    text=printer.task(task=task, show_prefix=True),
                    action="no change",
                    status=printer.NotificationStatus.WARNING,
                )
            )
            raise typer.Exit()
        task.status = status.value
        task.save()
        typer.secho(
            printer.notification(
                text=printer.task(task=task, show_prefix=True),
                action="updated",
                status=printer.NotificationStatus.SUCCESS,
            )
        )

    def show_task(self, id: int) -> None:
        task = self._get_task(id=id)
        typer.secho(f"Task: #{id} {printer.task(task=task, show_details=True)}")

    def show_tasks(
        self, exclude: Optional[List[Status]] = None, newline: bool = False
    ) -> None:
        exclude = exclude or []
        tasks = [
            task for task in self._base.tasks if Status(task.status) not in exclude
        ]
        if not tasks:
            typer.echo("No tasks yet for today...")
            raise typer.Exit()
        typer.secho(printer.tasks(tasks=tasks, newline=newline))
