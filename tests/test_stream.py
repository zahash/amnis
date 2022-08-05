from gc import collect
import operator
import unittest
from collections import namedtuple
from typing import Iterable

from pystream import Stream, Grouper

Person = namedtuple("Person", ["name", "age"])


class TestStream(unittest.TestCase):
    def test_stream_is_iterable(self):
        iterable = Stream([1, 2, 3, 4, 5])

        result = []
        for n in iterable:
            result.append(n)

        self.assertListEqual([1, 2, 3, 4, 5], result)

    def test_stream_is_iterable_with_map_filter(self):
        iterable = Stream([1, 2, 3, 4, 5]) \
            .map(lambda x: x * 2) \
            .filter(lambda x: x > 2)

        result = []
        for n in iterable:
            result.append(n)

        self.assertListEqual([4, 6, 8, 10], result)

    def test_collect_empty_with_default(self):
        result = Stream([]) \
            .collect()

        with self.assertRaises(StopIteration):
            next(result)

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

    def test_apply_empty(self):
        result = Stream([]) \
            .apply(lambda it: it) \
            .collect(list)

        self.assertListEqual([], result)

    def test_apply(self):
        def doubleit(iterable: Iterable) -> Iterable:
            return (item * 2 for item in iterable)

        result = Stream([1, 2, 3]) \
            .apply(doubleit) \
            .collect(list)

        self.assertListEqual([2, 4, 6], result)

    def test_foreach_empty(self):
        result = []
        Stream([]) \
            .foreach(lambda x: result.append(x + 1))

        self.assertListEqual([], result)

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

    def test_reduce_empty_without_initial(self):
        result = Stream([]) \
            .reduce(lambda x, y: x + y)

        self.assertIsNone(result)

    def test_reduce_empty_with_initial(self):
        result = Stream([]) \
            .reduce(lambda x, y: x + y, initial=10)

        self.assertEqual(10, result)

    def test_reduce_empty_with_zero_initial(self):
        result = Stream([]) \
            .reduce(lambda x, y: x + y, initial=0)

        self.assertEqual(0, result)

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

    def test_flatten(self):
        result = Stream([
            [1, 2, 3],
            [],
            [4, 5]
        ]) \
            .flatten() \
            .collect(list)

        self.assertListEqual([1, 2, 3, 4, 5], result)

    def test_flatmap(self):
        result = Stream(["it's Sunny in", "", "California"]) \
            .flatmap(lambda s: s.split(" ")) \
            .collect(list)

        self.assertListEqual(["it's", "Sunny", "in", "", "California"], result)

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

    def test_group_empty(self):
        result = Stream([]) \
            .group(key_fn=lambda x: x, val_fn=lambda x: x,
                   grouper=Grouper(list, grouper_fn=lambda l, item: l.append(item)))

        self.assertDictEqual({}, result)

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

    def test_first_empty(self):
        result = Stream([]) \
            .first()

        self.assertIsNone(result)

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

    def test_count_empty(self):
        result = Stream([]) \
            .count()

        self.assertEqual(0, result)

    def test_count(self):
        result = Stream([1, 2, 3]) \
            .count()

        self.assertEqual(3, result)

    def test_takeuntil(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .takeuntil(lambda x: x != 3) \
            .collect(list)

        self.assertListEqual([1, 2, 2, 4, 5], result)

    def test_takeuntil_with_generator(self):
        result = Stream(range(10)) \
            .takeuntil(lambda x: x <= 3) \
            .collect(list)

        self.assertListEqual([0, 1, 2, 3], result)

    def test_dropuntil(self):
        result = Stream([1, 2, 2, 4, 5, 3, 2, 3, 5]) \
            .dropuntil(lambda x: x != 3) \
            .collect(list)

        self.assertListEqual([3, 2, 3, 5], result)

    def test_dropuntil_with_generator(self):
        result = Stream(range(10)) \
            .dropuntil(lambda x: x <= 3) \
            .collect(list)

        self.assertListEqual([4, 5, 6, 7, 8, 9], result)

    def test_error_empty(self):
        def err_fn(x):
            if x <= 3:
                return x
            raise ValueError(x)

        err_messages = []

        def err_handler(err):
            err_messages.append(
                f"encountered {type(err).__name__} with the value {err.args}")

        Stream([]) \
            .map(err_fn) \
            .catch(err_handler) \
            .collect(list)

        self.assertListEqual([], err_messages)

    def test_error(self):
        def err_fn(x):
            if x <= 6:
                return x
            raise ValueError(x)

        err_messages = []

        def err_handler(err):
            err_messages.append(
                f"encountered {type(err).__name__} with the value {err.args}")

        result = Stream([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) \
            .map(err_fn) \
            .catch(err_handler) \
            .filter(lambda x: x % 2 == 0) \
            .collect(list)

        self.assertEqual(4, len(err_messages))
        self.assertTrue("7" in err_messages[0])
        self.assertTrue("8" in err_messages[1])
        self.assertTrue("9" in err_messages[2])
        self.assertTrue("10" in err_messages[3])
        for msg in err_messages:
            self.assertTrue("ValueError" in msg)

        self.assertListEqual([2, 4, 6], result)

    def test_multiple_catch(self):
        def err_fn_1(x):
            if x <= 3:
                raise ValueError(x)
            return x

        def err_fn_2(x):
            if 2 <= x <= 6:
                raise KeyError(x)
            return x

        err_messages_1 = []
        err_messages_2 = []

        def err_handler_1(err):
            err_messages_1.append(
                f"encountered {type(err).__name__} with the value {err.args}")

        def err_handler_2(err):
            err_messages_2.append(
                f"encountered {type(err).__name__} with the value {err.args}")

        result = Stream([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) \
            .map(err_fn_1) \
            .catch(err_handler_1) \
            .map(err_fn_2) \
            .filter(lambda x: x % 2 == 0) \
            .catch(err_handler_2) \
            .collect(list)

        self.assertEqual(3, len(err_messages_1))
        self.assertTrue("1" in err_messages_1[0])
        self.assertTrue("2" in err_messages_1[1])
        self.assertTrue("3" in err_messages_1[2])

        self.assertEqual(3, len(err_messages_2))
        self.assertTrue("4" in err_messages_2[0])
        self.assertTrue("5" in err_messages_2[1])
        self.assertTrue("6" in err_messages_2[2])

        for msg in err_messages_1:
            self.assertTrue("ValueError" in msg)
        for msg in err_messages_2:
            self.assertTrue("KeyError" in msg)

        self.assertListEqual([8, 10], result)

    def test_error_with_return_val(self):
        def err_fn(x):
            if x <= 6:
                return x
            raise ValueError(x)

        def err_handler(err):
            (value,) = err.args
            return value + 10

        result = Stream([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) \
            .map(err_fn) \
            .catch(err_handler) \
            .filter(lambda x: x % 2 == 0) \
            .collect(list)

        self.assertListEqual([2, 4, 6, 18, 20], result)

    def test_error_with_specific_error_type(self):
        def err_fn(x):
            if x == 'a':
                raise ValueError(x)
            if x == 'b':
                raise KeyError(x)
            return x

        def handle_value_err(err):
            (value,) = err.args
            return value * 2

        def handle_key_err(err):
            (value,) = err.args
            return value * 4

        result = Stream(['e', 'a', 'g', 'd', 'b']) \
            .map(err_fn) \
            .catch(handle_value_err, ValueError) \
            .catch(handle_key_err, KeyError) \
            .collect(list)

        self.assertListEqual(['e', 'aa', 'g', 'd', 'bbbb'], result)
