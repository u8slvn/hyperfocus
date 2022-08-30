from hyperfocus.console.commands.add import add
from hyperfocus.console.commands.config import config
from hyperfocus.console.commands.copy import copy
from hyperfocus.console.commands.delete import delete
from hyperfocus.console.commands.done import done
from hyperfocus.console.commands.init import init
from hyperfocus.console.commands.log import log
from hyperfocus.console.commands.main import hyf
from hyperfocus.console.commands.reset import reset
from hyperfocus.console.commands.show import show
from hyperfocus.console.commands.stash import stash
from hyperfocus.console.commands.status import status


hyf.add_commands(
    [
        add,
        config,
        copy,
        delete,
        done,
        init,
        log,
        reset,
        show,
        stash,
        status,
    ]
)


def run() -> None:
    hyf()
