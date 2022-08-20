from collections import defaultdict
from functools import reduce, partial
from typing import *

Grouper = NamedTuple(
    "Grouper",
    [
        ("collection", Any),
        ("grouper_fn", Callable[[Any, Any], Any])
    ]
)


class Stream:
    def __init__(self, iterable: Iterable):
        self._iterable = iterable

    def __iter__(self):
        return iter(self._iterable)

    def apply(self, fn: Callable[[Iterable], Iterable]) -> "Stream":
        return Stream(fn(self._iterable))

    def catch(self, handler: Callable[[Any], Any], err_type=Exception) -> "Stream":
        return self.apply(partial(self._catch, handler=handler, err_type=err_type))

    @staticmethod
    def _catch(iterable: Iterable, handler: Callable[["Exception"], Any], err_type) -> Iterable:
        it = iter(iterable)
        while True:
            try:
                item = next(it)
                yield item
            except StopIteration:
                break
            except err_type as ex:
                return_val = handler(ex)
                if return_val is not None:
                    yield return_val

    def map(self, fn: Callable[[Any], Any]) -> "Stream":
        return self.apply(partial(map, fn))

    def filter(self, fn: Callable[[Any], bool]) -> "Stream":
        return self.apply(partial(filter, fn))

    def flatten(self) -> "Stream":
        return self.apply(lambda iterable: (item for sublist in iterable for item in sublist))

    def flatmap(self, fn: Callable[[Any], Iterable]) -> "Stream":
        return self.map(fn).flatten()

    def distinct(self) -> "Stream":
        return self.apply(self._distinct)

    @staticmethod
    def _distinct(iterable: Iterable) -> Iterable:
        seen = set()
        for item in iterable:
            if item not in seen:
                yield item
                seen.add(item)

    def sorted(self) -> "Stream":
        return self.apply(sorted)

    def limit(self, n: int) -> "Stream":
        return self.apply(partial(self._limit, n=n))

    @staticmethod
    def _limit(iterable: Iterable, n: int) -> Iterable:
        for item in iterable:
            if n == 0:
                break
            yield item
            n -= 1

    def takeuntil(self, fn: Callable[[Any], bool]) -> "Stream":
        return self.apply(partial(self._takeuntil, fn=fn))

    @staticmethod
    def _takeuntil(iterable: Iterable, fn: Callable[[Any], bool]) -> Iterable:
        for item in iterable:
            if not fn(item):
                break
            yield item

    def dropuntil(self, fn: Callable[[Any], bool]) -> "Stream":
        return self.apply(partial(self._dropuntil, fn=fn))

    @staticmethod
    def _dropuntil(iterable: Iterable, fn: Callable[[Any], bool]) -> Iterable:
        start_allowing = False
        for item in iterable:
            if not fn(item):
                start_allowing = True

            if start_allowing:
                yield item

    def first(self) -> Optional[Any]:
        try:
            return next(iter(self._iterable))
        except StopIteration:
            return None

    def collect(self, collector: Callable[[Iterable], Iterable] = iter) -> Union[Sequence, Iterable, AbstractSet]:
        return collector(self._iterable)

    def reduce(self, fn: Callable[[Any, Any], Any], initial=None) -> Optional[Any]:
        try:
            return reduce(fn, self._iterable, initial) if initial is not None else reduce(fn, self._iterable)
        except TypeError:  # thrown when stream is empty without initial value
            return None

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
            if return_val is not None:
                d[key] = return_val
        return dict(d)

    def allmatch(self, fn: Callable[[Any], bool]) -> bool:
        return all(fn(item) for item in self._iterable)

    def anymatch(self, fn: Callable[[Any], bool]) -> bool:
        return any(fn(item) for item in self._iterable)

    def count(self) -> int:
        size = 0
        for _ in self._iterable:
            size += 1
        return size
