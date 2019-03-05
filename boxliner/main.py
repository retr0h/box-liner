# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2019 John Dewey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from boxliner import config
from boxliner import util
from boxliner.driver import compose
from boxliner.driver import docker
from boxliner.validator import inspec


def main(args, command_args):
    __config = config.Config(args, command_args)
    __compose = compose.Compose(__config)
    __docker = docker.Docker()
    __inspec = inspec.Inspec(__config)

    __compose.up()

    containers = __compose.ps()
    statuses = {}
    for container in containers:
        name, _, _ = container
        profiles = __docker.get_profiles(name)
        for profile in profiles:
            try:
                __inspec.exec(profile, name)
            # TODO(retr0h): Handle better exception.
            except SystemExit:
                statuses.update({name: {'failed': True}})

    __compose.down()

    failed = [name for (name, status) in statuses.items() if status['failed']]
    if failed:
        msg = "Validation Failed on '{}'".format(', '.join(failed))
        util.sysexit_with_message(msg)
