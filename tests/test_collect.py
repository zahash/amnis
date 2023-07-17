import unittest

from amnis import Stream


class TestCollect(unittest.TestCase):
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

        with self.assertRaises(StopIteration):
            next(result)

    def test_collect_with_list(self):
        result = Stream([1, 2, 3]) \
            .collect(list)

        self.assertListEqual([1, 2, 3], result)

    def test_collect_with_set(self):
        result = Stream([1, 2, 3]) \
            .collect(set)

        self.assertSetEqual({1, 2, 3}, result)

    def test_collect_with_dict(self):
        result = Stream([(1, 2), (3, 4)]) \
            .collect(dict)

        self.assertDictEqual({1: 2, 3: 4}, result)
