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

import click

from boxliner import config
from boxliner import util


@click.command()
@click.option('--image', help='Image to test.')
@click.option('--command', help='Command image should execute.')
@click.option('--goss-file', help='Path to Goss test file.')
@click.option('--goss-binary', help='Path to Goss binary.')
@click.pass_context
def validate(ctx, image, command, goss_file, goss_binary):
    """ Run and validate the container. """

    args = ctx.obj.get('args')
    command_args = {
        'image': image,
        'command': command,
        'goss_file': goss_file,
        'goss_binary': goss_binary,
    }
    filename = args.get('filename')
    _setup(filename)

    with util.open_file(filename) as stream:
        c = config.Config(stream.read(), args, command_args)
        c.validate()


def _setup(filename):
    if not os.path.exists(filename):
        msg = 'Unable to find {}. Exiting.'.format(filename)
        util.sysexit_with_message(msg)
