import unittest

from amnis import Stream


class TestNoMatch(unittest.TestCase):
    def test_nomatch_empty(self):
        result = (Stream([])
                  .nomatch(lambda x: "a" in x))

        self.assertTrue(result)

    def test_nomatch_true(self):
        result = (Stream([3, 5, 7])
                  .nomatch(lambda x: x % 2 == 0))

        self.assertTrue(result)

    def test_nomatch_false(self):
        result = (Stream([3, 4, 7])
                  .nomatch(lambda x: x % 2 == 0))

        self.assertFalse(result)
