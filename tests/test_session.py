import pytest

from hyperfocus.exceptions import SessionError
from hyperfocus.session import get_current_session


def test_session_not_in_click_context(mocker):
    mocker.patch("hyperfocus.session.click.get_current_context")

    with pytest.raises(
        SessionError,
        match="It appears that you are trying to invoke a command outside of the CLI context",
    ):
        get_current_session()
