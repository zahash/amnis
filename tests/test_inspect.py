from .derive_unittest import TestCase

from amnis import Stream
from .throw import throw


class TestInspect(TestCase):
    def test_inspect_is_stream(self):
        self.assertIsStream(Stream([1, 2, 3]).inspect(lambda x: print(x)))

    def test_inspect(self):
        before = []
        after = []

        result = (Stream([1, 2, 3])
                  .inspect(lambda x: before.append(x))
                  .map(lambda x: x * 3)
                  .inspect(lambda x: after.append(x))
                  .filter(lambda x: x > 6)
                  .collect(list))

        self.assertListEqual([9], result)
        self.assertListEqual([1, 2, 3], before)
        self.assertListEqual([3, 6, 9], after)

    def test_inspect_is_lazy(self):
        Stream([1, 2, 3]).map(throw).inspect(lambda x: print(x))
