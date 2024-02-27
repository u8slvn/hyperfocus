from __future__ import annotations

import pytest

from hyperfocus.config.exceptions import ConfigError
from hyperfocus.config.policy import AliasPolicy
from hyperfocus.config.policy import ConfigPolicies
from hyperfocus.config.policy import ConfigPolicy
from hyperfocus.config.policy import CorePolicy


def test_option_policies(mocker):
    foo_policy = mocker.Mock(spec=ConfigPolicy)
    option_policies = ConfigPolicies(
        {
            "foo": foo_policy,
        }
    )

    option_policies.check_input("foo", mocker.sentinel.key, mocker.sentinel.value)
    option_policies.check_deletion("foo", mocker.sentinel.key)

    assert foo_policy.call_args_list == [
        mocker.call(mocker.sentinel.key),
        mocker.call(mocker.sentinel.key),
    ]
    foo_policy.return_value.check_input.assert_called_once_with(mocker.sentinel.value)
    foo_policy.return_value.check_deletion.assert_called_once()


def test_core_policy(test_dir):
    db_path = test_dir / "test_database.sqlite"
    core_policy = CorePolicy("database")

    core_policy.check_input(str(db_path))


def test_core_policy_forbidden_deletion_of_db_path():
    core_policy = CorePolicy("database")

    with pytest.raises(
        ConfigError, match="Deletion of config option 'core.database' is forbidden."
    ):
        core_policy.check_deletion()


def test_core_policy_fails_with_bad_db_path(dummy_dir):
    db_path = dummy_dir / "test_database.sqlite"
    core_policy = CorePolicy("database")

    with pytest.raises(
        ConfigError, match="Config option 'core.database' must be a valid path."
    ):
        core_policy.check_input(str(db_path))


def test_core_policy_fails_with_unknown_option():
    core_policy = CorePolicy("foo")

    with pytest.raises(ConfigError, match="Unknown config option 'core.foo'."):
        core_policy.check_input("bar")


def test_alias_policy(mocker):
    mocker.patch("hyperfocus.console.cli.hyf.get_commands", return_value=["foo"])
    alias_policy = AliasPolicy("bar")

    alias_policy.check_input("foo")


def test_alias_policy_fails_with_non_existing_command(mocker):
    mocker.patch("hyperfocus.console.cli.hyf.get_commands", return_value=["foo"])
    alias_policy = AliasPolicy("bar")

    with pytest.raises(
        ConfigError, match="Alias must referred to an existing command."
    ):
        alias_policy.check_input("foobar")


def test_alias_policy_fails_overriding_an_existing_command(mocker):
    mocker.patch("hyperfocus.console.cli.hyf.get_commands", return_value=["foo", "bar"])
    alias_policy = AliasPolicy("foo")

    with pytest.raises(ConfigError, match="Alias cannot override an existing command."):
        alias_policy.check_input("bar")
