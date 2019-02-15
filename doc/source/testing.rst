Testing
=======

::

    $ virtualenv .venv --no-site-packages
    $ source .venv/bin/activate
    $ pip install -e .
    $ pip install -r requirements-doc.txt
    $ pip install -r requirements-test.txt
    $ pip install -r requirements.txt
    $ pip install tox

    $ tox
