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

import docker
import halo
import namesgenerator

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
        self._args = args
        self._command_args = command_args
        self._config = self._get_config()
        self._client = docker.from_env()
        # TODO(retr0h): Move to cli as override.
        self._goss_cmd = '/goss validate --color --format documentation'
        self._random_name = namesgenerator.get_random_name()

    @property
    def image(self):
        if self._command_args.get('image'):
            return self._command_args['image']
        return self._config['image']

    @property
    def command(self):
        if self._command_args.get('command'):
            return self._command_args['command']
        return self._config['command']

    @property
    def goss_file(self):
        if self._command_args.get('goss_file'):
            p = self._command_args['goss_file']
        else:
            p = self._config['goss_file']

        return os.path.abspath(p)

    @property
    def goss_binary(self):
        if self._command_args.get('goss_binary'):
            return self._command_args['goss_binary']
        return self._config['goss_binary']

    def validate(self):
        print('[{}]'.format(self._get_display_name()))
        try:
            container = self._run()
        except docker.errors.ImageNotFound as e:
            msg = "Image not Found\n\n{}".format(e)
            util.sysexit_with_message(msg)
        except docker.errors.APIError as e:
            msg = 'Failed to Run Container\n\n{}'.format(e)
            util.sysexit_with_message(msg)

        with halo.Halo(text='Validating', spinner='dots') as spinner:
            exit_code, output = container.exec_run(cmd=self._goss_cmd)
            if exit_code != 0:
                spinner.fail()
            else:
                spinner.succeed()

        with halo.Halo(text='Stopping', spinner='dots') as spinner:
            container.stop()
            spinner.succeed()

        with halo.Halo(text='Removing', spinner='dots') as spinner:
            container.remove()
            spinner.succeed()

        if exit_code != 0:
            print(output.decode('utf-8'))
            msg = 'Validation Failed'
            util.sysexit_with_message(msg)

    def _run(self):
        kwargs = {
            'volumes': {
                self.goss_binary: {
                    'bind': '/goss',
                    'mode': 'ro'
                },
                self.goss_file: {
                    'bind': '/goss.yaml',
                    'mode': 'ro'
                },
            },
            'command': self.command,
            'image': self.image,
            'detach': True,
            'remove': False,
            'name': self._random_name,
            'hostname': self._random_name,
        }

        with halo.Halo(text='Running', spinner='dots') as spinner:
            c = self._client.containers.run(**kwargs)
            spinner.succeed()

        return c

    def _get_config(self):
        return util.safe_load(self._data)

    def _get_display_name(self):
        return '{}@{}'.format(self._random_name, self.image)
