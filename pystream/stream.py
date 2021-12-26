from collections import defaultdict
from functools import reduce, partial
from typing import Iterable, Callable, Any, Union, Sequence, List, NamedTuple, AbstractSet

Grouper = NamedTuple("Grouper", [("collection", Any), ("grouper_fn", Callable[[Any, Any], Any])])


class Stream:
    def __init__(self, iterable: Iterable):
        self._iterable = iterable

    def apply(self, fn: Callable[[Iterable], Iterable]) -> "Stream":
        return Stream(fn(self._iterable))

    def map(self, fn: Callable[[Any], Any]) -> "Stream":
        return self.apply(partial(map, fn))

    def filter(self, fn: Callable[[Any], bool]) -> "Stream":
        return self.apply(partial(filter, fn))

    def distinct(self) -> "Stream":
        return self.apply(self._distinct)

    def sorted(self) -> "Stream":
        return self.apply(sorted)

    def limit(self, n: int) -> "Stream":
        return self.apply(partial(self._limit, n=n))

    @staticmethod
    def _limit(iterable: Iterable, n: int) -> Iterable:
        for item in iterable:
            if n == 0: break
            yield item
            n -= 1

    @staticmethod
    def _distinct(iterable: Iterable) -> Iterable:
        seen = set()
        for item in iterable:
            if item not in seen:
                yield item
                seen.add(item)

    def first(self) -> Any:
        return next(iter(self._iterable))

    def collect(self, collector: Callable[[Iterable], Iterable] = iter) -> Union[List, Sequence, Iterable, AbstractSet]:
        return collector(self._iterable)

    def reduce(self, fn: Callable[[Any, Any], Any], initial=None) -> Any:
        return reduce(fn, self._iterable, initial) if initial else reduce(fn, self._iterable)

    def foreach(self, fn: Callable[[Iterable], None]) -> None:
        for item in self._iterable:
            fn(item)

    def group(self, key_fn: Callable[[Any], Any], val_fn: Callable[[Any], Any], grouper: Grouper) -> dict:
        d = defaultdict(grouper.collection)
        for item in self._iterable:
            key, val = key_fn(item), val_fn(item)
            return_val = grouper.grouper_fn(d[key], val)
            # if there is no return value then it is assumed that the operation is performed inplace
            # eg: appending item to a list
            # but if there is a return value then it is assumed not inplace
            # eg: concatenating strings
            if return_val:
                d[key] = return_val
        return dict(d)

    def allmatch(self, fn: Callable[[Any], bool]):
        return all(fn(item) for item in self._iterable)

    def anymatch(self, fn: Callable[[Any], bool]):
        return any(fn(item) for item in self._iterable)
