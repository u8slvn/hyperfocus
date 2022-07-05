import sys
from typing import List, Optional

import click
import pyperclip

from hyperfocus import __app_name__, __version__, formatter, printer
from hyperfocus.app import Hyperfocus
from hyperfocus.config import DEFAULT_DB_PATH, Config
from hyperfocus.database import database
from hyperfocus.exceptions import TaskError
from hyperfocus.models import MODELS, Task, TaskEvents, TaskStatus
from hyperfocus.session import Session, get_current_session


class _CLIHelper:
    def __init__(self, session: Session):
        self._session = session

    def check_task_id_or_ask(
        self, task_id: int, text: str, exclude: Optional[List[TaskStatus]] = None
    ) -> int:
        if task_id:
            return task_id

        exclude = exclude or []
        self.show_tasks(newline=True, exclude=exclude)
        return printer.ask(text, type=int)

    def show_tasks(
        self, exclude: Optional[List[TaskStatus]] = None, newline=False
    ) -> None:
        exclude = exclude or []
        tasks = self._session.daily_tracker.get_tasks(exclude=exclude)
        if not tasks:
            printer.echo("No tasks for today...")
            raise click.exceptions.Exit
        printer.tasks(tasks=tasks, newline=newline)

    def get_task(self, task_id: int) -> Task:
        task = self._session.daily_tracker.get_task(task_id=task_id)
        if not task:
            raise TaskError(
                f"Task {task_id} does not exist", event=TaskEvents.NOT_FOUND
            )

        return task

    def update_task(self, task_id: int, status: TaskStatus, text: str):
        task_id = self.check_task_id_or_ask(task_id=task_id, text=text, exclude=[status])

        task = self.get_task(task_id=task_id)
        if task.status == status.value:
            printer.warning(
                text=formatter.task(task=task, show_prefix=True),
                event=TaskEvents.NO_CHANGE,
            )
            raise click.exceptions.Exit

        task.status = status
        self._session.daily_tracker.update_task(task=task, status=status)
        printer.success(
            text=formatter.task(task=task, show_prefix=True),
            event=TaskEvents.UPDATED,
        )


@click.group(
    cls=Hyperfocus, invoke_without_command=True, help="Show all the tasks for the day."
)
@click.version_option(
    version=__version__, prog_name=__app_name__, help="Show the version."
)
@click.option(
    "--all", is_flag=True, default=False, help="Show all tasks even the deleted ones."
)
@click.pass_context
def cli(ctx: click.Context, all: bool):
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    session = Session()
    session.bind_context(ctx=ctx)

    if session.is_a_new_day():
        printer.echo(f"✨ {formatter.date(date=session.date)}")
        printer.echo("✨ A new day starts, good luck!\n")

    if not ctx.invoked_subcommand:
        helper = _CLIHelper(session=session)
        exclude = [] if all else [TaskStatus.DELETED]
        helper.show_tasks(exclude=exclude)


@cli.command(help="Initialize hyperfocus config and database.")
@click.option(
    "--db-path",
    default=DEFAULT_DB_PATH,
    prompt=formatter.prompt("Database location"),
    help="Database file location.",
)
def init(db_path: str):
    config = Config(db_path=db_path)
    config.make_directory()
    config.save()
    printer.info(
        text=f"Config file created successfully in {config.file_path}",
        event=TaskEvents.INIT,
    )

    database.connect(db_path=config.db_path)
    database.init_models(MODELS)
    printer.info(
        text=f"Database initialized successfully in {config.db_path}",
        event=TaskEvents.INIT,
    )


@cli.command(help="Add a today task.")
def add():
    session = get_current_session()

    title = printer.ask("Task title")
    details = printer.ask("Task details (optional)", default="", show_default=False)

    task = session.daily_tracker.add_task(title=title, details=details)
    printer.success(
        text=formatter.task(task=task, show_prefix=True),
        event=TaskEvents.CREATED,
    )


@cli.command(help="Mark a task as done.")
@click.argument("task_id", required=False, type=int)
def done(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(
        task_id=task_id, status=TaskStatus.DONE, text="Mark task as done"
    )


@cli.command(help="Restore a task at initial status.")
@click.argument("task_id", required=False, type=int)
def reset(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(task_id=task_id, status=TaskStatus.TODO, text="Reset task")


@cli.command(help="Mark a task as block.")
@click.argument("task_id", required=False, type=int)
def block(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(task_id=task_id, status=TaskStatus.BLOCKED, text="Block task")


@cli.command(help="Mark a task as deleted (Deleted tasks won't appear in the list).")
@click.argument("task_id", required=False, type=int)
def delete(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    helper.update_task(task_id=task_id, status=TaskStatus.DELETED, text="Delete task")


@cli.command(help="Show task details.")
@click.argument("task_id", required=False, type=int)
def show(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    task_id = helper.check_task_id_or_ask(task_id=task_id, text="Show task details")

    task = helper.get_task(task_id=task_id)
    printer.task(task=task, show_details=True, show_prefix=True)


@cli.command(help="Copy task details into clipboard.")
@click.argument("task_id", required=False, type=int)
def copy(task_id: int):
    session = get_current_session()
    helper = _CLIHelper(session=session)

    task_id = helper.check_task_id_or_ask(task_id=task_id, text="Copy task details")

    task = helper.get_task(task_id=task_id)
    if not task.details:
        raise TaskError(
            f"Task {task_id} does not have details", event=TaskEvents.NOT_FOUND
        )

    pyperclip.copy(task.details)
    printer.success(text=f"Task {task_id} details copied to clipboard", event="copied")
