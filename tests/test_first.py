import unittest

from amnis import Stream


class TestFirst(unittest.TestCase):
    def test_first_empty(self):
        result = Stream([]).first()

        self.assertIsNone(result)

    def test_first_singleton(self):
        result = Stream([1]).first()

        self.assertEqual(1, result)

    def test_first(self):
        result = Stream([1, 2, 3]).first()

        self.assertEqual(1, result)
