# pystream

> Java like Streams Api for Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python package for Java like Streams. pystreams are lazy evaluated -- That is, evaluation starts only when a terminal
operation is applied

## Installation

pip install this repo.
(Note: Incompatible with Python 2.x)

```sh
pip3 install git+https://github.com/zahash/pystream.git
```

(or)

```sh
pip install git+https://github.com/zahash/pystream.git
```

## Usage examples

map and filter

```Python
from pystream import Stream

result = Stream([1, 2, 3]) \
    .filter(lambda x: x > 1) \
    .map(lambda x: x * 2) \
    .collect(list)

# [4, 6]
```

reduce

```Python
from pystream import Stream
import operator

result = Stream([1, 2, 3]) \
    .filter(lambda x: x > 1) \
    .map(lambda x: x * 2) \
    .reduce(operator.add, initial=20)

# 30
```

```Python
from pystream import Stream

result = Stream([1, 2, 3]) \
    .filter(lambda x: x > 1) \
    .map(lambda x: x * 2) \
    .reduce(lambda x, y: x + y, initial=20)

# 30
```

first

```Python
from pystream import Stream

result = Stream([1, 2, 3]) \
    .map(lambda x: x * 2) \
    .filter(lambda x: x > 1) \
    .first()

# 2
```

foreach

```Python
from pystream import Stream

Stream([1, 2, 3]) \
    .map(lambda x: x * 2) \
    .filter(lambda x: x > 1) \
    .foreach(print)

# >>> 2
# >>> 4
# >>> 6
```

distinct

```Python
from pystream import Stream

result = Stream([3, 2, 3, 1, 3, 2, 2]) \
    .map(lambda x: x * 2) \
    .distinct() \
    .filter(lambda x: x > 1) \
    .collect(list)

# [6, 4, 2]
```

group with list

```Python
from pystream import Stream, Grouper

class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age

result = Stream([Person("jack", 20), Person("jack", 30), Person("jill", 25)]) \
            .group(key_fn=lambda p: p.name,
                   val_fn=lambda p: p.age,
                   grouper=Grouper(list, grouper_fn=lambda l, item: l.append(item)))

# {
#   "jack": [20, 30],
#   "jill": [25]
# }
```

group with string

```Python
from pystream import Stream, Grouper

class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age

result = Stream([Person("jack", 20), Person("jack", 30), Person("jill", 25), Person("jack", 40)]) \
            .group(key_fn=lambda p: p.name,
                   val_fn=lambda p: p.age,
                   grouper=Grouper(str, grouper_fn=lambda s, item: f"{s}, {item}" if s else f"{item}"))

# {
#   "jack": "20, 30, 40",
#   "jill": "25"
# }
```

sorted

```Python
from pystream import Stream

result = Stream([5, 4, 3, 2, 1]) \
            .map(lambda x: x - 1) \
            .sorted() \
            .filter(lambda x: x % 2 == 0) \
            .collect(list)

# [0, 2, 4]
```

limit

```Python
from pystream import Stream

result = Stream(range(100)) \
    .limit(10) \
    .collect(list)

# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

error handling

```Python
from pystream import Stream

def err_fn_1(x):
    if x <= 3:
        raise ValueError(x)
    return x

def err_fn_2(x):
    if 2 <= x <= 6:
        raise KeyError(x)
    return x

err_messages = []

def err_handler(err):
    err_messages.append(f"encountered {type(err).__name__} with the value {err.args}")

result = Stream([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) \
    .map(err_fn_1) \
    .map(err_fn_2) \
    .filter(lambda x: x % 2 == 0) \
    .catch(err_handler) \
    .collect(list)

# result = [8, 10]
# err_messages = [
#       "encountered ValueError with the value (1,)",
#       "encountered ValueError with the value (2,)",
#       "encountered ValueError with the value (3,)",
#       "encountered KeyError with the value (4,)",
#       "encountered KeyError with the value (5,)",
#       "encountered KeyError with the value (6,)"
# ]
```

error handling at granular level

```Python
from pystream import Stream

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
    err_messages_1.append(f"encountered {type(err).__name__} with the value {err.args}")

def err_handler_2(err):
    err_messages_2.append(f"encountered {type(err).__name__} with the value {err.args}")

result = Stream([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) \
    .map(err_fn_1) \
    .catch(err_handler_1) \
    .map(err_fn_2) \
    .filter(lambda x: x % 2 == 0) \
    .catch(err_handler_2) \
    .collect(list)

# result = [8, 10]
# err_messages_1 = [
#       "encountered ValueError with the value (1,)",
#       "encountered ValueError with the value (2,)",
#       "encountered ValueError with the value (3,)"
# ]
# err_messages_2 = [
#       "encountered KeyError with the value (4,)",
#       "encountered KeyError with the value (5,)",
#       "encountered KeyError with the value (6,)"
# ]
```

## Development setup

Clone this repo and install packages listed in requirements.txt

```sh
pip3 install -r requirements.txt
```

## Meta

M. Zahash – zahash.z@gmail.com

Distributed under the MIT license. See `LICENSE` for more information.

[https://github.com/zahash/](https://github.com/zahash/)

## Contributing

1. Fork it (<https://github.com/zahash/pystream/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
