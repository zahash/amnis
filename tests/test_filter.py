import unittest

from pystream import Stream
from .throw import throw


class TestFilter(unittest.TestCase):
    def test_filter(self):
        result = Stream([1, 2, 3]) \
            .filter(lambda x: x > 1) \
            .collect(list)

        self.assertListEqual([2, 3], result)

    def test_filter_is_lazy(self):
        Stream([1, 2, 3]).map(throw).filter(lambda x: x > 2)