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

from boxliner import util


class Inspec(object):
    def __init__(self, config):
        self._config = config

    @property
    def stream(self):
        return True

    @property
    def log_level(self):
        # NOTE(retr0h): DEBUG seems way too verbose and not too useful
        # for general box-liner use.
        return 'INFO'

    def exec(self, profile, container_name):
        # debug on debug
        commands = [
            'inspec',
            'exec',
            '--log-level',
            self.log_level,
            profile,
            '-t',
            'docker://{}'.format(container_name),
        ]

        cmd = util.get_run_command(commands, env=self._config.env)
        util.run_command(cmd, stream=self.stream, debug=self._config.debug)
