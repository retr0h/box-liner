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

import plumbum
import pytest

from boxliner import util


@pytest.fixture
def _patched_red_text(mocker):
    return mocker.patch('boxliner.util.red_text')


@pytest.fixture
def _patched_print_debug(mocker):
    return mocker.patch('boxliner.util.print_debug')


@pytest.fixture
def _patched_print_boxliner_environment_vars(mocker):
    return mocker.patch('boxliner.util.print_boxliner_environment_vars')


def test_red_text():
    x = '\x1b[31mfoo\x1b[0m\x1b[39m'

    assert x == util.red_text('foo')


def test_cyan_text():
    x = '\x1b[36mfoo\x1b[0m\x1b[39m'

    assert x == util.cyan_text('foo')


def test_print_debug(capsys):
    util.print_debug('foo', {'foo': 'bar'})
    captured = capsys.readouterr()

    x = "\x1b[47m\x1b[1m\x1b[30mDEBUG: foo\x1b[0m\x1b[39m\n\x1b[30m\x1b[1m{'foo': 'bar'}\x1b[0m\x1b[39m\n"  # noqa: E501
    assert x == captured.out


def test_sysexit():
    with pytest.raises(SystemExit) as e:
        util.sysexit()

        assert 1 == e.value.code


def test_sysexit_with_custom_code():
    with pytest.raises(SystemExit) as e:
        util.sysexit(2)

    assert 2 == e.value.code


def test_sysexit_with_message(_patched_red_text):
    with pytest.raises(SystemExit) as e:
        util.sysexit_with_message('foo')

    assert 1 == e.value.code

    msg = 'ERROR: foo'
    _patched_red_text.assert_called_once_with(msg)


def test_sysexit_with_message_and_custom_code(_patched_red_text):
    with pytest.raises(SystemExit) as e:
        util.sysexit_with_message('foo', 2)

    assert 2 == e.value.code

    msg = 'ERROR: foo'
    _patched_red_text.assert_called_once_with(msg)


def test_safe_load():
    assert {'foo': 'bar'} == util.safe_load('foo: bar')


def test_safe_load_returns_empty_dict_on_empty_string():
    assert {} == util.safe_load('')


def test_safe_load_exits_when_cannot_parse():
    data = """
---
%foo:
""".strip()

    with pytest.raises(SystemExit) as e:
        util.safe_load(data)

    assert 1 == e.value.code


def test_get_run_command():
    commands = [
        'ls',
        '-l',
    ]
    x = '{} -l'.format(plumbum.local.which('ls'))

    assert x == str(util.get_run_command(commands))


def test_get_run_command_raises_when_command_not_found(_patched_red_text):
    commands = ['invalid']
    with pytest.raises(SystemExit) as e:
        util.get_run_command(commands)

    assert 1 == e.value.code
    msg = "ERROR: Command not found 'invalid'"
    _patched_red_text.assert_called_once_with(msg)


def test_run_command(_patched_print_debug,
                     _patched_print_boxliner_environment_vars):
    cmd = util.get_run_command(['echo', 'foo'])
    x = 'foo\n'

    assert x == util.run_command(cmd)

    assert not _patched_print_debug.called
    assert not _patched_print_boxliner_environment_vars.called


def test_run_command_streams_stdout(capsys):
    cmd = util.get_run_command(['echo', 'stdout'])
    util.run_command(cmd, stream=True)

    captured = capsys.readouterr()
    assert 'stdout\n' == captured.out


def test_run_command_streams_stderr(capsys):
    commands = [
        'python',
        '-c',
        'import sys; sys.stderr.write("stderr")',
    ]
    cmd = util.get_run_command(commands)
    util.run_command(cmd, stream=True)

    captured = capsys.readouterr()
    assert 'stderr\n' == captured.out


def test_run_command_with_debug(_patched_print_debug,
                                _patched_print_boxliner_environment_vars):
    cmd = util.get_run_command(['echo', 'foo'])
    util.run_command(cmd, debug=True)

    _patched_print_debug.assert_called_once_with('COMMAND', str(cmd))
    _patched_print_boxliner_environment_vars.assert_called_once_with(
        cmd.machine.env)


def test_run_command_raises_when_command_fails(_patched_red_text):
    commands = [
        'python',
        '-c',
        'import sys; sys.exit("stderr")',
    ]
    cmd = util.get_run_command(commands)
    with pytest.raises(SystemExit) as e:
        util.run_command(cmd)

    assert 1 == e.value.code
    msg = 'ERROR: Command failed to execute\n\nstderr\n'
    _patched_red_text.assert_called_once_with(msg)


def test_print_boxliner_environment_vars(mocker, _patched_print_debug):
    env = {
        'foo': 'bar',
        'BOXLINER_foo': 'foo',
        'BOXLINER_BAR': 'BAR',
    }
    util.print_boxliner_environment_vars(env)

    x = [
        mocker.call('BOXLINER ENVIRONMENT',
                    '---\nBOXLINER_BAR: BAR\nBOXLINER_foo: foo'),
        mocker.call('SHELL REPLAY', 'BOXLINER_BAR=BAR BOXLINER_foo=foo'),
    ]
    assert x == _patched_print_debug.mock_calls


def test_safe_dump():
    x = """
---
foo: bar
""".lstrip()

    assert x == util.safe_dump({'foo': 'bar'})
