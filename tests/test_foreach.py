import unittest

from pystream import Stream


class TestForEach(unittest.TestCase):
    def test_foreach_empty(self):
        result = []
        Stream([]) \
            .foreach(lambda x: result.append(x + 1))

        self.assertListEqual([], result)

    def test_foreach(self):
        result = []

        Stream([1, 2, 3]) \
            .foreach(lambda x: result.append(x + 1))

        self.assertListEqual([2, 3, 4], result)
