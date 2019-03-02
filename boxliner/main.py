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


def main(args, command_args):
    __config = config.Config(args, command_args)
    __compose = compose.Compose(__config)
    __docker = docker.Docker()
    __compose.up()

    containers = __compose.ps()
    statues = []
    for container in containers:
        name, _, _ = container
        exit_code, output = __docker.exec_run(name, __config.goss_command)
        statues.append([name, exit_code, output])

    for status in statues:
        name, exit_code, output = status
        msg = '--> {}'.format(util.cyan_text(name))
        print(msg)

        if exit_code != 0:
            print(output.decode('utf-8'))

    __compose.down()

    if exit_code != 0:
        msg = 'Validation Failed'
        util.sysexit_with_message(msg)
