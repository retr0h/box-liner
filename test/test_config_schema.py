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

from boxliner import config
from boxliner import config_schema

pytestmark = pytest.mark.skip("Pending Implementation")


def test_validate():
    d = {
        'goss_file': '.test.yml',
        'goss_binary': '/usr/local/bin/goss-linux-amd64',
    }
    result = config_schema.ConfigSchema().load(d)
    x = {}

    assert x == result.errors
    assert isinstance(result.data, config.Config)


def test_validate_has_errors():
    d = {
        'goss_file': 3,
        'goss_binary': 4,
    }
    result = config_schema.ConfigSchema().load(d)
    x = {
        'goss_binary': ['Not a valid string.'],
        'goss_file': ['Not a valid string.'],
    }

    assert x == result.errors
