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

import halo

from boxliner import util


class Compose(object):
    def __init__(self, config):
        self._config = config
        self._project_name = 'retr0h/box-liner'
        self._spinner = True

        # NOTE(retr0h): This should probably be moved outside the initializer.
        if config.debug:
            self.spinner = False

    @property
    def spinner(self):
        return self._spinner

    @spinner.setter
    def spinner(self, value):
        self._spinner = value

    @property
    def stream(self):
        if self._config.debug:
            return True
        return False

    @property
    def log_level(self):
        # NOTE(retr0h): DEBUG seems way too verbose and not too useful
        # for general box-liner use.
        return 'INFO'

    def up(self):
        commands = [
            'docker-compose',
            '--file',
            self._config.compose_file,
            '--project-name',
            self._project_name,
            '--log-level',
            self.log_level,
            'up',
            '--detach',
            '--no-recreate',
        ]
        with halo.Halo(
                text='Running Compose UP', spinner='dots',
                enabled=self.spinner) as s:
            cmd = util.get_run_command(commands, env=self._config.env)
            util.run_command(cmd, stream=self.stream, debug=self._config.debug)
            s.succeed()

    def ps(self):
        commands = [
            'docker-compose',
            '--file',
            self._config.compose_file,
            '--project-name',
            self._project_name,
            'ps',
        ]
        cmd = util.get_run_command(commands, env=self._config.env)
        out = util.run_command(cmd, debug=self._config.debug)
        # Name           Command     State   Ports
        # -----------------------------------------------
        lines = [i for i in out.split('\n')[2:] if i]

        return [line.split()[:3] for line in lines]

    def down(self):
        commands = [
            'docker-compose',
            '--file',
            self._config.compose_file,
            '--project-name',
            self._project_name,
            '--log-level',
            self.log_level,
            'down',
            '--remove-orphans',
        ]
        with halo.Halo(
                text='Running Compose DOWN', spinner='dots',
                enabled=self.spinner) as s:
            cmd = util.get_run_command(commands, env=self._config.env)
            util.run_command(cmd, stream=self.stream, debug=self._config.debug)
            s.succeed()
