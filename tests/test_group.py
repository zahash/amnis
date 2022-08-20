import unittest
from collections import namedtuple

from pystream import Stream, Grouper

Person = namedtuple("Person", ["name", "age"])


class TestGroup(unittest.TestCase):
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
