import unittest

from pystream import Stream


class TestNth(unittest.TestCase):
    def test_nth_empty(self):
        result = Stream([]).nth(10)

        self.assertIsNone(result)

    def test_nth_negative(self):
        result = Stream([1, 2, 3]).nth(-1)

        self.assertIsNone(result)

    def test_nth_excess(self):
        result = Stream([1, 2, 3]).nth(3)

        self.assertIsNone(result)

    def test_nth(self):
        self.assertEqual(1, Stream([1, 2, 3]).nth(0))
        self.assertEqual(2, Stream([1, 2, 3]).nth(1))
        self.assertEqual(3, Stream([1, 2, 3]).nth(2))
