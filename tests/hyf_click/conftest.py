import click
import pytest

from hyperfocus.console.core.group import AliasGroup
from hyperfocus.exceptions import HyperfocusException


@pytest.fixture(scope="session")
def hyf_group():
    @click.group(cls=AliasGroup, invoke_without_command=True)
    @click.pass_context
    def test_cli(ctx):
        if not ctx.invoked_subcommand:
            raise HyperfocusException("Test group error")

    @test_cli.command()
    def alias():
        click.echo("alias")

    return test_cli
