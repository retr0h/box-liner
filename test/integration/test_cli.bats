#!/usr/bin/env bats
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

load 'vendor/test_helpers/bats-file/load'
load 'vendor/test_helpers/bats-support/load'

setup() {
	TEST_TEMP_DIR="$(temp_make)"
	TEST_VENV="${TEST_TEMP_DIR}/.venv"
    # NOTE(retr0h): GOSS_BINARY_PATH overrien by travis.
    # TODO(retr0h): The default location needs handled better.
	GOSS_BINARY_PATH="${GOSS_BINARY_PATH:-${HOME}/Downloads/goss-linux-amd64}"
}

teardown() {
	temp_del "${TEST_TEMP_DIR}"
}

@test "invoke box-liner without arguments prints usage" {
	run box-liner

    echo "status = ${status}"
    echo "output = ${output}"

	[ "${status}" -eq 0 ]
	echo "${output}" | grep "Docker container validation."
}

@test "invoke box-liner init subcommand" {
	cd "${TEST_TEMP_DIR}"
	run box-liner init --project-name bats-test

    echo "status = ${status}"
    echo "output = ${output}"

	[ "${status}" -eq 0 ]
	assert_file_exist ./bats-test/docker-compose.yml
	assert_file_exist ./bats-test/test/test.yml
}

@test "invoke box-liner validate subcommand" {
	cd "${TEST_TEMP_DIR}"
	run box-liner init --project-name bats-test

    echo "status = ${status}"
    echo "output = ${output}"

	[ "${status}" -eq 0 ]

	cd bats-test
	run box-liner validate --goss-binary "${GOSS_BINARY_PATH}"

    echo "status = ${status}"
    echo "output = ${output}"


	[ "${status}" -eq 0 ]
}
