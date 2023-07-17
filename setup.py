# pip3 install setuptools twine
# python3 setup.py sdist bdist_wheel
# twine upload dist/*

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with (HERE / "requirements.txt").open() as f:
    requirements = f.read().splitlines()

setup(
    name="amnis",
    version="0.1.1",
    description="Java like Stream Api for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zahash/amnis",
    author="zahash",
    author_email="zahash.z@gmail.com",
    license="MIT",
    python_requires='>=3.7',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["amnis"],
    include_package_data=True,
    install_requires=requirements,
)
