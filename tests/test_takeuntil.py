from .derive_unittest import TestCase

from amnis import Stream
from .throw import throw


class TestTakeUntil(TestCase):
    def test_takeuntil_is_a_stream(self):
        self.assertIsStream(
            Stream([1, 2, 2, 4, 5, 3, 2, 3, 5])
            .takeuntil(lambda x: x != 3)
        )

    def test_takeuntil(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .takeuntil(lambda x: x != 3) \
            .collect(list)

        self.assertListEqual([1, 2, 2, 4, 5], result)

    def test_takeuntil_take_all(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .takeuntil(lambda x: x != 50) \
            .collect(list)

        self.assertListEqual([1, 2, 2, 4, 5, 3, 2, 3, 5], result)

    def test_takeuntil_take_nothing(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .takeuntil(lambda x: x != 1) \
            .collect(list)

        self.assertListEqual([], result)

    def test_takeuntil_is_lazy(self):
        Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]).map(throw) \
            .takeuntil(lambda x: x != 3)

    def test_takeuntil_with_generator(self):
        result = Stream(range(10)) \
            .takeuntil(lambda x: x <= 3) \
            .collect(list)

        self.assertListEqual([0, 1, 2, 3], result)
