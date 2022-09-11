import unittest

from pystream import Stream


class TestMax(unittest.TestCase):
    def test_max_empty(self):
        self.assertIsNone(Stream([]).max())

    def test_max_empty_with_key(self):
        self.assertIsNone(Stream([]).max(lambda x: x + 1))

    def test_max_singleton(self):
        self.assertEqual(1, Stream([1]).max())

    def test_max_singleton_with_key(self):
        self.assertEqual(1, Stream([1]).max(lambda x: x * 2))

    def test_max(self):
        self.assertEqual("cc", Stream(["a", "bbbbb", "cc"]).max())

    def test_max_with_key(self):
        self.assertEqual(
            "bbbbb",
            Stream(["a", "bbbbb", "cc"]).max(lambda x: len(x))
        )
