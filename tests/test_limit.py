from .derive_unittest import TestCase

from pystream import Stream
from .throw import throw


class TestLimit(TestCase):
    def test_limit_is_a_stream(self):
        self.assertIsStream(Stream([1, 2, 3]).limit(2))

    def test_limit_empty(self):
        result = Stream([]).limit(10).collect(list)
        self.assertListEqual([], result)

    def test_limit_zero(self):
        result = Stream([1, 2, 3]).limit(0).collect(list)
        self.assertListEqual([], result)

    def test_limit_negative(self):
        result = Stream([1, 2, 3]).limit(-1).collect(list)
        self.assertListEqual([], result)

    def test_limit(self):
        result = Stream(range(100)) \
            .limit(10) \
            .collect(list)

        self.assertListEqual(list(range(10)), result)

    def test_limit_is_lazy(self):
        Stream(range(100)).map(throw).limit(10)

    def test_limit_excess(self):
        result = Stream(range(10)) \
            .limit(100) \
            .collect(list)

        self.assertListEqual(list(range(10)), result)
