import unittest

from pystream import Stream


class TestLast(unittest.TestCase):
    def test_last_empty(self):
        result = Stream([]).last()

        self.assertIsNone(result)

    def test_last_singleton(self):
        result = Stream([1]).last()

        self.assertEqual(1, result)

    def test_last(self):
        result = Stream([1, 2, 3]).last()

        self.assertEqual(3, result)
