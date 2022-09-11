from .derive_unittest import TestCase

from pystream import Stream
from .throw import throw


class TestDistinct(TestCase):
    def test_distinct_is_a_stream(self):
        self.assertIsStream(Stream([1, 1, 2, 3, 3, 2]).distinct())

    def test_distinct(self):
        result = Stream([1, 1, 2, 3, 3, 2]) \
            .distinct() \
            .collect(list)

        self.assertListEqual([1, 2, 3], result)

    def test_distinct_is_lazy(self):
        Stream([1, 1, 2, 3, 3, 2]).map(throw).distinct()
