import os
import sys
import tempfile
from operator import methodcaller
from subprocess import call

import begin
from broadcast.broadcast import Broadcast
from broadcast.rest_actions import FEEDS as KNOWN_FEEDS
from broadcast.rest_actions import RestActions
from clint import resources
from clint.textui import prompt, puts, colored

from .broadcast_printer import broadcast_printer
from .utils import isMessageBody, build_help_text, UrlValidator, exit_and_fail, url_valid

_in_data = ''
URL_FILENAME = 'url'
AUTHTOKEN_FILENAME = 'token'


@begin.subcommand
def send(message: 'set the message body' = None, *feeds: 'Bare list of feeds {0}'.format(KNOWN_FEEDS)):
    """Sends a new broadcast to the server"""
    parent = begin.context.last_return
    validate_feeds(feeds)

    # prompt the user for input if we are allowed/reqired
    if message is None:
        if parent['interactive']:
            message = interactive_editor()
        else:
            exit_and_fail('You must provide a message')

    broadcast = parent['action'].post(
        Broadcast(list(feeds), message)
    )

    puts(colored.green('Successfully sent broadcast!'))

    if parent['raw']:
        print(broadcast)
    else:
        broadcast_printer(broadcast)


def validate_feeds(feeds):
    feeds = set(feeds)
    if not feeds:
        exit_and_fail("You must specify feed name/s ('broadcast send -h' for more info)")
    elif not set(KNOWN_FEEDS) > feeds:  # are there incorrect feed names supplyed
        exit_and_fail(
            "Unknown feed name/s: {0}.\nRecognised names are: '{1}'".format(
                feeds.difference(KNOWN_FEEDS),
                ', '.join(KNOWN_FEEDS)
            )
        )


def interactive_editor():
    EDITOR = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=True) as tf:
        tf.write(b'\n' + build_help_text(KNOWN_FEEDS))
        tf.flush()

        call([EDITOR, tf.name])

        tf.seek(0)  # go to start of file
        message = tf.readlines()  # and get a full array of lines

        message = map(methodcaller('decode', 'utf-8'), message)  # convert bites 2 strings
        message = list(filter(isMessageBody, message))  # remove blank lines and comments
    return ' '.join(message)


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


@begin.subcommand()
def configure(delete: 'Deletes any exsisting config' = False,
              allow_write: 'allows write while in interactive mode' = False):
    """Set or delete a url to be remembered by the program"""
    parent = begin.context.last_return
    url = parent['url']
    auth_token = parent['action'].auth_token
    if delete:
        resources.user.delete(URL_FILENAME)
        resources.user.delete(AUTHTOKEN_FILENAME)
        puts(colored.green("Existing config deleted..."))
        return None
    if parent['interactive'] is False and allow_write is False:
        exit_and_fail("Writing to file while in non-interactive mode explicitly requires the '--allow-write' flag")

    puts('This will write a config file so that The following is remembered:')

    if parent['interactive']:
        if confirm_write(url, auth_token) is False:
            sys.exit(0)

    puts(colored.yellow("Writing to '{}'".format(resources.user.path)))
    resources.user.write(URL_FILENAME, url)
    resources.user.write(AUTHTOKEN_FILENAME, auth_token)
    puts(colored.green("Success!"))


def confirm_write(url, token):
    PROMPT_OPTIONS = [
        {'selector': 'y', 'prompt': 'Yes, write this url to file', 'return': True},
        {'selector': 'n', 'prompt': 'No, and exit program', 'return': False}
    ]

    return prompt.options("\nURL   : '{}'\nToken : '{}'".format(url, token),
                          PROMPT_OPTIONS)


def set_authtoken(interactive, action):
    config = get_config(AUTHTOKEN_FILENAME)
    if config:
        action.auth_token = config
        return config
    if interactive:
        puts(colored.yellow("Querying: {} for a API token".format(action.url)))
        config = action.Authenticate(
            prompt.query(
                'Please enter you username:'),
            prompt.query(
                'Please enter you password:')
        )
        puts(colored.green('Success!'))
        return config

    exit_and_fail('You must specify a auth token')


@begin.start(auto_convert=True, short_args=True)
def broadcast(raw: 'Reurn only raw Json' = False,
              interactive: 'Force interactive on/off' = True,
              url: 'Specify url' = None,
              auth_token: 'Explicitly specify auth token instead of from config or interactively' = None
              ):
    """
    Sends and receives broadcasts (multi social network posts) from a server.

    Use [subcommand] -h to get information of a command
    """
    sys.path.insert(0, os.path.abspath('..'))
    resources.init('cbrady', 'broadcasts_cli')

    if url is None:
        url = get_url(interactive)
    elif not url_valid(url):
        exit_and_fail("Invalid URL")

    action = RestActions(return_raw=raw, url=url)  # create our instance

    # need the action instance for this one
    if auth_token is None:
        set_authtoken(interactive, action)

    return dict(action=action, raw=raw, interactive=interactive, url=url)


def get_url(interactive):
    config = get_config(URL_FILENAME)
    if config:
        if not url_valid(config):
            exit_and_fail("Url in config is not valid! use 'broadcast configure --delete' to fix this")
        return config
    elif interactive:
        return url_prompt()

    exit_and_fail('Url is not specified!')


def url_prompt():
    return prompt.query('Please enter an API URL:', default='http://localhost:3000', validators=[UrlValidator()])


def get_config(filename):
    """ try to find config file else return None """
    return resources.user.read(filename)  # try to find config file

# def use_pipe():
#     '''this function is run from the shell'''
#     # use care here as it steels the stdin"
#     _in_data = piped_in()
#     if _in_data:
#         puts(colored.red('Data was piped in this will be used as the message body'))
#     else:
#         print(colored.green('started'))
