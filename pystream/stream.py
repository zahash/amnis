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
        return Stream(fn(self))

    def catch(self, handler: Callable[[Any], Any], err_type=Exception) -> "Stream":
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

        return self.apply(partial(_catch, handler=handler, err_type=err_type))

    def map(self, fn: Callable[[Any], Any]) -> "Stream":
        return self.apply(partial(map, fn))

    def filter(self, fn: Callable[[Any], bool]) -> "Stream":
        return self.apply(partial(filter, fn))

    def flatten(self) -> "Stream":
        return self.apply(lambda iterable: (item for sublist in iterable for item in sublist))

    def flatmap(self, fn: Callable[[Any], Iterable]) -> "Stream":
        return self.map(fn).flatten()

    def distinct(self) -> "Stream":
        def _distinct(iterable: Iterable) -> Iterable:
            seen = set()
            for item in iterable:
                if item not in seen:
                    yield item
                    seen.add(item)

        return self.apply(_distinct)

    def sorted(self) -> "Stream":
        return self.apply(sorted)

    def limit(self, n: int) -> "Stream":
        def _limit(iterable: Iterable, n: int) -> Iterable:
            for item in iterable:
                if n == 0:
                    break
                yield item
                n -= 1

        return self.apply(partial(_limit, n=max(n, 0)))

    def skip(self, n: int) -> "Stream":
        def _skip(iterable: Iterable, n: int) -> Iterable:
            it = iter(iterable)
            for item in it:
                if n == 0:
                    yield item
                    break
                n -= 1
            yield from it

        return self.apply(partial(_skip, n=max(n, 0)))

    def takeuntil(self, fn: Callable[[Any], bool]) -> "Stream":
        def _takeuntil(iterable: Iterable, fn: Callable[[Any], bool]) -> Iterable:
            for item in iterable:
                if not fn(item):
                    break
                yield item

        return self.apply(partial(_takeuntil, fn=fn))

    def skipuntil(self, fn: Callable[[Any], bool]) -> "Stream":
        def _skipuntil(iterable: Iterable, fn: Callable[[Any], bool]) -> Iterable:
            it = iter(iterable)

            for item in it:
                if not fn(item):
                    yield item
                    break

            yield from it

        return self.apply(partial(_skipuntil, fn=fn))

    def first(self) -> Optional[Any]:
        return self.nth(0)

    def nth(self, n: int) -> Optional[Any]:
        for item in self:
            if n == 0:
                return item
            n -= 1

    def last(self) -> Optional[Any]:
        last_item = None
        for item in self:
            last_item = item
        return last_item

    def collect(self, collector: Callable[[Iterable], Iterable] = iter) -> Union[Sequence, Iterable, AbstractSet]:
        return collector(self)

    def reduce(self, fn: Callable[[Any, Any], Any], initial=None) -> Optional[Any]:
        try:
            return reduce(fn, self, initial) if initial is not None else reduce(fn, self)
        except TypeError:  # thrown when stream is empty without initial value
            return None

    def max(self, key: Callable[[Any], Any] = lambda x: x) -> Optional[Any]:
        _max = None
        for item in self:
            if _max is None or key(item) > key(_max):
                _max = item
        return _max

    def min(self, key: Callable[[Any], Any] = lambda x: x) -> Optional[Any]:
        _min = None
        for item in self:
            if _min is None or key(item) < key(_min):
                _min = item
        return _min

    def find(self, fn: Callable[[Any], bool]) -> Optional[Any]:
        return self.filter(fn).first()

    def foreach(self, fn: Callable[[Iterable], None]) -> None:
        for item in self:
            fn(item)

    def group(self, key_fn: Callable[[Any], Any], val_fn: Callable[[Any], Any], grouper: Grouper) -> dict:
        d = defaultdict(grouper.collection)
        for item in self:
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
        return all(fn(item) for item in self)

    def anymatch(self, fn: Callable[[Any], bool]) -> bool:
        return any(fn(item) for item in self)

    def count(self) -> int:
        size = 0
        for _ in self:
            size += 1
        return size
