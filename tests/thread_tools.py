from time import time
from os import cpu_count

# just in case of hyperthreading
ncpu = cpu_count() // 2

# -1 for overhead
expected_speedup_factor = ncpu - 1


def timeit(fn):
    start = time()
    fn()
    end = time()
    return end - start
