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

import io
import os

import pytest

from boxliner import util


def test_sysexit():
    with pytest.raises(SystemExit) as e:
        util.sysexit()

        assert 1 == e.value.code


def test_sysexit_with_custom_code():
    with pytest.raises(SystemExit) as e:
        util.sysexit(2)

    assert 2 == e.value.code


def test_sysexit_with_message(capsys):
    with pytest.raises(SystemExit) as e:
        util.sysexit_with_message('foo')

    assert 1 == e.value.code

    captured = capsys.readouterr()
    assert captured.out == '{}\n'.format(util.red_text('ERROR: foo'))


def test_sysexit_with_message_and_custom_code(capsys):
    with pytest.raises(SystemExit) as e:
        util.sysexit_with_message('foo', 2)

    assert 2 == e.value.code

    captured = capsys.readouterr()
    assert captured.out == '{}\n'.format(util.red_text('ERROR: foo'))


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


def test_open_file(temp_dir):
    path = os.path.join(temp_dir.strpath, 'foo')
    util.write_file(path, 'foo: bar')

    with util.open_file(path) as stream:
        try:
            file_types = (file, io.IOBase)
        except NameError:
            file_types = io.IOBase

        assert isinstance(stream, file_types)
