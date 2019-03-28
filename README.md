# Box Liner

Box Liner is a tool which runs a suite of validation tests against the
specified containers.

Intended to test [Docker][1] containers post build and prior to publishing.
The container(s) lifecycle is managed through [Docker Compose][2], and
validation is handled by [InSpec][3].

Tests are run against local containers, and optionally the services they expose
through a "sidecar" container.

[1]: https://www.docker.com/
[2]: https://docs.docker.com/compose/
[3]: https://www.inspec.io/

## Where is it?

Unfortunately, this project has been moved in house.  Hopefully, we can release it
in the near future.
