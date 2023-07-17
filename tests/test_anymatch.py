import unittest

from amnis import Stream


class TestAnyMatch(unittest.TestCase):
    def test_anymatch_empty(self):
        result = Stream([]) \
            .anymatch(lambda x: "a" in x)

        self.assertFalse(result)

    def test_anymatch_true(self):
        result = Stream(["cat", "dog", "rat"]) \
            .anymatch(lambda x: "at" in x)

        self.assertTrue(result)

    def test_anymatch_false(self):
        result = Stream(["cat", "dog", "rat"]) \
            .anymatch(lambda x: "z" in x)

        self.assertFalse(result)
