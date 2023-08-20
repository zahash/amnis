import inspect
from amnis import Stream

# Output file path for the README
README_PATH = "README.md"

PREFIX = """
<div align="center">

# amnis

_Java like Streams Api for Python_

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python package for Java like Streams. Streams are lazy evaluated -- That is, evaluation starts only when a terminal operation is applied

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
"""

SUFFIX = """
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
"""


def generate_readme():
    with open(README_PATH, "w") as readme:
        def write_line(s=""):
            readme.write(f"{s}\n")

        write_line(PREFIX)
        write_line()

        write_line("# Usage examples")
        write_line()
        for method_name, method in inspect.getmembers(Stream, inspect.isfunction):
            if method.__doc__:
                write_line()
                write_line(f"## `{method_name}`")
                write_line()

                for line in inspect.cleandoc(method.__doc__).splitlines():
                    write_line(f"{line}")

                write_line()

        write_line()
        write_line(SUFFIX)
        print("README generated successfully.")


if __name__ == "__main__":
    generate_readme()
