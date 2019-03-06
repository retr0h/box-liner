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

import docker

from boxliner import util


class Docker(object):
    def __init__(self, config):
        self._config = config
        self._client = docker.from_env()

    def exec_run(self, name, command):
        c = self._client.containers.get(name)

        return c.exec_run(cmd=command)

    def get_profiles(self, name):
        c = self._client.containers.get(name)
        try:
            labels = c.labels['com.retr0h.boxliner']
            labels_dict = util.safe_load(labels)
            print("D")
            print(labels_dict)

            return labels_dict['verifier']['profiles']
        except KeyError:
            msg = "Missing 'labels.com.retr0h.boxliner' from {}".format(
                self._config.compose_file)
            util.sysexit_with_message(msg)
