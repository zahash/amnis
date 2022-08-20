import unittest

from pystream import Stream


class TestReduce(unittest.TestCase):
    def test_reduce_empty_without_initial(self):
        result = Stream([]) \
            .reduce(lambda x, y: x + y)

        self.assertIsNone(result)

    def test_reduce_empty_with_initial(self):
        result = Stream([]) \
            .reduce(lambda x, y: x + y, initial=10)

        self.assertEqual(10, result)

    def test_reduce_empty_with_zero_initial(self):
        result = Stream([]) \
            .reduce(lambda x, y: x + y, initial=0)

        self.assertEqual(0, result)

    def test_reduce(self):
        result = Stream([1, 2, 3]) \
            .reduce(lambda x, y: x + y)

        self.assertEqual(6, result)

    def test_reduce_with_initial_value(self):
        result = Stream([1, 2, 3]) \
            .reduce(lambda x, y: x + y, initial=10)

        self.assertEqual(16, result)
