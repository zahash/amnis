# amnis

> Java like Streams Api for Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python package for Java like Streams. Streams are lazy evaluated -- That is, evaluation starts only when a terminal
operation is applied

## Installation

pip install this repo.
(Note: Incompatible with Python 2.x)

```sh
pip3 install git+https://github.com/zahash/amnis.git
```

(or)

```sh
pip install git+https://github.com/zahash/amnis.git
```

## Usage examples

### map

```Python
from amnis import Stream

result = (Stream([1, 2, 3])
    .map(lambda x: x * 2)
    .collect(list))

# [2, 4, 6]
```

### filter

```Python
from amnis import Stream

result = (Stream([1, 2, 3])
    .filter(lambda x: x > 1)
    .collect(list))

# [2, 3]
```

### reduce

```Python
from amnis import Stream
import operator

result = (Stream([1, 2, 3])
    .reduce(operator.add, initial=20))

# 26
```

```Python
from amnis import Stream

result = (Stream([1, 2, 3])
    .reduce(lambda x, y: x + y, initial=20))

# 26
```

### map, filter and reduce

```Python
from amnis import Stream

result = (Stream([1, 2, 3])
    .map(lambda x: x * 2)
    .filter(lambda x: x > 2)
    .reduce(lambda x, y: x + y, initial=0))

# 10
```

### iterate

```Python
from amnis import Stream

stream = Stream([1, 2, 3])

result = []
for n in stream:
    result.append(n)

# [1, 2, 3]
```

### iterate with map, filter

```Python
from amnis import Stream

stream = (Stream([1, 2, 3])
    .map(lambda x: x * 2)
    .filter(lambda x: x > 2))

result = []
for n in stream:
    result.append(n)

# [4, 6]
```

### flatten

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

### flatmap

```Python
from amnis import Stream

result = (Stream(["it's Sunny in", "", "California"])
            .flatmap(lambda s: s.split(" "))
            .collect(list))

# ["it's", "Sunny", "in", "", "California"]
```

flatmap is exactly the same as doing map and flatten

```Python
from amnis import Stream

result = (Stream(["it's Sunny in", "", "California"])
            .map(lambda s: s.split(" "))
            .flatten()
            .collect(list))

# ["it's", "Sunny", "in", "", "California"]
```

### first

```Python
from amnis import Stream

result = Stream([1, 2, 3]).first()

# 1
```

### foreach

```Python
from amnis import Stream

Stream([1, 2, 3]).foreach(print)

# >>> 1
# >>> 2
# >>> 3
```

```Python
from amnis import Stream

Stream([1, 2, 3]).foreach(lambda n: print(n))

# >>> 1
# >>> 2
# >>> 3
```

### distinct

```Python
from amnis import Stream

result = (Stream([3, 2, 3, 1, 3, 2, 2])
    .distinct()
    .collect(list))

# [3, 2, 1]
```

### group with list

```Python
from amnis import Stream, Grouper

class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age

people = [
    Person("jack", 20),
    Person("jack", 30),
    Person("jill", 25)
]

result = (Stream(people)
            .group(
                key_fn=lambda p: p.name,
                val_fn=lambda p: p.age,
                grouper=Grouper(list, grouper_fn=lambda l, item: l.append(item))
            ))

# {
#   "jack": [20, 30],
#   "jill": [25]
# }
```

### group with string

```Python
from amnis import Stream, Grouper

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
                grouper=Grouper(str, grouper_fn=lambda s, item: f"{s}--{item}" if s else f"{item}")
            ))

# {
#   "jack": "20--30--40",
#   "jill": "25"
# }
```

### sorted

```Python
from amnis import Stream

# Warning: .sorted() is not lazy
result = (Stream([5, 4, 3, 2, 1])
            .sorted()
            .collect(list))

# [1, 2, 3, 4, 5]
```

### limit

```Python
from amnis import Stream

result = (Stream(range(100))
    .limit(10)
    .collect(list))

# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### count

```Python
from amnis import Stream

result = Stream(['a', 'b', 'c']).count()

# 3
```

### takeuntil

```Python
from amnis import Stream

result = (Stream([1, 2, 2, 4, 5, 3, 2, 3, 5])
            .takeuntil(lambda x: x != 3)
            .collect(list))

# [1, 2, 2, 4, 5]
```

### skipuntil

```Python
from amnis import Stream

result = (Stream([1, 2, 2, 4, 5, 3, 2, 3, 5])
            .skipuntil(lambda x: x != 3)
            .collect(list))

# [3, 2, 3, 5]
```

### allmatch

```Python
from amnis import Stream

result = (Stream(["cat", "fat", "rat"])
            .allmatch(lambda x: "at" in x))

# True
```

```Python
from amnis import Stream

result = (Stream(["cat", "dog", "rat"])
            .allmatch(lambda x: "at" in x))

# False
```

### anymatch

```Python
from amnis import Stream

result = (Stream(["cat", "dog", "rat"])
            .anymatch(lambda x: "at" in x))

# True
```

```Python
from amnis import Stream

result = (Stream(["cat", "dog", "rat"])
            .anymatch(lambda x: "z" in x))

# False
```

### error handling

```Python
from amnis import Stream
import logging

def handler(err):
    logging.error(err)

result = (Stream(['a', 'b', 'c', 10, 'd'])
    .map(lambda x: x.upper())
    .catch(handler)
    .collect(list))

# >>> ERROR:root:'int' object has no attribute 'upper'
# result = ['A', 'B', 'C', 'D']
```

### multiple error handling

```Python
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

### replace error value

```Python
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

### specific error handling

```Python
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

1. Fork it (<https://github.com/zahash/amnis/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
