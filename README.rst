csvhawk
=======

The name *csvsed* was already taken, so this is ... *csvhawk*, the CSV
stream editor.

Note that this software is very alpha, it has been created/used for one
specific goal only.


Usage
-----

::

    $ cat input.csv
    "Username","AccountId","Notes"
    "john","555","john was very verbose.
    overly verbose if you ask me."
    "amy","123"," amy likes spaces "

Get help with ``-h``::

    $ csvhawk -h
    usage: csvhawk [-h] [-w] [-d N] [FILE]

    CSV stream editor.

    positional arguments:
      FILE              the file to process

    optional arguments:
      -h, --help        show this help message and exit
      -w, --normalize   normalize whitepace: remove non-SP and collapse spaces
      -d N, --delete N  delete column N (by name)


Remove excess whitespace using ``-w``::

    $ cat input.csv | csvhawk -w
    "Username","AccountId","Notes"
    "john","555","john was very verbose. overly verbose if you ask me."
    "amy","123","amy likes spaces"

Remove columns using ``-d``::

    $ csvhawk -d Username -d Notes input.csv
    "AccountId"
    "555"
    "123"


License
-------

csvhawk is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, version 3 or any later version.
