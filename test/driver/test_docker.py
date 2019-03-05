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

from boxliner.driver import docker


@pytest.fixture
def _patched_docker_containers_get(mocker):
    return mocker.patch('docker.models.containers.ContainerCollection.get')


@pytest.fixture
def _instance(config_instance):
    return docker.Docker(config_instance)


def test_exec_run(_instance, _patched_docker_containers_get, mocker):
    _patched_docker_containers_get.return_value = mocker.Mock(
        exec_run=mocker.Mock(return_value='foo'))
    x = 'foo'

    assert x == _instance.exec_run('foo', 'bar')


def test_get_profiles(_instance, _patched_docker_containers_get, mocker):
    verifier_data = """
verifier:
  profiles:
    - foo
    - bar
    - baz
"""
    patched_labels = mocker.Mock().return_value = {
        'com.retr0h.boxliner': verifier_data
    }
    _patched_docker_containers_get.return_value = mocker.Mock(
        labels=patched_labels)
    x = [
        'foo',
        'bar',
        'baz',
    ]

    assert x == _instance.get_profiles('foo')


def test_get_profiles_handles_missing_verifier_data(
        _instance, _patched_docker_containers_get, mocker):
    _patched_docker_containers_get.return_value = mocker.Mock(labels={})
    _patched_sysexit_with_message = mocker.patch(
        'boxliner.util.sysexit_with_message')

    _instance.get_profiles('foo')

    msg = "Missing 'labels.com.retr0h.boxliner' from {}".format(
        _instance._config.compose_file)
    _patched_sysexit_with_message.assert_called_once_with(msg)
