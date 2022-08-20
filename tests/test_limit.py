import unittest
import operator

from pystream import Stream
from .throw import throw


class TestLimit(unittest.TestCase):
    def test_limit(self):
        result = Stream(range(100)) \
            .limit(10) \
            .collect(list)

        self.assertListEqual(list(range(10)), result)

    def test_limit_is_lazy(self):
        Stream(range(100)).map(throw).limit(10)

    def test_limit_excess(self):
        result = Stream(range(10)) \
            .limit(100) \
            .collect(list)

        self.assertListEqual(list(range(10)), result)

    def test_limit_with_reduce(self):
        result = Stream(range(1, 100)) \
            .limit(5) \
            .reduce(operator.add)

        self.assertEqual(15, result)
