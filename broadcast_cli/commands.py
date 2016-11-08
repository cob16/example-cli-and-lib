import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from clint import piped_in
from clint.textui import colored, puts

_in_data = None


def __init__(self):
    _in_data = piped_in()
    if _in_data:
        puts(colored.red('Data was piped in this will be used as the message body'))


def test():
    print(colored.green('started'))
    puts(_in_data)
