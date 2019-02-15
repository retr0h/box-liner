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

from boxliner import util


class Container(object):
    """
    A class to ease the working with containers.
    """

    def __init__(self, d):
        """
        Initialize a new ``Container`` class and returns None.
        :param d: A dict containing the container to initalize' data.
        :return: None
        """
        self._d = d
        self._client = docker.from_env()
        self._goss_cmd = '/goss validate --color --format documentation'

    @property
    def name(self):
        return self._d['name']

    @property
    def container_name(self):
        return '{}@{}'.format(self.name, self.image)

    @property
    def image(self):
        return self._d['image']

    @property
    def command(self):
        return self._d['command']

    @property
    def goss_file(self):
        return os.path.abspath(self._d['goss_file'])

    @property
    def goss_binary(self):
        return os.path.abspath(self._d['goss_binary'])

    def validate(self):
        container = self._run()

        msg = 'validating container:{}'.format(self.container_name)
        with halo.Halo(text=msg, spinner='dots') as spinner:
            exit_code, output = container.exec_run(cmd=self._goss_cmd)
            if exit_code != 0:
                spinner.fail()
            else:
                spinner.succeed()

        msg = 'Stopping container:{}'.format(self.container_name)
        with halo.Halo(text=msg, spinner='dots') as spinner:
            container.stop()
            spinner.succeed()

        msg = 'Removing container:{}'.format(self.container_name)
        with halo.Halo(text=msg, spinner='dots') as spinner:
            container.remove()
            spinner.succeed()

        if exit_code != 0:
            print(output.decode('utf-8'))
            msg = 'validation failed'
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
            'name': self.name,
            'hostname': self.name,
        }

        msg = 'Running container:{}'.format(self.container_name)
        with halo.Halo(text=msg, spinner='dots') as spinner:
            c = self._client.containers.run(**kwargs)
            spinner.succeed()

        return c
