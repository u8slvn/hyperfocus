⚙️ Commands
===========

add
---

Add a task to the current working day. You can add a simple task or a task with details. If you want to add a task with details, you can use the `-d` option. If you want to add a task with multiple lines details, you can use the `-d -` option, **Hyperfocus** will open your default editor to write the details.

Usage:

.. code-block:: bash

    hyf add [OPTIONS] <title>

- **<title>** The title description of your task.

Options:

- ``-d``, ``--details``  Allows to add some details to the task.
- ``-b``, ``--bulk`` Open the editor and allows to add multiple tasks at once by writing one title per line. Note that you won't be able to fill details with the bulk mode.
- ``-h``, ``--help`` Command help.

Examples:

.. code-block:: bash
    :caption: Add a simple task

    hyf add "Call John Doe."

.. code-block:: bash
    :caption: Add a task with details

    hyf add "Read an article about cats" -d "https://catsfunfacts.pet"

.. code-block:: bash
    :caption: Add a task with multiple lines details

    hyf add "Do something with a lot of details" -d -

.. code-block:: bash
    :caption: Add multiple tasks at once

    hyf add --bulk

    # In the editor write one task per line
    Call John Doe
    Read some articles about dogs

config
------

Manage **Hyperfocus** configuration. It is currently exclusively meant to set up aliases, see the examples below.

Usage:

.. code-block:: bash

    hyf config [OPTIONS] <option> <value>

- **<option>** The option you want to set up within the config. It must follow this format: ``section.key``.
- **<value>** The value to set to the given field.

Options:

- ``--unset`` Unset an option from the config.
- ``--list``  Show the whole config.
- ``-h``, ``--help`` Command help.

Examples:

.. code-block:: shell
    :caption: Add an alias del for command delete

    hyf config alias.del delete

.. code-block:: shell
    :caption: Show the config

    hyf config --list

copy
----

Copy task details into clipboard.

Usage:

.. code-block:: bash

    hyf copy [OPTIONS] <id>

- **<id>** The task id which you want to copy the details from.

Options:

- ``-h``, ``--help`` Command help.

Example:

.. code-block:: bash
    :caption: Copy details from task #3 into clipboard

    hyf copy 3

delete
------

Delete one or more tasks from the current day. **Hyperfocus** uses soft deletion by default, if you are sure you want to remove a task, you need to use the `--force` option.

Usage:

.. code-block:: bash

    hyf delete [OPTIONS] <id>

- **<id>** The id of the task you want to delete. If you don't remember the id of the task, leave it empty, **Hyperfocus** will display you a little reminder.

Options:

- ``f``, ``--force`` Force a task deletion
- ``-h``, ``--help`` Command help.

Examples:

.. code-block:: bash
    :caption: Delete task #3.

    hyf delete 3

.. code-block:: bash
    :caption: Delete tasks #3 and #4.

    hyf delete 3 4

.. code-block:: bash
    :caption: Hard delete task #3.

    hyf delete 3 --force

done
----

Mark a task as done from the current working day.

Usage:

.. code-block:: bash

    hyf done [OPTIONS] <id>

- **<id>** The id of the task you want to mark ad done. If you don't remember the id of the task, leave it empty, **Hyperfocus** will display you a little reminder.

Options:

- ``-h``, ``--help`` Command help.

Examples:

.. code-block:: bash
    :caption: Mark task #3 as done.

    hyf done 3

.. code-block:: bash
    :caption: mark tasks #3 and #4 as done.

    hyf done 3 4

init
----

Initialize **Hyperfocus** config and database. This command is mandatory if you want to be able to use **Hyperfocus**. It can also be used as a reset.

Usage:

.. code-block:: bash

    hyf init [OPTIONS]

Options:

- ``-h``, ``--help`` Command help.

log
---

Show the whole tasks history.

Usage:

.. code-block:: bash

    hyf log [OPTIONS]

Options:

- ``-h``, ``--help`` Command help.

reset
-----

Reset a task status. Reset task will be set to *TODO*.

Usage:

.. code-block:: bash

    hyf reset [OPTIONS] <id>

- **<id>** The id of the task you want to reset.

Options:

- ``-h``, ``--help`` Command help.

Examples:

.. code-block:: bash
    :caption: Reset task #1

    hyf reset 1

.. code-block:: bash
    :caption: Reset tasks #1 and #2

    hyf reset 1 2

show
----

Show a task in detail with its history.

Usage:

.. code-block:: bash

    hyf show [OPTIONS] <id>

- **<id>** The id of the task you want to show.

Options:

- ``-h``, ``--help`` Command help.

Example:

.. code-block:: bash
    :caption: Show task #1 details and history.

    hyf show

stash
-----

Postpone a task by saving it for later.

stash apply
^^^^^^^^^^^

Pop all the stashed tasks to the current working day.

Usage:

.. code-block:: bash

    hyf stash apply [OPTIONS]

Options:

- ``-h``, ``--help`` Command help.

stash clear
^^^^^^^^^^^

Cleared the stashed tasks. All the removed tasks will be deleted.

Usage:

.. code-block:: bash

    hyf stash clear [OPTIONS]

Options:

- ``-h``, ``--help`` Command help.

stash list
^^^^^^^^^^

List all the stashed tasks.

Usage:

.. code-block:: bash

    hyf stash list [OPTIONS]

Options:

- ``-h``, ``--help`` Command help.

stash pop
^^^^^^^^^

Pop a stashed task into the current working day.

Usage:

.. code-block:: bash

    hyf stash pop [OPTIONS] <id>

- **<id>** The id of the stashed task you want to pop.

Options:

- ``-h``, ``--help`` Command help.

stash push
^^^^^^^^^^

Push a task from the current working day into the stashed list.

Usage:

.. code-block:: bash

    hyf stash push [OPTIONS] <id>

- **<id>** The id of the task you want to stash.

Options:

- ``-h``, ``--help`` Command help.

status
------

Show **Hyperfocus** current working day status. This is the default command called when calling `hyf`.

Usage:

.. code-block:: bash

    hyf status

Options:

- ``-h``, ``--help`` Command help.

Examples:

.. code-block:: bash
    :caption: Show current working day status

    hyf status


.. code-block:: bash
    :caption: Show current working day status

    hyf
