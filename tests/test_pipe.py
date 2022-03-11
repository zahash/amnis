import unittest

from pystream import pipe


class TestPipe(unittest.TestCase):
    def test_pipe_one_fn_one_posarg_one_return(self):
        def doubleit(x):
            return x * 2

        piped = pipe(doubleit)

        self.assertEqual(4, piped(2))

    def test_pipe_multi_fns_one_posarg_one_return(self):
        def doubleit(x):
            return x * 2

        def add5(x):
            return x + 5

        piped = pipe(doubleit, add5)

        self.assertEqual(9, piped(2))
