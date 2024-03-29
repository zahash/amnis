from .derive_unittest import TestCase

from amnis import Stream
from .throw import throw


class TestSkipWhile(TestCase):
    def test_skipwhile_is_a_stream(self):
        self.assertIsStream(Stream([1, 2, 3]).skipwhile(lambda x: x != 2))

    def test_skipwhile(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .skipwhile(lambda x: x != 3) \
            .collect(list)

        self.assertListEqual([3, 2, 3, 5], result)

    def test_skipwhile_skip_all(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .skipwhile(lambda x: x != 50) \
            .collect(list)

        self.assertListEqual([], result)

    def test_skipwhile_take_all(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .skipwhile(lambda x: x != 1) \
            .collect(list)

        self.assertListEqual([1, 2, 2, 4, 5, 3, 2, 3, 5], result)

    def test_skipwhile_is_lazy(self):
        Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]).map(throw) \
            .skipwhile(lambda x: x != 3)

    def test_skipwhile_with_generator(self):
        result = Stream(range(10)) \
            .skipwhile(lambda x: x <= 3) \
            .collect(list)

        self.assertListEqual([4, 5, 6, 7, 8, 9], result)
