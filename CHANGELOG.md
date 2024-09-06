# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## Version 1.2.0 (2024-09-06)

### Added:

* Add `edit` command to edit task title and details.
* Task ids prompt accept multiple ids separated by space, for `done`, `reset` and `delete` commands.

### Changed:

* Default response option while reviewing unfinished tasks is now `y`.

## Version 1.1.0 (2024-08-11)

### Added:

* Add `--bulk` option for `add` command to add multiple tasks at once.

### Changed:

* Upgrade `add` command to accept inline task details. By @a-delannoy.
* Improve `add` command to accept multiple line task details.
* Colorized action in output message to improve readability.

## Version 1.0.0 (2024-06-12)

### Added:

* Add `-h` option for help.
* Add `log` command to show task log history.
* New style management with markup.
* Colored design for `config --list`.
* Add `stash` command group to manage tasks into stash box.
  * Add `stash pop` command.
  * Add `stash apply` command.
  * Add `stash list` command.
  * Add `stash clear` command.
* Add `--force` option to delete command to allow force deletion.
* Add task details with history in `show` command.
* Add progress bar to working day status.
* Add security check preventing bad config deletion.
* Commands `done`, `block`, `reset` and `delete` accept task id batches.
* Force color option for Windows.

### Changed:

* Improved global architecture.
* New daily tasks progress bar style.
* Tasks are now listed by task id.
* Rework unfinished tasks review system.
* Minor design modifications on `new day` and `unfinished tasks` events.

### Fixed:

* Log command must not show empty working days.
* Handle database connection errors.
* Alias cannot overwrite other commands.
* `hyf init` initialize the whole config path and create missing directory.

## Version 0.2.1 (2022-07-12)

* Fix config command `--list` option.

## Version 0.2.0 (2022-07-11)

* Add alias options in config.
* Add review of previous unfinished tasks on new day.
* Add status command.
* Add config command.
* Pretty print click exceptions.

## Version 0.1.1 (2022-07-05)

* Fix update status without passing task id as argument.

## Version 0.1.0 (2022-07-05)

* Initial release.
* Manage daily tasks with status.
* Copy task details to clipboard.
