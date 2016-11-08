import os
import sys

# sys.path.insert(0, os.path.abspath('..'))
from urllib.parse import urlparse

from clint import piped_in
from clint.textui import colored, puts

from actions import Action

_in_data = ''

'''
this function is run from the shell
'''


def cmd():
    _in_data = piped_in()
    if _in_data:
        puts(colored.red('Data was piped in this will be used as the message body'))


def test():
    get_input()
    print(colored.green('started'))
    puts(_in_data)


import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import prompt, puts, colored, validators


def setup():
    # Use a default value and a validator
    _URL = urlparse(
        prompt.query('Please enter the API URL:', default='localhost:3000')
    )

    a = Action(_URL, 'foobar')
    puts(colored.blue(_URL.getURL()))
