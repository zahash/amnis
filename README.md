
<div align="center">

<pre>
 █████╗ ███╗   ███╗███╗   ██╗██╗███████╗
██╔══██╗████╗ ████║████╗  ██║██║██╔════╝
███████║██╔████╔██║██╔██╗ ██║██║███████╗
██╔══██║██║╚██╔╝██║██║╚██╗██║██║╚════██║
██║  ██║██║ ╚═╝ ██║██║ ╚████║██║███████║
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝
----------------------------------------
Java like Streams Api for Python
</pre>

[![PyPI](https://img.shields.io/pypi/v/amnis.svg)](https://pypi.org/project/amnis/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Streams are lazy evaluated -- That is, evaluation starts only when a terminal operation is applied

</div>

## Installation

pip install this repo.
(Note: Incompatible with Python 2.x)

```sh
pip3 install amnis
```

(or)

```sh
pip install amnis
```


# Usage examples


## `allmatch`

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


## `anymatch`

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


## `catch`

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


## `collect`

Collect the elements in the stream into a collection.

This method collects the elements in the stream and returns them as a collection,
determined by the provided collector function. The default collector is `iter`,
which returns an iterable containing the elements.

```Python
from amnis import Stream

result = Stream([1, 2, 3]).collect(list)

# [1, 2, 3]
```


## `count`

Count the number of elements in the stream.

This method returns the total number of elements in the stream.

```Python
from amnis import Stream

result = Stream(['a', 'b', 'c']).count()

# 3
```


## `distinct`

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


## `filter`

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


## `find`

Find the first element that matches a condition in the stream.

This method returns the first element from the stream that satisfies the condition
defined by the provided function `fn`. If no matching element is found, `None` is returned.

```Python
from amnis import Stream

result = Stream([5, 4, 3, 2, 1]).find(lambda x: x % 2 == 0)

# 4
```


## `first`

Get the first element from the stream.

This method returns the first element from the stream, or `None` if the stream is empty.

```Python
from amnis import Stream

result = Stream([1, 2, 3]).first()

# 1
```


## `flatmap`

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


## `flatten`

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


## `foreach`

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


## `group`

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


## `inspect`

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


## `last`

Get the last element from the stream.

This method returns the last element from the stream, or `None` if the stream is empty.

```Python
from amnis import Stream

result = Stream([1, 2, 3]).last()

# 3
```


## `limit`

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


## `map`

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


## `max`

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


## `min`

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


## `nomatch`

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


## `nth`

Get the element at the nth position in the stream.

This method returns the element at the specified position `n` in the stream. If the
position is out of bounds, `None` is returned. The position index is zero-based.
Negative indexes are not supported.

```Python
from amnis import Stream

result = Stream([1, 2, 3]).nth(1)

# 2
```


## `par_map`

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


## `reduce`

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


## `skip`

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


## `skipwhile`

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


## `sorted`

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


## `takewhile`

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


## `window`

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



## Development setup

Clone this repo and install packages listed in requirements.txt

```sh
pip3 install -r requirements.txt
```

## Meta

M. Zahash - zahash.z@gmail.com

Distributed under the MIT license. See `LICENSE` for more information.

[https://github.com/zahash/](https://github.com/zahash/)

## Contributing

1. Fork it (<https://github.com/zahash/amnis/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

