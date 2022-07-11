from __future__ import annotations

import sys

import click

from hyperfocus import __app_name__, __version__, formatter
from hyperfocus.commands.cmd_config import ConfigCommand
from hyperfocus.commands.cmd_init import InitCommand
from hyperfocus.commands.cmd_new_day import NewDayCommand
from hyperfocus.commands.cmd_status import StatusCommand
from hyperfocus.commands.cmd_task import (
    AddTaskCommand,
    CopyCommand,
    ShowTaskCommand,
    UpdateTaskCommand,
)
from hyperfocus.database.models import TaskStatus
from hyperfocus.hyf_click.core import HyfGroup
from hyperfocus.hyf_click.parameters import NotRequired, NotRequiredIf
from hyperfocus.locations import DEFAULT_DB_PATH
from hyperfocus.session import Session, get_current_session


@click.group(cls=HyfGroup, help="Minimalist task manager")
@click.version_option(
    version=__version__, prog_name=__app_name__, help="Show the version"
)
@click.pass_context
def hyf(ctx: click.Context) -> None:
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    session = Session()
    session.bind_context(ctx=ctx)

    NewDayCommand(session).execute()


@hyf.result_callback()
def process_session(session: Session | None, **_):
    if session is None:
        return

    for callback_commands in session.callback_commands:
        callback_commands()


@hyf.command(help="Initialize hyperfocus config and database")
@click.option(
    "--db-path",
    default=DEFAULT_DB_PATH,
    prompt=formatter.prompt("Database location"),
    help="Database file location",
)
def init(db_path: str) -> None:
    InitCommand().execute(db_path=db_path)


@hyf.command(help="Show current working day status")
def status() -> Session:
    session = get_current_session()
    StatusCommand(session).execute()

    return session


@hyf.command(help="Add task to current working day")
@click.argument("title", metavar="<title>", type=click.STRING)
@click.option("-d", "--details", "add_details", is_flag=True, help="add task details")
def add(title: str, add_details: bool) -> Session:
    session = get_current_session()
    AddTaskCommand(session).execute(title=title, add_details=add_details)

    return session


@hyf.command(help="Mark task as done")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def done(task_id: int | None) -> Session:
    session = get_current_session()
    UpdateTaskCommand(session).execute(
        task_id=task_id, status=TaskStatus.DONE, text="Validate task"
    )

    return session


@hyf.command(help="Reset task as todo")
@click.argument("task_id", metavar="<id>", required=False, type=int)
def reset(task_id: int | None) -> Session:
    session = get_current_session()
    UpdateTaskCommand(session).execute(
        task_id=task_id, status=TaskStatus.TODO, text="Reset task"
    )

    return session


@hyf.command(help="Mark task as blocked")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def block(task_id: int | None) -> Session:
    session = get_current_session()
    UpdateTaskCommand(session).execute(
        task_id=task_id, status=TaskStatus.BLOCKED, text="Block task"
    )

    return session


@hyf.command(help="Delete given task")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def delete(task_id: int | None) -> Session:
    session = get_current_session()
    UpdateTaskCommand(session).execute(
        task_id=task_id, status=TaskStatus.DELETED, text="Delete task"
    )

    return session


@hyf.command(help="Show task details")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def show(task_id: int | None) -> Session:
    session = get_current_session()
    ShowTaskCommand(session).execute(task_id=task_id)

    return session


@hyf.command(help="Copy task details into clipboard")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def copy(task_id: int | None) -> Session:
    session = get_current_session()
    CopyCommand(session).execute(task_id=task_id)

    return session


@hyf.command(help="Get and set options")
@click.argument(
    "option",
    cls=NotRequiredIf,
    not_required_if=["list_"],
    metavar="<option>",
    type=click.STRING,
)
@click.argument(
    "value",
    cls=NotRequiredIf,
    not_required_if=["list_", "unset"],
    metavar="<value>",
    type=click.STRING,
)
@click.option(
    "--unset",
    cls=NotRequired,
    not_required=["value", "list_"],
    is_flag=True,
    help="Unset an option",
)
@click.option(
    "--list",
    "list_",
    cls=NotRequired,
    not_required=["option", "value", "unset"],
    is_flag=True,
    help="Show the whole config",
)
def config(option: str | None, value: str | None, list_: bool, unset: bool) -> Session:
    session = get_current_session()
    ConfigCommand(session).execute(option=option, value=value, list_=list_, unset=unset)

    return session


def get_commands() -> list[str]:
    return [command for command in hyf.commands.keys()]
