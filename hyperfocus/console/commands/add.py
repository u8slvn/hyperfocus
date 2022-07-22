import click

from hyperfocus.console.commands.task import AddTaskCmd
from hyperfocus.session import Session, get_current_session


@click.command(help="Add task to current working day")
@click.argument("title", metavar="<title>", type=click.STRING)
@click.option("-d", "--details", "add_details", is_flag=True, help="add task details")
def add(title: str, add_details: bool) -> Session:
    session = get_current_session()
    AddTaskCmd(session).execute(title=title, add_details=add_details)

    return session
