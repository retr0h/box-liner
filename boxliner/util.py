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
import sys

import colorama
import plumbum
import yaml

colorama.init(autoreset=True)


def color_text(color, msg):
    return '{}{}{}{}'.format(color, msg, colorama.Style.RESET_ALL,
                             colorama.Fore.RESET)


def red_text(msg):
    return color_text(colorama.Fore.RED, msg)


def cyan_text(msg):
    return color_text(colorama.Fore.CYAN, msg)


def print_debug(title, data):
    title = 'DEBUG: {}'.format(title)
    colors = [
        colorama.Back.WHITE,
        colorama.Style.BRIGHT,
        colorama.Fore.BLACK,
    ]
    print(color_text(''.join(colors), title))

    colors = [
        colorama.Fore.BLACK,
        colorama.Style.BRIGHT,
    ]
    print(color_text(''.join(colors), data))


def sysexit(code=1):
    sys.exit(code)


def sysexit_with_message(msg, code=1):
    print(red_text('ERROR: {}'.format(msg)))
    sysexit(code)


def safe_load(string):
    """
    Parse the provided string returns a dict.
    :param string: A string to be parsed.
    :return: dict
    """
    try:
        return yaml.safe_load(string) or {}
    except yaml.scanner.ScannerError as e:
        sysexit_with_message(str(e))


def get_run_command(commands, env=os.environ):
    __cmd = plumbum.local
    __cmd.env = env
    try:
        for partial in commands:
            __cmd = __cmd[partial]

        return __cmd
    except plumbum.CommandNotFound as e:
        msg = "Command not found '{}'".format(e.program)
        sysexit_with_message(msg)


def run_command(cmd, stream=False, debug=False):
    if debug:
        print()
        print_debug('COMMAND', str(cmd))
        print_boxliner_environment_vars(cmd.machine.env)
        print()
    try:
        if stream:
            for stdout, stderr in cmd.popen().iter_lines():
                if stdout:
                    print(stdout)
                if stderr:
                    print(stderr)
            return
        return cmd()
    except plumbum.commands.processes.ProcessExecutionError as e:
        msg = 'Command failed to execute\n\n{}'.format(e.stderr)
        sysexit_with_message(msg)


def print_boxliner_environment_vars(env):
    boxliner_env = {k: v for (k, v) in env.items() if 'BOXLINER_' in k}
    print_debug('BOXLINER ENVIRONMENT', safe_dump(boxliner_env).rstrip())
    print_debug(
        'SHELL REPLAY', " ".join(
            ["{}={}".format(k, v) for (k, v) in sorted(boxliner_env.items())]))


def safe_dump(data):
    return yaml.dump(data, default_flow_style=False, explicit_start=True)
