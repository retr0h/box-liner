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

import pytest

from boxliner import config


@pytest.fixture
def _data():
    return """
image: solita/ubuntu-systemd:latest
command: /sbin/init
goss_file: ./test/test.yml
goss_binary: /Users/jodewey/Downloads/goss-linux-amd64
"""


@pytest.fixture
def _args():
    return {}


@pytest.fixture
def _command_args():
    return {}


@pytest.fixture
def _instance(_data, _args, _command_args):
    return config.Config(_data, _args, _command_args)


def test_name_property(_instance):
    pass


def test_image_property(_instance):
    x = 'solita/ubuntu-systemd:latest'

    assert x == _instance.image


def test_command_property(_instance):
    x = '/sbin/init'

    assert x == _instance.command


def test_goss_file_property(_instance):
    x = os.path.abspath('test/test.yml')

    assert x == _instance.goss_file


def test_goss_binary_property(_instance):
    x = '/Users/jodewey/Downloads/goss-linux-amd64'

    assert x == _instance.goss_binary


def test_validate(_instance):
    pass
    #  _instance.validate()
