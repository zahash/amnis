from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import suppress
from functools import reduce, partial
from typing import *
from os import cpu_count

ncpu = cpu_count()


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
        """
        Handle exceptions while iterating through the stream.

        This method returns a new Stream that applies the provided exception handler
        function `handler` to handle exceptions of a specific type `err_type` while
        iterating through the stream. The handler can return a value to continue
        iteration, or raise a different exception to propagate it.

        ```Python

        # =======
        # Logging
        # =======

        from amnis import Stream
        import logging

        def handler(err):
            logging.error(err)

        result = (Stream(['a', 'b', 'c', 10, 'd'])
            .map(lambda x: x.upper())
            .catch(handler)
            .collect(list))

        # >>> ERROR:root:'int' object has no attribute 'upper'
        # result = ['A', 'B', 'C', None, 'D']
        ```

        ```Python

        # =======================
        # Multiple Error Handling
        # =======================

        from amnis import Stream
        import logging

        def handle_upper(err):
            logging.error(err)

        def handle_index_out_of_bounds(err):
            logging.warning(err)

        result = (Stream(['ab', 'cd', 'e', 10, 'fg'])
            .map(lambda x: x.upper())
            .catch(handle_upper)
            .map(lambda x: x[1])
            .catch(handle_index_out_of_bounds)
            .collect(list))

        # >>> WARNING:root:string index out of range
        # >>> ERROR:root:'int' object has no attribute 'upper'
        # result = ['B', 'D', 'G']
        ```

        ```Python

        # ===================
        # Replace Error Value
        # ===================

        from amnis import Stream

        def sqrt(x):
            if x < 0:
                raise ValueError(x)
            return x ** 0.5

        def handler_neg_sqrt(err):
            (value,) = err.args
            return value * 1000

        result = (Stream([4, 9, -3, 16])
            .map(sqrt)
            .catch(handler_neg_sqrt)
            .collect(list))

        # [2.0, 3.0, -3000, 4.0]
        ```

        ```Python

        # =======================
        # Specific Error Handling
        # =======================

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

        result = (Stream(['e', 'a', 'g', 'd', 'b'])
            .map(err_fn)
            .catch(handle_value_err, ValueError)
            .catch(handle_key_err, KeyError)
            .collect(list))

        # ['e', 'aa', 'g', 'd', 'bbbb']
        ```
        """
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
        """
        Apply a function to each element in the stream.

        This method applies the provided function `fn` to each element in the stream 
        and returns a new Stream containing the transformed values.

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 3])
            .map(lambda x: x * 2)
            .collect(list))

        # [2, 4, 6]
        ```
        """
        return self.apply(partial(map, fn))

    def par_map(self, fn: Callable[[T], U]) -> "Stream[U]":
        """
        Parallel version of the `map` method for CPU-bound operations.
        The results may not be in the same order as the original stream due
        to the parallel execution.

        **IMPORTANT**: Lambda functions are not allowed as `fn` since they are not easily
        serializable for parallel execution. Define your mapping function as a regular
        named function.

        See the documentation for the `map` method for more details.

        ```Python
        from amnis import Stream

        def times2(x):
            return x * 2

        result = (Stream([1, 2, 3])
            .par_map(times2)
            .collect(list))

        # [2, 4, 6]
        ```
        """
        def _par_map(iterable: Iterable[T]) -> Iterable[U]:
            with ProcessPoolExecutor(max_workers=ncpu) as executor:
                yield from executor.map(fn, iterable)
        return self.apply(_par_map)

    def filter(self, fn: Callable[[T], bool]) -> "Stream[T]":
        """
        Filter elements in the stream based on a given condition.

        This method filters the elements in the stream, retaining only those that satisfy
        the provided condition defined by the function `fn`.

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 3])
            .filter(lambda x: x > 1)
            .collect(list))

        # [2, 3]
        ```        
        """
        return self.apply(partial(filter, fn))

    def flatten(self) -> "Stream[Iterable[T]]":
        """
        Flatten a stream of nested iterables into a single stream.

        This method flattens a stream that contains nested iterables, such as lists or
        tuples, into a single stream of individual elements.

        ```Python
        from amnis import Stream

        result = (Stream([
                    [1, 2, 3],
                    [],
                    [4, 5]
                ])
                    .flatten()
                    .collect(list))

        # [1, 2, 3, 4, 5]
        ```
        """
        def _flatten(nested_iterable: Iterable[Iterable[T]]) -> Iterable[T]:
            for iterable in nested_iterable:
                yield from iterable
        return self.apply(_flatten)

    def flatmap(self, fn: Callable[[T], Iterable[U]]) -> "Stream[U]":
        """
        Apply a function to each element and flatten the results into a single stream.

        This method applies the provided function `fn` to each element in the stream and
        then flattens the resulting iterable of each function call into a single stream.

        flatmap is exactly the same as doing map and flatten

        ```Python
        from amnis import Stream

        result = (Stream(["it's Sunny in", "", "California"])
                    .flatmap(lambda s: s.split(" "))
                    .collect(list))

        # ["it's", "Sunny", "in", "", "California"]
        ```
        """
        return self.map(fn).flatten()

    def inspect(self, fn: Callable[[T], None]) -> "Stream[T]":
        """
        Apply a function to each element in the stream while preserving the stream's contents.

        This method returns a new Stream that applies the provided function `fn` to each
        element in the original stream. The function is called for every element, and it can
        have side effects. The original elements remain unchanged, and the new Stream still
        contains the same elements.

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 3])
                  .inspect(lambda x: print(f"before map : {x}"))
                  .map(lambda x: x * 3)
                  .inspect(lambda x: print(f"after map  : {x}"))
                  .collect(list))

        # >>> before map : 1
        # >>> after map  : 3
        # >>> before map : 2
        # >>> after map  : 6
        # >>> before map : 3
        # >>> after map  : 9
        # result = [3, 6, 9]
        ```
        """
        def _inspect(iterable: Iterable[T]) -> Iterable[T]:
            for item in iterable:
                fn(item)
                yield item
        return self.apply(_inspect)

    def window(self, window_size: int) -> "Stream[Tuple[T, ...]]":
        """
        Create a sliding window over the stream.

        This method returns a new Stream where each element is a tuple containing the elements
        of the original stream that form a sliding window of the specified size `window_size`.
        The elements within each window are ordered as they appear in the stream.

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 3, 4, 5])
                    .window(3)
                    .collect(list))

        # [
        #     (1, 2, 3),
        #     (2, 3, 4),
        #     (3, 4, 5),
        # ]

        result = (Stream([1, 2, 3, 4, 5])
                    .window(3)
                    .map(lambda w: w[0]+w[1]+w[2])
                    .collect(list))

        # [6, 9, 12]
        ```
        """
        def _window(iterable: Iterable[T]) -> Iterable[List[T]]:
            buffer = deque(maxlen=window_size)
            for item in iterable:
                buffer.append(item)
                if len(buffer) == window_size:
                    yield tuple(buffer)

        if window_size <= 0:
            return Stream([])
        return self.apply(partial(_window))

    def distinct(self) -> "Stream[T]":
        """
        Remove duplicate elements from the stream.

        This method returns a new Stream containing only the distinct elements from the
        original stream. Duplicate elements are eliminated, and only the first occurrence
        is retained.

        ```Python
        from amnis import Stream

        result = (Stream([3, 2, 3, 1, 3, 2, 2])
            .distinct()
            .collect(list))

        # [3, 2, 1]
        ```        
        """
        def _distinct(iterable: Iterable[T]) -> Iterable[T]:
            seen = set()
            for item in iterable:
                if item not in seen:
                    yield item
                    seen.add(item)
        return self.apply(_distinct)

    def sorted(self, key: Callable[[T], Any] = None) -> "Stream[T]":
        """
        Sort the elements in the stream.

        This method returns a new Stream containing the elements from the original stream,
        sorted in ascending order by default. A custom sorting key can be provided using
        the `key` parameter.

        **WARNING**: Sorting is an eager operation and requires all elements to be loaded into memory.

        ```Python
        from amnis import Stream

        result = (Stream([5, 4, 3, 2, 1])
                    .sorted()
                    .collect(list))

        # [1, 2, 3, 4, 5]

        result = (Stream([(1, 4), (2, 3), (3, 2), (4, 1)])
                  .sorted(key=lambda p: p[1])
                  .collect(list))

        # [(4, 1), (3, 2), (2, 3), (1, 4)]
        ```
        """
        return self.apply(partial(sorted, key=key))

    def limit(self, n: int) -> "Stream[T]":
        """
        Limit the number of elements in the stream.

        This method returns a new Stream containing, at most, the first `n` elements from
        the original stream. If `n` is greater than the total number of elements, all
        elements from the original stream will be included.

        ```Python
        from amnis import Stream

        result = (Stream(range(100))
            .limit(10)
            .collect(list))

        # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ```
        """
        def _limit(iterable: Iterable[T], n: int) -> Iterable[T]:
            for item in iterable:
                if n == 0:
                    break
                yield item
                n -= 1
        return self.apply(partial(_limit, n=max(n, 0)))

    def skip(self, n: int) -> "Stream[T]":
        """
        Skip the first `n` elements in the stream.

        This method returns a new Stream containing the elements from the original stream
        after skipping the first `n` elements. If `n` is greater than the total number of
        elements, an empty stream will be returned.

        Stream([1, 2, 3]).skip(2)

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 3])
            .skip(2)
            .collect(list))

        # [3]
        ```
        """
        def _skip(iterable: Iterable[T], n: int) -> Iterable[T]:
            for item in iterable:
                if n == 0:
                    yield item
                    break
                n -= 1
            yield from iterable
        return self.apply(partial(_skip, n=max(n, 0)))

    def takewhile(self, fn: Callable[[T], bool]) -> "Stream[T]":
        """
        Create a new stream with elements while a condition is met.

        This method returns a new Stream that includes elements from the original stream
        as long as the provided condition defined by the function `fn` evaluates to True.
        Once an element is encountered that does not satisfy the condition, the new stream
        stops including further elements.

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 2, 4, 5, 3, 2, 3, 5])
                    .takewhile(lambda x: x < 5)
                    .collect(list))

        # [1, 2, 2, 4]
        ```
        """
        def _takewhile(iterable: Iterable[T]) -> Iterable[T]:
            for item in iterable:
                if not fn(item):
                    break
                yield item
        return self.apply(_takewhile)

    def skipwhile(self, fn: Callable[[T], bool]) -> "Stream[T]":
        """
        Create a new stream by skipping elements while a condition is met.

        This method returns a new Stream that starts including elements from the original
        stream as soon as the provided condition defined by the function `fn` evaluates to False.
        Elements before the first one that does not satisfy the condition are skipped.

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 2, 3, 5, 3, 2, 3, 5])
                    .skipwhile(lambda x: x < 3)
                    .collect(list))

        # [3, 5, 3, 2, 3, 5]
        ```
        """
        def _skipwhile(iterable: Iterable[T]) -> Iterable[T]:
            for item in iterable:
                if not fn(item):
                    yield item
                    break
            yield from iterable
        return self.apply(_skipwhile)

    def first(self) -> Optional[T]:
        """
        Get the first element from the stream.

        This method returns the first element from the stream, or `None` if the stream is empty.

        ```Python
        from amnis import Stream

        result = Stream([1, 2, 3]).first()

        # 1
        ```
        """
        return self.nth(0)

    def nth(self, n: int) -> Optional[T]:
        """
        Get the element at the nth position in the stream.

        This method returns the element at the specified position `n` in the stream. If the
        position is out of bounds, `None` is returned. The position index is zero-based.
        Negative indexes are not supported.

        ```Python
        from amnis import Stream

        result = Stream([1, 2, 3]).nth(1)

        # 2
        ```
        """
        if n < 0:
            return
        for item in self:
            if n == 0:
                return item
            n -= 1

    def last(self) -> Optional[T]:
        """
        Get the last element from the stream.

        This method returns the last element from the stream, or `None` if the stream is empty.

        ```Python
        from amnis import Stream

        result = Stream([1, 2, 3]).last()

        # 3
        ```
        """
        last_item = None
        for item in self:
            last_item = item
        return last_item

    def collect(self, collector: Callable[[Iterable], Iterable] = iter) -> Union[Sequence, Iterable, AbstractSet]:
        """
        Collect the elements in the stream into a collection.

        This method collects the elements in the stream and returns them as a collection,
        determined by the provided collector function. The default collector is `iter`,
        which returns an iterable containing the elements.

        ```Python
        from amnis import Stream

        result = Stream([1, 2, 3]).collect(list)

        # [1, 2, 3]
        ```
        """
        return collector(self)

    def reduce(self, fn: Callable[[T, T], T], initial=None) -> Optional[T]:
        """
        Reduce the elements in the stream to a single value.

        This method applies the provided binary function `fn` cumulatively to the elements
        of the stream, from left to right, and returns a single accumulated result. An
        initial value can be provided to start the accumulation; otherwise, the first element
        of the stream is used as the initial value.

        ```Python
        from amnis import Stream

        result = (Stream([1, 2, 3])
            .reduce(lambda x, y: x + y))

        # 6

        import operator

        result = (Stream([1, 2, 3])
            .reduce(operator.add, initial=20))

        # 26
        ```
        """
        with suppress(TypeError):  # thrown when stream is empty without initial value
            return reduce(fn, self, initial) if initial is not None else reduce(fn, self)

    def max(self, key: Callable[[T], U] = None) -> Optional[T]:
        """
        Find the maximum element in the stream.

        This method returns the maximum element from the stream, based on the natural
        ordering of the elements or a custom sorting key defined by the `key` parameter.

        ```Python
        from amnis import Stream

        result = Stream(["a", "bbbbb", "cc"]).max()

        # "cc"

        result = Stream(["a", "bbbbb", "cc"]).max(lambda x: len(x))

        # "bbbbb"
        ```
        """
        with suppress(ValueError):  # thrown when stream is empty
            return max(self, key=key)

    def min(self, key: Callable[[T], U] = None) -> Optional[T]:
        """
        Find the minimum element in the stream.

        This method returns the minimum element from the stream, based on the natural
        ordering of the elements or a custom sorting key defined by the `key` parameter.

        ```Python
        from amnis import Stream

        result = Stream(["cc", "aaaaa", "b"]).min()

        # "aaaaa"

        result = Stream(["cc", "aaaaa", "b"]).min(lambda x: len(x))

        # "b"
        ```
        """
        with suppress(ValueError):  # thrown when stream is empty
            return min(self, key=key)

    def find(self, fn: Callable[[T], bool]) -> Optional[T]:
        """
        Find the first element that matches a condition in the stream.

        This method returns the first element from the stream that satisfies the condition
        defined by the provided function `fn`. If no matching element is found, `None` is returned.

        ```Python
        from amnis import Stream

        result = Stream([5, 4, 3, 2, 1]).find(lambda x: x % 2 == 0)

        # 4
        ```
        """
        return self.filter(fn).first()

    def foreach(self, fn: Callable[[T], None]) -> None:
        """
        Apply a function to each element in the stream.

        This method applies the provided function `fn` to each element in the stream.
        The function can have side effects.

        ```Python
        from amnis import Stream

        Stream([1, 2, 3]).foreach(lambda x: print(x))

        # >>> 1
        # >>> 2
        # >>> 3
        ```
        """
        for item in self:
            fn(item)

    def group(self, key_fn: Callable[[T], U], val_fn: Callable[[T], V], grouper: Grouper) -> dict:
        """
        Group elements in the stream based on keys and values.

        This method groups elements in the stream based on keys and values determined by
        the provided key and value functions. The grouping logic is defined by the provided
        grouper object, which specifies how values are combined for each key.

        Parameters:
            `key_fn`: A function that takes an element of type `T` and
                returns a key of type `U` to group the elements by.
            `val_fn`: A function that takes an element of type `T` and
                returns a value of type `V` associated with the element.
            `grouper`: A Grouper object that specifies how values are combined for each key.
                The Grouper should have `collection` and `grouper_fn` attributes.

        Returns:
            dict: A dictionary where keys are the result of the key function and values
            are the results of applying the grouper function to the associated values.

        ```Python
        from amnis import Stream, Grouper

        result = (Stream(["apple", "banana", "cherry"])
                    .group(
                        key_fn=lambda word: len(word),
                        val_fn=lambda word: word.upper(),
                        grouper=Grouper(list, grouper_fn=lambda l, item: l.append(item))
                    ))

        # {5: ['APPLE'], 6: ['BANANA', 'CHERRY']}

        class Person:
            def __init__(self, name, age):
                self.name, self.age = name, age

        people = [
            Person("jack", 20),
            Person("jack", 30),
            Person("jill", 25),
            Person("jack", 40)
        ]

        result = (Stream(people)
                    .group(
                        key_fn=lambda p: p.name,
                        val_fn=lambda p: p.age,
                        grouper=Grouper(list, grouper_fn=lambda l, item: l.append(item))
                    ))

        # {
        #   "jack": [20, 30, 40],
        #   "jill": [25]
        # }

        result = (Stream(people)
                    .group(
                        key_fn=lambda p: p.name,
                        val_fn=lambda p: p.age,
                        grouper=Grouper(str, grouper_fn=lambda s, item: f"{s}--{item}" if s else f"{item}")
                    ))

        # {
        #   "jack": "20--30--40",
        #   "jill": "25"
        # }
        ```
        """
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
        """
        Check if all elements in the stream match a condition.

        This method returns `True` if all elements in the stream satisfy the condition
        defined by the provided function `fn`. If any element does not satisfy the
        condition, `False` is returned.

        ```Python
        from amnis import Stream

        result = (Stream(["cat", "fat", "rat"])
                    .allmatch(lambda x: "at" in x))

        # True

        result = (Stream(["cat", "dog", "rat"])
                    .allmatch(lambda x: "at" in x))

        # False
        ```
        """
        return all(fn(item) for item in self)

    def anymatch(self, fn: Callable[[T], bool]) -> bool:
        """
        Check if any element in the stream matches a condition.

        This method returns `True` if at least one element in the stream satisfies the
        condition defined by the provided function `fn`. If no element satisfies the
        condition, `False` is returned.

        ```Python
        from amnis import Stream

        result = (Stream(["cat", "dog", "rat"])
                    .anymatch(lambda x: "at" in x))

        # True

        result = (Stream(["cat", "dog", "rat"])
                    .anymatch(lambda x: "z" in x))

        # False
        ```
        """
        return any(fn(item) for item in self)

    def nomatch(self, fn: Callable[[T], bool]) -> bool:
        """
        Check if no elements in the stream match a condition.

        This method returns `True` if none of the elements in the stream satisfy the condition
        defined by the provided function `fn`. If any element satisfies the condition, `False`
        is returned.

        ```Python
        from amnis import Stream

        result = (Stream([3, 5, 7])
                  .nomatch(lambda x: x % 2 == 0))

        # True

        result = (Stream([3, 4, 7])
                  .nomatch(lambda x: x % 2 == 0))

        # False
        ```
        """
        return not any(fn(item) for item in self)

    def count(self) -> int:
        """
        Count the number of elements in the stream.

        This method returns the total number of elements in the stream.

        ```Python
        from amnis import Stream

        result = Stream(['a', 'b', 'c']).count()

        # 3
        ```
        """
        size = 0
        for _ in self:
            size += 1
        return size
