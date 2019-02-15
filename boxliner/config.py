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

from boxliner import container
from boxliner import util


class Config(object):
    """
    Box Liner searches the current directory for ``boxliner.yml`` and
    loads them into a ``Config`` class, which Box Liner operates upon.
    """

    def __init__(self, data, args, command_args):
        """
        Initialize a new config class and returns None.
        :param data: A string containing the config data to path to load.
        :param args: An optional dict of options, arguments and commands from
         the CLI.
        :param command_args: An optional dict of options passed to the
         subcommand from the CLI.
        :returns: None
        """
        self._data = data
        self.config = self._get_config()

    @property
    def containers(self):
        """
        Return a list of ``Container`` objects.
        :returns: list
        """
        return [container.Container(c) for c in self.config['containers']]

    def _get_config(self):
        """
        """
        return util.safe_load(self._data)
