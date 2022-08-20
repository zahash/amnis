import unittest
from typing import Iterable

from pystream import Stream


class TestStream(unittest.TestCase):
    def test_stream_is_iterable(self):
        iterable = Stream([1, 2, 3, 4, 5])

        result = []
        for n in iterable:
            result.append(n)

        self.assertListEqual([1, 2, 3, 4, 5], result)

    def test_apply_empty(self):
        result = Stream([]) \
            .apply(lambda it: it) \
            .collect(list)

        self.assertListEqual([], result)

    def test_apply(self):
        def doubleit(iterable: Iterable) -> Iterable:
            return (item * 2 for item in iterable)

        result = Stream([1, 2, 3]) \
            .apply(doubleit) \
            .collect(list)

        self.assertListEqual([2, 4, 6], result)
