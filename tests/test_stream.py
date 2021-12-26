import operator
import unittest
from collections import namedtuple
from typing import Iterable

from pystream import Stream, Grouper

Person = namedtuple("Person", ["name", "age"])


class TestStream(unittest.TestCase):
    def test_collect_with_default(self):
        result = Stream([1, 2, 3]) \
            .collect()

        self.assertEqual(1, next(result))
        self.assertEqual(2, next(result))
        self.assertEqual(3, next(result))

    def test_collect_with_list(self):
        result = Stream([1, 2, 3]) \
            .collect(list)

        self.assertListEqual([1, 2, 3], result)

    def test_collect_with_set(self):
        result = Stream([1, 2, 3]) \
            .collect(set)

        self.assertSetEqual({1, 2, 3}, result)

    def test_apply(self):
        def doubleit(iterable: Iterable) -> Iterable:
            return (item * 2 for item in iterable)

        result = Stream([1, 2, 3]) \
            .apply(doubleit) \
            .collect(list)

        self.assertListEqual([2, 4, 6], result)

    def test_foreach(self):
        result = []

        Stream([1, 2, 3]) \
            .foreach(lambda x: result.append(x + 1))

        self.assertListEqual([2, 3, 4], result)

    def test_map(self):
        result = Stream([1, 2, 3]) \
            .map(lambda x: x * 3) \
            .collect(list)

        self.assertListEqual([3, 6, 9], result)

    def test_filter(self):
        result = Stream([1, 2, 3]) \
            .filter(lambda x: x > 1) \
            .collect(list)

        self.assertListEqual([2, 3], result)

    def test_reduce(self):
        result = Stream([1, 2, 3]) \
            .reduce(lambda x, y: x + y)

        self.assertEqual(6, result)

    def test_reduce_with_initial_value(self):
        result = Stream([1, 2, 3]) \
            .reduce(lambda x, y: x + y, initial=10)

        self.assertEqual(16, result)

    def test_map_and_filter(self):
        result = Stream([1, 2, 3]) \
            .filter(lambda x: x > 1) \
            .map(lambda x: x * 2) \
            .collect(list)

        self.assertListEqual([4, 6], result)

    def test_map_and_filter_and_reduce(self):
        result = Stream([1, 2, 3]) \
            .filter(lambda x: x > 1) \
            .map(lambda x: x * 2) \
            .reduce(operator.add, 10)

        self.assertEqual(20, result)

    def test_distinct(self):
        result = Stream([1, 1, 2, 3, 3, 2]) \
            .distinct() \
            .collect()

        self.assertEqual(1, next(result))
        self.assertEqual(2, next(result))
        self.assertEqual(3, next(result))

    def test_distinct_with_map_filter(self):
        result = Stream([1, 1, 2, 3, 3, 2]) \
            .map(lambda x: x * 2) \
            .distinct() \
            .filter(lambda x: x > 0) \
            .collect(list)

        self.assertListEqual([2, 4, 6], result)

    def test_group_with_list(self):
        result = Stream([Person("jack", 20), Person("jack", 30), Person("jill", 25)]) \
            .group(key_fn=lambda p: p.name, val_fn=lambda p: p.age,
                   grouper=Grouper(list, grouper_fn=lambda l, item: l.append(item)))

        self.assertDictEqual({"jack": [20, 30], "jill": [25]}, result)

    def test_group_with_str(self):
        result = Stream([Person("jack", 20), Person("jack", 30), Person("jill", 25), Person("jack", 40)]) \
            .group(key_fn=lambda p: p.name, val_fn=lambda p: p.age,
                   grouper=Grouper(str, grouper_fn=lambda s, item: f"{s}, {item}" if s else f"{item}"))

        self.assertDictEqual({"jack": "20, 30, 40", "jill": "25"}, result)

    def test_first(self):
        result = Stream([1, 2, 3]) \
            .first()

        self.assertEqual(1, result)

    def test_first_with_map_filter(self):
        result = Stream([1, 2, 3]) \
            .filter(lambda x: x > 1) \
            .map(lambda x: x * 2) \
            .first()

        self.assertEqual(4, result)

    def test_sorted(self):
        result = Stream([3, 1, 2]) \
            .sorted() \
            .collect(list)

        self.assertListEqual([1, 2, 3], result)

    def test_sorted_with_map_filter(self):
        result = Stream([5, 4, 3, 2, 1]) \
            .map(lambda x: x - 1) \
            .sorted() \
            .filter(lambda x: x % 2 == 0) \
            .collect(list)

        self.assertEqual([0, 2, 4], result)

    def test_limit(self):
        result = Stream(range(100)) \
            .limit(10) \
            .collect(list)

        self.assertListEqual(list(range(10)), result)

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

    def test_allmatch_true(self):
        result = Stream(["cat", "fat", "rat"]) \
            .allmatch(lambda x: "at" in x)

        self.assertTrue(result)

    def test_allmatch_false(self):
        result = Stream(["cat", "dog", "rat"]) \
            .allmatch(lambda x: "at" in x)

        self.assertFalse(result)

    def test_anymatch_true(self):
        result = Stream(["cat", "dog", "rat"]) \
            .anymatch(lambda x: "at" in x)

        self.assertTrue(result)

    def test_anymatch_false(self):
        result = Stream(["cat", "dog", "rat"]) \
            .anymatch(lambda x: "z" in x)

        self.assertFalse(result)

    def test_count_empty(self):
        result = Stream([]) \
            .count()

        self.assertEqual(0, result)

    def test_count(self):
        result = Stream([1, 2, 3]) \
            .count()

        self.assertEqual(3, result)

    def test_takewhile(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .takewhile(lambda x: x != 3) \
            .collect(list)

        self.assertListEqual([1, 2, 2, 4, 5], result)

    def test_dropwhile(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .dropwhile(lambda x: x != 3) \
            .collect(list)

        self.assertListEqual([3, 2, 3, 5], result)
