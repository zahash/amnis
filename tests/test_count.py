import unittest

from amnis import Stream


class TestCount(unittest.TestCase):
    def test_count_empty(self):
        result = Stream([]) \
            .count()

        self.assertEqual(0, result)

    def test_count(self):
        result = Stream([1, 2, 3]) \
            .count()

        self.assertEqual(3, result)
