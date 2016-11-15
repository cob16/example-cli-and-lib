import os
import tempfile
from functools import reduce
from operator import methodcaller
from subprocess import call
from urllib.parse import urlparse

import begin
from .broadcast_printer import broadcast_printer
from clint import piped_in
from clint.textui import prompt, puts, colored

from .actions import Actions, FEEDS
from .utils import isMessageBody

_in_data = ''
_a = None


def generate_feeds():
    return ': \n\n'.join(FEEDS) + ': \n'


@begin.subcommand
def send(message: 'set the message body' = None):
    """Sends a new broadcast"""

    if message is None:
        EDITOR = os.environ.get('EDITOR', 'vim')
        editHelpText = "# place an \'x\' after the feed name to indicate you wish to post there \n" \
                       "{} \n" \
                       "# Enter the body your message below then save & quit\n" \
            .format(generate_feeds()).encode()

        with tempfile.NamedTemporaryFile(suffix=".tmp", delete=True) as tf:
            tf.write(b'#\n' + editHelpText)
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
def show(id: 'broadcast id' = None):
    """Show all detail of a broadcast"""
    parent = begin.context.last_return
    broadcasts = parent['action'].get(id)

    if parent['raw']:
        print(broadcasts)
    elif id:
        broadcast_printer(broadcasts)
    else:
        for b in broadcasts:
            broadcast_printer(b)
            # list(map(lambda d: Broadcast().from_json(d), data)


# main cmd method
@begin.start(auto_convert=True)
def broadcast(raw: 'Reurn only raw Json' = False):
    """
    Sends and receives broadcasts (multi social network posts) from a server.

    Use [subcommand] -h to get information of a command
    """
    action = Actions(return_raw=raw)  # create our instance
    return dict(action=action, raw=raw)


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
