import unittest

from amnis import Stream


class TestCatch(unittest.TestCase):
    def test_catch_empty(self):
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

    def test_catch(self):
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

    def test_catch_with_return_val(self):
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

    def test_catch_with_specific_error_type(self):
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
