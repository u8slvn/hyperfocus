Commands
========

add
---

Add a task to the current working day.

Usage:

.. code-block:: bash

    hyf add [OPTIONS] <title>

- **<title>** The title description of your task.

Options:

- ``-d``, ``--details``  Allows to add some details to the task.
- ``-h``, ``help`` Command help.

Example:

.. code-block:: bash
    :caption: Add a simple task

    $ hyf add "Call John Doe."

.. code-block:: bash
    :caption: Add a task with details

    $ hyf add "Read the article about cats" -d
    >>> ? Task details: https://catsfunfacts.pet

config
------

Manage hyf configuration. It's currently used only to set up aliases, see the examples below.

Usage:

.. code-block:: bash

    hyf config [OPTIONS] <option> <value>

- **<option>** The option you want to set up within the config. It must follow this format: ``section.key``.
- **<value>** The value to set to the given field.

Options:

- ``--unset`` Unset an option from the config.
- ``--list``  Show the whole config.
- ``-h``, ``help`` Command help.

Example:

.. code-block:: shell
    :caption: Add an alias del for command delete

    $ hyf config alias.del delete

.. code-block:: shell
    :caption: Show the config

    $ hyf config --list

copy
----

Copy task details into clipboard.

Usage:

.. code-block:: bash

    hyf copy [OPTIONS] <id>

- **<id>** The task id which you want to copy the details from.

Options:

- ``-h``, ``help`` Command help.

Example:

.. code-block:: bash
    :caption: Copy details from task #3 into clipboard

    $ hyf copy 3

delete
------

Delete a task from the current day. **Hyperfocus** uses soft deletion by default, if you want to formally remove a task you need to use the `--force` option.

Usage:

.. code-block:: bash

    hyf delete [OPTIONS] <id>

- **<id>** The id of the task you want to delete. If you don't remember the id of the task, leave it empty, **Hyperfocus** will display you a little reminder.

Options:

- ``f``, ``--force`` Force a task deletion
- ``-h``, ``help`` Command help.

Example:

.. code-block:: bash
    :caption: Delete task #3.

    $ hyf delete 3

.. code-block:: bash
    :caption: Hard delete task #3.

    $ hyf delete 3 --force

init
----

log
---

reset
-----

show
----

stash
-----

status
------
