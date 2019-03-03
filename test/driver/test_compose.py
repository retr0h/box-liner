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

from boxliner.driver import compose


@pytest.fixture
def _patched_get_run_command(mocker):
    return mocker.patch('boxliner.util.get_run_command')


@pytest.fixture
def _patched_run_command(mocker):
    m = mocker.patch('boxliner.util.run_command')
    m.return_value = mocker.Mock(spec=open)

    return m


@pytest.fixture
def _instance(config_instance):
    c = compose.Compose(config_instance)
    c.spinner = False  # NOTE(retr0h): Only used by tests.

    return c


def test_spinner_property(_instance):
    assert not _instance.spinner


def test_spinner_setter(_instance):
    _instance.spinner = True

    assert _instance.spinner


def test_stream_property(_instance):
    assert not _instance.stream


def test_stream_property_true_when_debug_on(_instance):
    _instance._config.debug = True

    assert _instance.stream


def test_log_level_property(_instance):
    x = 'INFO'

    assert x == _instance.log_level


def test_up(_instance, _patched_get_run_command, _patched_run_command):
    _patched_get_run_command.return_value = 'up command to execute'
    _instance.up()

    x = [
        'docker-compose',
        '--file',
        _instance._config.compose_file,
        '--project-name',
        _instance._project_name,
        '--log-level',
        _instance.log_level,
        'up',
        '--detach',
        '--no-recreate',
    ]
    _patched_get_run_command.assert_called_once_with(
        x, env=_instance._config.env)
    _patched_run_command.assert_called_once_with(
        'up command to execute',
        stream=False,
        debug=False,
    )


def test_ps(_instance, _patched_get_run_command, _patched_run_command):
    _patched_get_run_command.return_value = 'ps command to execute'
    _patched_run_command.return_value = """
Name           Command     State   Ports
-----------------------------------------------
instance-1     command     Up
instance-2     command     Up
""".lstrip()
    result = _instance.ps()

    x = [
        'docker-compose',
        '--file',
        _instance._config.compose_file,
        '--project-name',
        _instance._project_name,
        'ps',
    ]
    _patched_get_run_command.assert_called_once_with(
        x, env=_instance._config.env)
    _patched_run_command.assert_called_once_with(
        'ps command to execute',
        debug=False,
    )

    x = [
        ['instance-1', 'command', 'Up'],
        ['instance-2', 'command', 'Up'],
    ]
    assert x == result


def test_down(_instance, _patched_get_run_command, _patched_run_command):
    _patched_get_run_command.return_value = 'down command to execute'
    _instance.down()

    x = [
        'docker-compose',
        '--file',
        _instance._config.compose_file,
        '--project-name',
        _instance._project_name,
        '--log-level',
        _instance.log_level,
        'down',
        '--remove-orphans',
    ]

    _patched_get_run_command.assert_called_once_with(
        x, env=_instance._config.env)
    _patched_run_command.assert_called_once_with(
        'down command to execute',
        stream=False,
        debug=False,
    )
