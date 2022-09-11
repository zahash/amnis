import unittest

from pystream import Stream


class TestMin(unittest.TestCase):
    def test_min_empty(self):
        self.assertIsNone(Stream([]).min())

    def test_min_empty_with_key(self):
        self.assertIsNone(Stream([]).min(lambda x: x + 1))

    def test_min_singleton(self):
        self.assertEqual(1, Stream([1]).min())

    def test_min_singleton_with_key(self):
        self.assertEqual(1, Stream([1]).min(lambda x: x * 2))

    def test_min(self):
        self.assertEqual("aaaaa", Stream(["cc", "aaaaa", "b"]).min())

    def test_min_with_key(self):
        self.assertEqual(
            "b",
            Stream(["cc", "aaaaa", "b"]).min(lambda x: len(x))
        )
