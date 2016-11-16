import os
import sys
import tempfile
from operator import methodcaller
from subprocess import call

import begin
from clint import resources, Args
from clint.textui import prompt, puts, colored

from .actions import Actions, FEEDS
from .broadcast_printer import broadcast_printer
from .utils import isMessageBody, build_help_text, UrlValidator, exit_and_fail, url_valid

_in_data = ''
URL_FILE_NAME = 'url'

@begin.subcommand
def send(message: 'set the message body' = None, *feeds: 'Bare list of feeds {0}'.format(FEEDS)):
    """Sends a new broadcast to the server"""
    parent = begin.context.last_return

    for f in FEEDS:
        if any(f in s for s in feeds): #if feed name matched user input provided
            puts(f + ' was provided')
        else:
            puts(f + ' was not')

    sys.exit(0)

    # prompt the user for input if we are allowed/reqired
    if parent['interactive']:
        if message is None:
            message = interactive_editor()
        if feeds is '':
            feeds = interactive_feed_select()

    # missing param handle
    if not message:
        exit_and_fail('No message was specified!')
    elif feeds is '':
        exit_and_fail('No feed was specified!')
    else:
        # actualy run the cmd
        print(colored.green(''.join(message)))
        puts(colored.red("TODO"))  # TODO


def interactive_feed_select():
    return 'email'


def interactive_editor():
    EDITOR = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=True) as tf:
        tf.write(b'#\n' + build_help_text(FEEDS))
        tf.flush()

        call([EDITOR, tf.name])

        tf.seek(0)  # go to start of file
        message = tf.readlines()  # and get a full array of lines

        message = map(methodcaller('decode', 'utf-8'), message)  # convert bites 2 strings
        message = filter(isMessageBody, message)  # remove blank lines and comments
    return message


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
def configure(delete: 'Deletes any exsisting config'=False, allow_write: 'allows write while in interactive mode'=False):
    """Set or delete a url to be remembered by the program"""
    parent = begin.context.last_return
    url = parent['url']
    if delete:
        resources.user.delete(URL_FILE_NAME)
        puts(colored.green("Existing config deleted..."))
        return None
    if parent['interactive'] or allow_write is False:
        exit_and_fail("Writing to file while in non-interactive mode explicitly requires the '--allow-write' flag")

    puts('This will write a config file so that the url is remembered')

    if parent['interactive']:
        keep_prompting = confirm_write(url)
        while keep_prompting:
            url = url_prompt()
            puts()
            keep_prompting = confirm_write(url)

        if keep_prompting is None:
            sys.exit(0)

    puts(colored.yellow("Writing to '{}'".format(resources.user.path)))
    resources.user.write(URL_FILE_NAME, url)
    puts(colored.green("Success!"))


def confirm_write(url):
    prompt_options = [{'selector': 'y', 'prompt': 'Yes, write this url to file', 'return': False},
                      {'selector': 'n', 'prompt': 'No, and exit program', 'return': None},
                      {'selector': 'r', 'prompt': 'Re enter URL', 'return': True}]

    return prompt.options("'{}' will be written to config.".format(url), prompt_options)


# main cmd method
@begin.start(auto_convert=True, short_args=True)
def broadcast(raw: 'Reurn only raw Json' = False,
              interactive: 'force interactive on/off' = True,
              url: 'specify url' = None
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

    action = Actions(return_raw=raw, url=url)  # create our instance
    return dict(action=action, raw=raw, interactive=interactive, url=url)


def get_url(interactive):

    config = resources.user.read(URL_FILE_NAME)  # try to find config file
    if config is not None:
        if not url_valid(config):
            exit_and_fail("Url in config is not valid! use 'broadcast configure --delete' to fix this")
        return config
    elif interactive:
        return url_prompt()

    exit_and_fail('Url is not specified!')


def url_prompt():
    return prompt.query('Please enter an API URL:', default='http://localhost:3000', validators=[UrlValidator()])

# def use_pipe():
#     '''this function is run from the shell'''
#     # use care here as it steels the stdin"
#     _in_data = piped_in()
#     if _in_data:
#         puts(colored.red('Data was piped in this will be used as the message body'))
#     else:
#         print(colored.green('started'))
