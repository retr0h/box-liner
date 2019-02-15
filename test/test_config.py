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


def test_config_member(config_instance):
    x = {
        'containers': [{
            'name':
            'instance',
            'image':
            'solita/ubuntu-systemd:latest',
            'command':
            '/sbin/init',
            'goss_file':
            './test/test.yml',
            'goss_binary':
            '/Users/jodewey/Downloads/goss-linux-amd64',
        }]
    }

    assert x == config_instance.config


def test_containers_property(config_instance):
    assert isinstance(config_instance.containers[0], container.Container)


def test_containers_property_handles_missing_containers_dict(config_instance):
    pass
    # TODO(retr0h): Schema validate this.


def test_get_config(config_instance):
    # NOTE(retr0h): This is tested via the config member test.
    pass
