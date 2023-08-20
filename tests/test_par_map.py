from time import sleep
from .thread_tools import timeit, ncpu, expected_speedup_factor
from .derive_unittest import TestCase

from amnis import Stream
from .throw import throw


def expensive(x):
    sleep(0.1)
    return x


def times3(x):
    return x * 3


class TestParallelMap(TestCase):
    def test_par_map_is_stream(self):
        self.assertIsStream(Stream([1, 2, 3]).par_map(lambda x: x * 3))

    def test_par_map(self):
        result = (Stream([1, 2, 3])
                  .par_map(times3)
                  .sorted()
                  .collect(list))

        self.assertListEqual([3, 6, 9], result)

    def test_par_map_is_lazy(self):
        Stream([1, 2, 3]).map(throw).par_map(times3)

    def test_par_map_time(self):
        seq_time = timeit(lambda: (Stream([1] * ncpu * 2)
                                   .map(expensive)
                                   .collect(list)))

        par_time = timeit(lambda: (Stream([1] * ncpu * 2)
                                   .par_map(expensive)
                                   .collect(list)))

        self.assertLess(par_time, seq_time / expected_speedup_factor)
