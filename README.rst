NicBot - Discord Bot
=====================

.. contents:: Table of Contents

Introduction
-------------

NicBot is a bot that runs on Discord.


Technologies Used
------------------

- `discord.py <https://github.com/rapptz/discord.py>`_

Project Status
---------------

This project is currently in its *early stages of development*.


Version Naming
---------------

This library uses semantic versioning:

.. code:: txt

  MAJOR.MINOR.PATCH

Where an increment in:

* ``MAJOR`` = Incompatible changes (i.e., code may need to be updated).
* ``MINOR`` = Backwards compatible feature changes.
* ``PATCH`` = Backwards compatible bug fixes.


Getting Started
----------------

- Install the *discord.py* library.

.. code:: console

  $ pip install -U discord.py

- Fill out `config.template.json <./nicbot/config/config.template.json>`
  then rename it to *config.json*.

- To run the bot, run `launcher.py <./launcher.py>`_ from the root directory.

.. code:: console

  $ python launcher.py

- The bot should now display *Online* on Discord.

Bug/Feature Request
--------------------

If you find a bug (program failed to run and/or gave undesired results)
or you just want to request a feature, kindly open a new issue
`here <https://github.com/nicdgonzalez/NicBot/issues>`_.


Contributing
-------------

Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

- `Fork <https://github.com/nicdgonzalez/NicBot/fork>`_ the repository and create a new branch.

.. code:: console

  $ git clone "https://github.com/{username}/{respository}.git"
  $ cd {respository}
  $ git checkout -b "improve-feature"

- Make the appropriate changes and stage the modified files.

.. code:: console

  $ git add <changed file(s)>

- Commit the changes.

.. code:: console

  $ git commit -m "Improve feature."

- Push to the new branch.

.. code:: console

  $ git push "origin" "improve-feature"

- Create a `Pull Request <https://github.com/nicdgonzalez/NicBot/pulls>`_.
