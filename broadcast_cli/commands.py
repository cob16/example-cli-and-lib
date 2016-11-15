import os
import tempfile
from operator import methodcaller
from subprocess import call
from urllib.parse import urlparse

import begin
from broadcast_cli import broadcast_printer as print_field
from clint import piped_in
from clint.textui import prompt, puts, colored

from .actions import Actions
from .utils import isMessageBody

_in_data = ''
_a = None


@begin.subcommand
def send(message: 'set the message body' = None):
    """Sends a new broadcast"""
    if message is None:
        EDITOR = os.environ.get('EDITOR', 'vim')
        editHelpText = b'#\n' \
                       b'# Enter the body your message above then save & quit\n' \
                       b'# (lines like this one that start with a # are removed)'

        with tempfile.NamedTemporaryFile(suffix=".tmp", delete=True) as tf:
            tf.write(b'\n' + editHelpText)
            tf.flush()

            call([EDITOR, tf.name])

            tf.seek(0)  # go to start of file
            message = tf.readlines()  # and get a full array of lines

            message = map(methodcaller('decode', 'utf-8'), message)  # convert bites 2 strings
            message = filter(isMessageBody, message)  # extract body

    print(colored.green(''.join(message)))
    puts(colored.red("TODO"))  # TODO


@begin.subcommand
def list(all: 'Gets all broadcasts no matter what users made them' = False):
    """Gets a list of all broadcasts made by the current user"""
    print(Actions().get())


@begin.subcommand
def show(id: 'broadcast id'):
    """Show all detail of a broadcast"""

    b = Actions().get(id)

    print_field.content(b)
    print_field.feed(b)
    print_field.created_at(b)


# main cmd method
@begin.start(auto_convert=True)
def broadcast():
    """
    Sends and receives broadcasts (multi social network posts) from a server.

    Use [subcommand] -h to get information of a command
    """
    pass


# def use_pipe():
#     '''this function is run from the shell'''
#     # use care here as it steels the stdin"
#     _in_data = piped_in()
#     if _in_data:
#         puts(colored.red('Data was piped in this will be used as the message body'))
#     else:
#         print(colored.green('started'))


def setup():
    url = urlparse(
        prompt.query('Please enter the API URL:', default='localhost:3000')
    )
