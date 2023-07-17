import unittest

from amnis import Stream


class TestNth(unittest.TestCase):
    def test_nth_empty(self):
        self.assertIsNone(Stream([]).nth(0))
        self.assertIsNone(Stream([]).nth(-1))
        self.assertIsNone(Stream([]).nth(1))
        self.assertIsNone(Stream([]).nth(10))

    def test_nth_singleton(self):
        self.assertEqual(1, Stream([1]).nth(0))

    def test_nth_negative(self):
        self.assertIsNone(Stream([1, 2, 3]).nth(-1))

    def test_nth_excess(self):
        self.assertIsNone(Stream([1, 2, 3]).nth(3))
        self.assertIsNone(Stream([1, 2, 3]).nth(10))

    def test_nth(self):
        self.assertEqual(1, Stream([1, 2, 3]).nth(0))
        self.assertEqual(2, Stream([1, 2, 3]).nth(1))
        self.assertEqual(3, Stream([1, 2, 3]).nth(2))
