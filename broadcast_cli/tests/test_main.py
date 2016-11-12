import sys
from io import StringIO
from unittest import TestCase

import broadcast_cli


class TestJoke(TestCase):
    def test_is_string(self):
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            # broadcast_cli.test()

            output = out.getvalue().strip()
            # assert output == 'started'
        finally:
            sys.stdout = saved_stdout
