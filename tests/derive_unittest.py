import unittest

from pystream import Stream


class TestCase(unittest.TestCase):
    def assertIsStream(self, obj):
        self.assertIsInstance(obj, Stream)
