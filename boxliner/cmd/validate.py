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

import click

from boxliner import config_schema
from boxliner import util


def _validate(c):
    result = config_schema.ConfigSchema().load(c)
    if result.errors:
        msg = 'Validation Failed\n\n{}'.format(result.errors)
        util.sysexit_with_message(msg)

    return result


@click.command()
@click.option(
    '--filename',
    default='boxliner.yml',
    help='Path to boxliner file.  Default boxliner.yml',
    type=click.File('r'))
@click.option('--image', help='Image to test.')
@click.option('--command', help='Command image should execute.')
@click.option('--goss-file', help='Path to Goss test file.')
@click.option('--goss-binary', help='Path to Goss binary.')
@click.option(
    '--goss-command',
    default='/goss validate --color --format documentation',
    help='Goss command to execute.')
@click.pass_context
def validate(ctx, filename, image, command, goss_file, goss_binary,
             goss_command):
    """ Run and validate the container. """

    args = ctx.obj.get('args')
    command_args = {
        'image': image,
        'command': command,
        'goss_file': goss_file,
        'goss_binary': goss_binary,
        'goss_command': goss_command,
        'debug': args.get('debug'),
    }

    f = filename.read()
    c = util.safe_load(f)
    filtered = {k: v for k, v in command_args.items() if v is not None}
    c.update(filtered)

    result = _validate(c)
    result.data.validate()
