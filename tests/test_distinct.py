import unittest

from pystream import Stream
from .throw import throw


class TestDistinct(unittest.TestCase):
    def test_distinct(self):
        result = Stream([1, 1, 2, 3, 3, 2]) \
            .distinct() \
            .collect()

        self.assertEqual(1, next(result))
        self.assertEqual(2, next(result))
        self.assertEqual(3, next(result))

    def test_distinct_is_lazy(self):
        Stream([1, 1, 2, 3, 3, 2]).map(throw).distinct()

    def test_distinct_with_map_filter(self):
        result = Stream([1, 1, 2, 3, 3, 2]) \
            .map(lambda x: x * 2) \
            .distinct() \
            .filter(lambda x: x > 0) \
            .collect(list)

        self.assertListEqual([2, 4, 6], result)
