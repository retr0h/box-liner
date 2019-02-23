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

import os


class Config(object):
    """
    Box Liner searches the current directory for ``boxliner.yml`` and
    loads them into a ``Config`` class, which Box Liner operates upon.
    """

    def __init__(self, args, command_args):
        """
        Initialize a new config class and returns None.
        :param config: A dict containing the config data.
        :returns: None
        """
        self._args = args
        self._command_args = command_args
        self._debug = self._args.get('debug')

    @property
    def compose_file(self):
        return os.path.abspath(self._command_args['compose_file'])

    @property
    def goss_file(self):
        return os.path.abspath(self._command_args['goss_file'])

    @property
    def goss_binary(self):
        return self._command_args['goss_binary']

    @property
    def goss_command(self):
        return self._command_args['goss_command']

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def env(self):
        env = os.environ.copy()
        env.update({
            'BOXLINER_GOSS_FILE': self.goss_file,
            'BOXLINER_GOSS_BINARY': self.goss_binary,
        })

        return env
