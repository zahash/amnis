from collections import defaultdict
from contextlib import suppress
from functools import reduce, partial
from typing import *

Grouper = NamedTuple(
    "Grouper",
    [
        ("collection", Any),
        ("grouper_fn", Callable[[Any, Any], Any])
    ]
)

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class Stream(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self._iterator: Iterator[T] = iter(iterable)

    def __iter__(self) -> Iterator[T]:
        return self._iterator

    def __next__(self) -> T:
        return next(self._iterator)

    def apply(self, fn: Callable[[Iterable[T]], Iterable[U]]) -> "Stream[U]":
        return Stream(fn(self))

    def catch(self, handler: Callable[["Exception"], Any], err_type=Exception) -> "Stream":
        def _catch(iterable: Iterable) -> Iterable:
            while True:
                try:
                    yield next(iter(iterable))
                except StopIteration:
                    break
                except err_type as ex:
                    return_val = handler(ex)
                    if return_val is not None:
                        yield return_val

        return self.apply(_catch)

    def map(self, fn: Callable[[T], U]) -> "Stream[U]":
        return self.apply(partial(map, fn))

    def filter(self, fn: Callable[[T], bool]) -> "Stream[T]":
        return self.apply(partial(filter, fn))

    def flatten(self) -> "Stream[Iterable[T]]":
        def _flatten(nested_iterable: Iterable[Iterable[T]]) -> Iterable[T]:
            for iterable in nested_iterable:
                yield from iterable

        return self.apply(_flatten)

    def flatmap(self, fn: Callable[[T], Iterable[U]]) -> "Stream[U]":
        return self.map(fn).flatten()

    def distinct(self) -> "Stream[T]":
        def _distinct(iterable: Iterable[T]) -> Iterable[T]:
            seen = set()
            for item in iterable:
                if item not in seen:
                    yield item
                    seen.add(item)

        return self.apply(_distinct)

    def sorted(self) -> "Stream[T]":
        return self.apply(sorted)

    def limit(self, n: int) -> "Stream[T]":
        def _limit(iterable: Iterable[T], n: int) -> Iterable[T]:
            for item in iterable:
                if n == 0:
                    break
                yield item
                n -= 1

        return self.apply(partial(_limit, n=max(n, 0)))

    def skip(self, n: int) -> "Stream[T]":
        def _skip(iterable: Iterable[T], n: int) -> Iterable[T]:
            for item in iterable:
                if n == 0:
                    yield item
                    break
                n -= 1
            yield from iterable

        return self.apply(partial(_skip, n=max(n, 0)))

    def takeuntil(self, fn: Callable[[T], bool]) -> "Stream[T]":
        def _takeuntil(iterable: Iterable[T]) -> Iterable[T]:
            for item in iterable:
                if not fn(item):
                    break
                yield item

        return self.apply(_takeuntil)

    def skipuntil(self, fn: Callable[[T], bool]) -> "Stream[T]":
        def _skipuntil(iterable: Iterable[T]) -> Iterable[T]:
            for item in iterable:
                if not fn(item):
                    yield item
                    break

            yield from iterable

        return self.apply(_skipuntil)

    def first(self) -> Optional[T]:
        return self.nth(0)

    def nth(self, n: int) -> Optional[T]:
        for item in self:
            if n == 0:
                return item
            n -= 1

    def last(self) -> Optional[T]:
        last_item = None
        for item in self:
            last_item = item
        return last_item

    def collect(self, collector: Callable[[Iterable], Iterable] = iter) -> Union[Sequence, Iterable, AbstractSet]:
        return collector(self)

    def reduce(self, fn: Callable[[T, T], T], initial=None) -> Optional[T]:
        with suppress(TypeError):  # thrown when stream is empty without initial value
            return reduce(fn, self, initial) if initial is not None else reduce(fn, self)

    def max(self, key: Callable[[T], U] = lambda x: x) -> Optional[T]:
        with suppress(ValueError):  # thrown when stream is empty
            return max(self, key=key)

    def min(self, key: Callable[[T], U] = lambda x: x) -> Optional[T]:
        with suppress(ValueError):  # thrown when stream is empty
            return min(self, key=key)

    def find(self, fn: Callable[[T], bool]) -> Optional[T]:
        return self.filter(fn).first()

    def foreach(self, fn: Callable[[T], None]) -> None:
        for item in self:
            fn(item)

    def group(self, key_fn: Callable[[T], U], val_fn: Callable[[T], V], grouper: Grouper) -> dict:
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

    def allmatch(self, fn: Callable[[T], bool]) -> bool:
        return all(fn(item) for item in self)

    def anymatch(self, fn: Callable[[T], bool]) -> bool:
        return any(fn(item) for item in self)

    def count(self) -> int:
        size = 0
        for _ in self:
            size += 1
        return size
