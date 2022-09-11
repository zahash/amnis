import unittest
from .derive_unittest import TestCase

from pystream import Stream
from .throw import throw


class TestSorted(TestCase):
    def test_sorted_is_a_stream(self):
        self.assertIsStream(Stream([3, 1, 2]).sorted())

    def test_sorted(self):
        result = Stream([3, 1, 2]) \
            .sorted() \
            .collect(list)

        self.assertListEqual([1, 2, 3], result)

    @unittest.skip("sorted is not yet lazy")
    def test_sorted_is_lazy(self):
        Stream([3, 1, 2]).map(throw).sorted()
