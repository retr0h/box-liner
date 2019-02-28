# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2016 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import click
import click_completion

import boxliner

from boxliner import cmd

click_completion.init()


@click.group()
@click.option(
    '--debug/--no-debug',
    default=False,
    help='Enable or disable debug mode. Default is disabled.')
@click.version_option(version=boxliner.__version__)
@click.pass_context
def main(ctx, debug):  # pragma: no cover
    """
    \b
    .              .
    |-. ,-. . ,    |  . ,-. ,-. ,-.
    | | | |  X  -- |  | | | |-' |
    ^-' `-' ' `    `' ' ' ' `-' '

    Enable autocomplete issue:

      eval "$(_BOX_LINER_COMPLETE=source box-liner)"
    """
    ctx.obj = {}
    ctx.obj['args'] = {}
    ctx.obj['args']['debug'] = debug


main.add_command(cmd.validate.validate)
main.add_command(cmd.init.init)
