import unittest

from pystream import Stream
from .throw import throw


class TestDropUntil(unittest.TestCase):
    def test_dropuntil(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .dropuntil(lambda x: x != 3) \
            .collect(list)

        self.assertListEqual([3, 2, 3, 5], result)

    def test_dropuntil_is_lazy(self):
        Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]).map(throw) \
            .dropuntil(lambda x: x != 3)

    def test_dropuntil_with_generator(self):
        result = Stream(range(10)) \
            .dropuntil(lambda x: x <= 3) \
            .collect(list)

        self.assertListEqual([4, 5, 6, 7, 8, 9], result)
