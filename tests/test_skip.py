from .derive_unittest import TestCase

from pystream import Stream
from .throw import throw


class TestSkip(TestCase):
    def test_skip_is_a_stream(self):
        self.assertIsStream(Stream([1, 2, 3]).skip(2))

    def test_skip_empty(self):
        result = Stream([]).skip(10).collect(list)
        self.assertListEqual([], result)

    def test_skip_zero(self):
        result = Stream([1, 2, 3]).skip(0).collect(list)
        self.assertListEqual([1, 2, 3], result)

    def test_skip_negative(self):
        result = Stream([1, 2, 3]).skip(-1).collect(list)
        self.assertListEqual([1, 2, 3], result)

    def test_skip_singleton(self):
        result = Stream([1]).skip(1).collect(list)
        self.assertListEqual([], result)

    def test_skip(self):
        result = Stream(range(100)).skip(10).collect(list)

        self.assertListEqual(list(range(10, 100)), result)

    def test_skip_is_lazy(self):
        Stream(range(100)).map(throw).skip(10)

    def test_skip_excess(self):
        result = Stream(range(10)).skip(100).collect(list)

        self.assertListEqual([], result)
