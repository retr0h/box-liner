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


def test_compose_file_property(config_instance):
    x = os.path.abspath('compose_file')

    assert x == config_instance.compose_file


def test_goss_file_property(config_instance):
    x = os.path.abspath('goss_file')

    assert x == config_instance.goss_file


def test_goss_binary_property(config_instance):
    x = 'goss_binary'

    assert x == config_instance.goss_binary


def test_goss_command_property(config_instance):
    x = 'goss_command'

    assert x == config_instance.goss_command


def test_debug_property(config_instance):
    assert not config_instance.debug


def test_debug_setter(config_instance):
    config_instance.debug = True

    assert config_instance.debug


def test_env_property(config_instance):
    env = os.environ.copy()
    env.update({
        'BOXLINER_GOSS_FILE': os.path.abspath('goss_file'),
        'BOXLINER_GOSS_BINARY': 'goss_binary',
    })

    assert env == config_instance.env
