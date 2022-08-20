import unittest

from pystream import Stream
from .throw import throw


class TestSorted(unittest.TestCase):
    def test_sorted(self):
        result = Stream([3, 1, 2]) \
            .sorted() \
            .collect(list)

        self.assertListEqual([1, 2, 3], result)

    @unittest.skip("sorted is not yet lazy")
    def test_sorted_is_lazy(self):
        Stream([3, 1, 2]).map(throw).sorted()

    def test_sorted_with_map_filter(self):
        result = Stream([5, 4, 3, 2, 1]) \
            .map(lambda x: x - 1) \
            .sorted() \
            .filter(lambda x: x % 2 == 0) \
            .collect(list)

        self.assertEqual([0, 2, 4], result)
