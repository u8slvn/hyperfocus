import datetime
from functools import partial

import click
import pytest
from freezegun import freeze_time

from hyperfocus.config.config import Config
from hyperfocus.exceptions import SessionError
from hyperfocus.session import Session, get_current_session


def test_get_current_session(mocker):
    ctx = mocker.Mock(spec=click.Context, instance=True)
    ctx.obj = mocker.Mock(spec=Session, instance=True)
    mocker.patch("hyperfocus.session.click.get_current_context", return_value=ctx)

    session = get_current_session()

    assert session == ctx.obj


def test_get_current_session_with_no_click_context(mocker):
    mocker.patch("hyperfocus.session.click.get_current_context")

    with pytest.raises(
        SessionError,
        match=(
            "It appears that you are trying to invoke a command outside "
            "of the CLI context"
        ),
    ):
        _ = get_current_session()


def test_session_bind_context(mocker, test_session):
    ctx = mocker.Mock(spec=click.Context, instance=True)

    test_session.bind_context(ctx)

    assert ctx.obj == test_session
    ctx.call_on_close.assert_called_once_with(test_session.teardown)


def test_session_register_callback_commands(test_session):
    callback1 = partial(int, "249")
    callback2 = partial(int, "417")

    test_session.register_callback(callback1)
    test_session.register_callback(callback2)

    result = sum([callback() for callback in test_session.callback_commands])
    assert result == 666


def test_session_teardown(test_session):
    test_session.teardown()

    test_session._database.close.assert_called_once()


@freeze_time("2022-01-01")
def test_session_init(mocker):
    config = mocker.MagicMock(spec=Config, instance=True)
    mocker.patch(
        "hyperfocus.session.Config", spec=Config, **{"load.return_value": config}
    )
    database = mocker.patch("hyperfocus.session.Session._database")

    session = Session()

    database.connect.assert_called_once()
    assert session._config == config
    assert session.date == datetime.date(2022, 1, 1)
    assert session.callback_commands == []
