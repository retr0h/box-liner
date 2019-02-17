[![Build Status](http://img.shields.io/travis/retr0h/box-liner.svg?style=popout-square&logo=travis)](https://travis-ci.org/retr0h/box-liner)
[![Coverage](https://img.shields.io/codecov/c/github/retr0h/box-liner.svg?style=popout-square&logo=codecov)](https://codecov.io/gh/retr0h/box-liner)
[![PyPI](https://img.shields.io/pypi/v/box-liner.svg?style=popout-square&logo=python)](https://pypi.org/project/box-liner/)

# Box Liner

Box Liner is a tool which runs a [Docker container][1] against a set of
[Goss][2] validation tests.


Intended to test docker container(s) post build and prior to publishing.  The
`boxliner.yml` file should be checked into the project which hosts the
Dockerfile, or repo which is responsible for building the container(s).

Box Liner is not intended to test the multi-container interactions.  This is
better served by a clustering/scheduling framework.  However, it can test
multiple containers individually.

[1]: https://www.docker.com/
[2]: https://github.com/aelsabbahy/goss

## Install

    $ virtualenv .venv --no-site-packages
    $ source .venv/bin/activate
    $ pip install box-liner

## Usage

Create a `boxliner.yml` with the following content.

```yaml
---
containers:
  - image: solita/ubuntu-systemd:latest
    command: /sbin/init
    goss_file: relative/path/to/test.yml
    goss_binary: /path/to/goss/binary/goss-linux-amd64
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
