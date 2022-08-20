import unittest

from pystream import Stream
from .throw import throw


class TestFlatten(unittest.TestCase):
    def test_flatten(self):
        result = Stream([
            [1, 2, 3],
            [],
            [4, 5]
        ]) \
            .flatten() \
            .collect(list)

        self.assertListEqual([1, 2, 3, 4, 5], result)

    def test_flatten_is_lazy(self):
        Stream([[1, 2, 3], [], [4, 5]]).map(throw).flatten()
