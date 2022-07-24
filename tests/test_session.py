import datetime

import click
import pytest
from freezegun import freeze_time

from hyperfocus.config.config import Config
from hyperfocus.exceptions import SessionError
from hyperfocus.services import DailyTracker
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


def test_session_teardown(session):
    session.teardown()

    session._database.close.assert_called_once()


@freeze_time("2022-01-01")
def test_session_create(mocker):
    config = mocker.MagicMock(spec=Config, instance=True)
    mocker.patch(
        "hyperfocus.session.Config", spec=Config, **{"load.return_value": config}
    )
    daily_tracker = mocker.patch("hyperfocus.session.DailyTracker", spec=DailyTracker)
    daily_tracker.from_date.return_value.date = mocker.sentinel.date
    database = mocker.patch("hyperfocus.session.Session._database")

    session = Session.create()

    database.connect.assert_called_once()
    daily_tracker.from_date.assert_called_once_with(datetime.datetime(2022, 1, 1))
    assert session._config == config
    assert session.date == mocker.sentinel.date


def test_session_bind_context(mocker):
    context = mocker.create_autospec(click.Context)
    session = Session(mocker.MagicMock(), mocker.Mock())

    session.bind_context(context)

    assert context.obj == session
    context.call_on_close.assert_called_once_with(session.teardown)
