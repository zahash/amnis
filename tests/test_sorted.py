import unittest
from .derive_unittest import TestCase

from amnis import Stream
from .throw import throw


class TestSorted(TestCase):
    def test_sorted_is_a_stream(self):
        self.assertIsStream(Stream([3, 1, 2]).sorted())

    def test_sorted(self):
        result = Stream([3, 1, 2]) \
            .sorted() \
            .collect(list)

        self.assertListEqual([1, 2, 3], result)

    def test_sorted_with_key(self):
        result = (Stream([(1, 4), (2, 3), (3, 2), (4, 1)])
                  .sorted(key=lambda p: p[1])
                  .collect(list))

        self.assertListEqual([(4, 1), (3, 2), (2, 3), (1, 4)], result)

    @unittest.skip("sorted is not yet lazy")
    def test_sorted_is_lazy(self):
        Stream([3, 1, 2]).map(throw).sorted()
