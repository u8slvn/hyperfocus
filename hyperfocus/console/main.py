from hyperfocus.console.commands.add import add
from hyperfocus.console.commands.config import config
from hyperfocus.console.commands.copy import copy
from hyperfocus.console.commands.delete import delete
from hyperfocus.console.commands.done import done
from hyperfocus.console.commands.hyf import hyf
from hyperfocus.console.commands.init import init
from hyperfocus.console.commands.reset import reset
from hyperfocus.console.commands.show import show
from hyperfocus.console.commands.status import status


hyf.add_commands(  # type: ignore
    [
        add,
        config,
        copy,
        delete,
        done,
        init,
        reset,
        show,
        status,
    ]
)


def cli():
    hyf()
