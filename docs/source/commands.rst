Commands
========

add
---

Add a task to the current working day.

Usage:

.. code-block:: bash

    hyf add [OPTIONS] <title>

- **<title>** the title description of your task.

Options:

- ``-d``, ``--details``  Allows to add some details to the task.

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

Manage hyf configuration. It's actually used only to set up aliases, see the examples below.

Usage:

.. code-block:: bash

    hyf config [OPTIONS] <option> <value>

Options:

- ``--unset`` Unset an option
- ``--list``  Show the whole config

Example:

.. code-block:: shell

hyf config alias.del delete

copy
----

delete
------

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
