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

Create a `docker-compose.yml` file similar to the following:

```yaml
---
version: "3"
services:
  test-1:
    image: solita/ubuntu-systemd:latest
    hostname: test-1
    command: >-
      /sbin/init
    volumes:
      - ${BOXLINER_GOSS_FILE}:/goss.yaml:ro
      - ${BOXLINER_GOSS_BINARY}:/goss:ro
```

Create a `test.yml` with the tests to perform.  Reference Goss' full
[documentation][1] for further details.


```yaml
---
group:
  sshd:
    exists: true
    gid: 74
```

[3]: https://github.com/aelsabbahy/goss/blob/master/docs/manual.md

Validate the container.

    $ box-liner validate

### Pass

![Pass](img/pass.png?raw=true "Pass")

### Fail

![Fail](img/fail.png?raw=true "Fail")

## Similar Tools

* [DGoss][1]

[1]: https://github.com/aelsabbahy/goss/tree/master/extras/dgoss

## License

MIT
