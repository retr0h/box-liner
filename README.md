[![Build Status](http://img.shields.io/travis/retr0h/box-liner.svg?style=popout-square&logo=travis)](https://travis-ci.org/retr0h/box-liner)
[![Coverage](https://img.shields.io/codecov/c/github/retr0h/box-liner.svg?style=popout-square&logo=codecov)](https://codecov.io/gh/retr0h/box-liner)
[![PyPI](https://img.shields.io/pypi/v/box-liner.svg?style=popout-square&logo=python)](https://pypi.org/project/box-liner/)

# Box Liner

Box Liner is a tool which runs a [Docker container][1] against a set of
[Goss][2] validation tests.

[1]: https://www.docker.com/
[2]: https://github.com/aelsabbahy/goss

## Install

    $ virtualenv .venv --no-site-packages
    $ source .venv/bin/activate
    $ pip install box-liner

## Usage

    $ box-liner validate

## Caveats

* Supports only Docker at this time.

## Similar Tools

* [DGoss][1]

[1]: https://github.com/aelsabbahy/goss/tree/master/extras/dgoss

## License

MIT
