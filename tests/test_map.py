import unittest

from pystream import Stream
from .throw import throw


class TestMap(unittest.TestCase):
    def test_map(self):
        result = Stream([1, 2, 3]) \
            .map(lambda x: x * 3) \
            .collect(list)

        self.assertListEqual([3, 6, 9], result)

    def test_map_is_lazy(self):
        Stream([1, 2, 3]).map(throw).map(lambda x: x + 2)
