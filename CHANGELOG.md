# Changelog

## 1.0.0-alpha.1 (2022-08-16)

### Added:

* New style management with markup.
* Colored design for `config --list`.
* Add `stash` command group to manage tasks into stash box.
  * Add `stash pop` command.
  * Add `stash apply` command.
  * Add `stash list` command.
  * Add `stash clear` command.
* Add `--force` option to delete command to allow force deletion.

### Changed:

* Improved global architecture.
* New daily tasks progress bar style.
* Tasks are now listed by task id.

### Fixed:

* `hyf init` initialize the whole config path and create missing directory.

## 1.0.0-alpha.0 (2022-07-17)

* Add task details with history in `show` command.
* Rework unfinished tasks review system.
* Add progress bar to working day status.
* Minor design modifications on `new day` and `unfinished tasks` events.
* Add security check preventing bad config deletion.
* Commands `done`, `block`, `reset` and `delete` accept task id batches.

## 0.2.1 (2022-07-12)

* Fix config command `--list` option.

## 0.2.0 (2022-07-11)

* Add alias options in config.
* Add review of previous unfinished tasks on new day.
* Add status command.
* Add config command.
* Pretty print click exceptions.

## 0.1.1 (2022-07-05)

* Fix update status without passing task id as argument.

## 0.1.0 (2022-07-05)

* Initial release.
* Manage daily tasks with status.
* Copy task details to clipboard.
