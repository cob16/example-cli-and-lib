# helper functions
from urllib.parse import urlparse

import sys
from clint.textui.validators import ValidationError


def isMessageBody(line: str) -> bool:
    """
    Returns True if line has more than just whitepsace and unempty or is a comment (contains #)
    """
    return not (line.isspace() or line.lstrip().startswith('#'))


def build_help_text(feeds):
    """
    Takes field names and any proved params and makes the help text for the editor
    """
    return " \n" \
           "# Enter the body your message then save & quit\n" \
        .format(feeds).encode()


class UrlValidator(object):
    """
    Trows clint.textui.validators.ValidationError if url fails to validate
    """
    message = 'Enter a valid URL.'

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __call__(self, value):
        """
        Validates that the input is a valid directory.
        """
        if not url_valid(value):
            raise ValidationError(self.message)
        return value


def url_valid(url):
    return urlparse(url).scheme


def exit_and_fail(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(2)
