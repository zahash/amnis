import unittest

from pystream import Stream


class TestAllMatch(unittest.TestCase):
    def test_allmatch_empty(self):
        result = Stream([]) \
            .allmatch(lambda x: "a" in x)

        self.assertTrue(result)

    def test_allmatch_true(self):
        result = Stream(["cat", "fat", "rat"]) \
            .allmatch(lambda x: "at" in x)

        self.assertTrue(result)

    def test_allmatch_false(self):
        result = Stream(["cat", "dog", "rat"]) \
            .allmatch(lambda x: "at" in x)

        self.assertFalse(result)
