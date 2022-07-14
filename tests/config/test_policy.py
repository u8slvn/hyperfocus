import pytest

from hyperfocus.config.exceptions import ConfigError
from hyperfocus.config.policy import (
    AliasPolicy,
    CorePolicy,
    OptionPolicies,
    OptionPolicy,
)


def test_option_policies(mocker):
    foo_policy = mocker.Mock(spec=OptionPolicy)
    option_policies = OptionPolicies(
        {
            "foo": foo_policy,
        }
    )

    option_policies.check_input("foo", mocker.sentinel.key, mocker.sentinel.value)
    option_policies.check_input("bar", mocker.sentinel.key, mocker.sentinel.value)

    foo_policy.assert_called_once_with(mocker.sentinel.key, mocker.sentinel.value)
    foo_policy.return_value.validate.assert_called_once()


def test_core_policy(test_dir):
    db_path = test_dir / "test_database.sqlite"
    core_policy = CorePolicy("database", str(db_path))

    core_policy.validate()


def test_core_policy_fails_with_bad_db_path(dummy_dir):
    db_path = dummy_dir / "test_database.sqlite"
    core_policy = CorePolicy("database", str(db_path))

    with pytest.raises(
        ConfigError, match="Config option 'core.database' must be a valid path."
    ):
        core_policy.validate()


def test_core_policy_fails_with_unknown_option():
    core_policy = CorePolicy("foo", "bar")

    with pytest.raises(ConfigError, match="Unknown config option 'core.foo'."):
        core_policy.validate()


def test_alias_policy(mocker):
    mocker.patch("hyperfocus.cli.get_commands", return_value=["foo"])
    alias_policy = AliasPolicy("bar", "foo")

    alias_policy.validate()


def test_alias_policy_fails_with_non_existing_command(mocker):
    mocker.patch("hyperfocus.cli.get_commands", return_value=["foo"])
    alias_policy = AliasPolicy("bar", "foobar")

    with pytest.raises(
        ConfigError, match="Alias must referred to an existing command name."
    ):
        alias_policy.validate()
