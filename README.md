[![Build Status](http://img.shields.io/travis/retr0h/box-liner.svg?style=popout-square&logo=travis)](https://travis-ci.org/retr0h/box-liner)
[![Coverage](https://img.shields.io/codecov/c/github/retr0h/box-liner.svg?style=popout-square&logo=codecov)](https://codecov.io/gh/retr0h/box-liner)
[![PyPI](https://img.shields.io/pypi/v/box-liner.svg?style=popout-square&logo=python)](https://pypi.org/project/box-liner/)

# Box Liner

Box Liner is a tool which runs a suite of validation tests against the
specified containers.

Intended to test [Docker][1] containers post build and prior to publishing.
The container(s) lifecycle is managed through [Docker Compose][2], and
validation is currently handled by [Goss][3] with plans to swich to
[InSpec][4].

Tests are run local to the container, with plans to add external integration
tests in the future.

[1]: https://www.docker.com/
[2]: https://docs.docker.com/compose/
[3]: https://github.com/aelsabbahy/goss/
[4]: https://www.inspec.io/

## Install

    $ virtualenv .venv --no-site-packages
    $ source .venv/bin/activate
    $ pip install box-liner

## Usage

Create a new project, and modify the generated Docker Compose and Goss tests.
Reference Goss' full [documentation][1] for further details.

    $ box-liner init --project-name test-project

[3]: https://github.com/aelsabbahy/goss/blob/master/docs/manual.md

Validate the container.

    $ cd test-project
    $ box-liner validate --goss-binary /path/to/goss/binary

### Pass

![Pass](img/pass.png?raw=true "Pass")

### Fail

![Fail](img/fail.png?raw=true "Fail")

## Similar Tools

* [DGoss][1]

[1]: https://github.com/aelsabbahy/goss/tree/master/extras/dgoss

## License

MIT
