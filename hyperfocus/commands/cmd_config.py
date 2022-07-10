from __future__ import annotations

from hyperfocus.commands import SessionHyperfocusCommand, printer


class ConfigCommand(SessionHyperfocusCommand):
    def execute(
        self, option: str | None, value: str | None, list_: bool, unset: bool
    ) -> None:
        if list_:
            self._show_config()
        elif unset and option is not None:
            self._delete_option(option=option)
        elif option is not None and value is not None:
            self._edit_option(option=option, value=value)

    def _show_config(self) -> None:
        for option, value in self._session.config.options.items():
            printer.echo(f"{option} = {value}")

    def _save_config(self) -> None:
        self._session.config.save()
        printer.success("Config updated", event="success")

    def _delete_option(self, option: str) -> None:
        del self._session.config[option]
        self._save_config()

    def _edit_option(self, option: str, value) -> None:
        self._session.config[option] = value
        self._save_config()
