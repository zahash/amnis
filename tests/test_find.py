import unittest

from pystream import Stream


class TestFind(unittest.TestCase):
    def test_find_empty(self):
        self.assertIsNone(Stream([]).find(lambda x: x == 1))

    def test_find_singleton_found(self):
        self.assertEqual(1, Stream([1]).find(lambda x: x == 1))

    def test_find_singleton_not_found(self):
        self.assertIsNone(Stream([0]).find(lambda x: x == 1))

    def test_find_found(self):
        self.assertEqual(2, Stream([1, 2, 3]).find(lambda x: x == 2))

    def test_find_not_found(self):
        self.assertIsNone(Stream([1, 2, 3]).find(lambda x: x == 5))
