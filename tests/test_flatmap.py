from .derive_unittest import TestCase

from amnis import Stream
from .throw import throw


class TestFlatMap(TestCase):
    def test_flatmap_is_a_stream(self):
        self.assertIsStream(
            Stream(["it's Sunny in", "", "California"])
            .flatmap(lambda s: s.split(" "))
        )

    def test_flatmap(self):
        result = Stream(["it's Sunny in", "", "California"]) \
            .flatmap(lambda s: s.split(" ")) \
            .collect(list)

        self.assertListEqual(["it's", "Sunny", "in", "", "California"], result)

    def test_flatmap_is_lazy(self):
        Stream(["it's Sunny in", "", "California"]) \
            .map(throw) \
            .flatmap(lambda s: s.split(" "))
