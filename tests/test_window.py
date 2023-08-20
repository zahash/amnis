from .derive_unittest import TestCase

from amnis import Stream
from .throw import throw


class TestWindow(TestCase):
    def test_window_is_a_stream(self):
        self.assertIsStream(Stream([1, 2, 3]).window(2))

    def test_window_empty(self):
        result = Stream([]).window(10).collect(list)
        self.assertListEqual([], result)

    def test_window_zero(self):
        result = Stream([1, 2, 3]).window(0).collect(list)
        self.assertListEqual([], result)

    def test_window_negative(self):
        result = Stream([1, 2, 3]).window(-1).collect(list)
        self.assertListEqual([], result)

    def test_unit_width_window(self):
        result = Stream([1, 2, 3]).window(1).collect(list)
        self.assertListEqual([(1,), (2,), (3,)], result)

    def test_window_singleton(self):
        result = Stream([1]).window(1).collect(list)
        self.assertListEqual([(1,)], result)

    def test_window_width_same_as_stream_length(self):
        result = Stream([1, 2, 3]).window(3).collect(list)
        self.assertListEqual([(1, 2, 3)], result)

    def test_window(self):
        result = Stream([1, 2, 3, 4, 5]) \
            .window(3) \
            .collect(list)

        self.assertListEqual([
            (1, 2, 3),
            (2, 3, 4),
            (3, 4, 5),
        ], result)

    def test_window_is_lazy(self):
        Stream(range(100)).map(throw).window(10)

    def test_window_excess(self):
        result = Stream(range(10)) \
            .window(100) \
            .collect(list)

        self.assertListEqual([], result)
