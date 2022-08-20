import unittest

from pystream import Stream


class TestFirst(unittest.TestCase):
    def test_first_empty(self):
        result = Stream([]) \
            .first()

        self.assertIsNone(result)

    def test_first(self):
        result = Stream([1, 2, 3]) \
            .first()

        self.assertEqual(1, result)

    def test_first_with_map_filter(self):
        result = Stream([1, 2, 3]) \
            .filter(lambda x: x > 1) \
            .map(lambda x: x * 2) \
            .first()

        self.assertEqual(4, result)
