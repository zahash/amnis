import unittest

from pystream import Stream
from .throw import throw


class TestFlatMap(unittest.TestCase):
    def test_flatmap(self):
        result = Stream(["it's Sunny in", "", "California"]) \
            .flatmap(lambda s: s.split(" ")) \
            .collect(list)

        self.assertListEqual(["it's", "Sunny", "in", "", "California"], result)

    def test_flatmap_is_lazy(self):
        Stream(["it's Sunny in", "", "California"]) \
            .map(throw) \
            .flatmap(lambda s: s.split(" "))
