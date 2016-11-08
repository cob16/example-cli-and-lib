from urllib.parse import urlparse

from clint import piped_in
from clint.textui import prompt, puts, colored, validators

from .actions import Action

_in_data = ''

'''
this function is run from the shell
'''


def cmd():
    "use care here as it steels the stdin"
    _in_data = piped_in()
    if _in_data:
        puts(colored.red('Data was piped in this will be used as the message body'))
    else:
        print(colored.green('started'))


def test():
    setup()

def setup():
    url = urlparse(
        prompt.query('Please enter the API URL:', default='localhost:3000')
    )

    a = Action(url, 'foobar')
    puts(colored.blue(str(url)))
