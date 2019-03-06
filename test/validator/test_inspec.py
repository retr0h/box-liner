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

import pytest

from boxliner.validator import inspec


@pytest.fixture
def _instance(config_instance):
    return inspec.Inspec(config_instance)


def test_stream_property(_instance):
    assert _instance.stream


def test_log_level_property(_instance):
    x = 'INFO'

    assert x == _instance.log_level


def test_exec(_instance, patched_get_run_command, patched_run_command):
    patched_get_run_command.return_value = 'exec command to execute'
    _instance.exec('profile', 'container_name')

    x = [
        'inspec',
        'exec',
        '--log-level',
        'INFO',
        'profile',
        '-t',
        'docker://container_name',
    ]
    patched_get_run_command.assert_called_once_with(
        x, env=_instance._config.env)
    patched_run_command.assert_called_once_with(
        'exec command to execute',
        stream=True,
        debug=False,
    )
