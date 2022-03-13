import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with (HERE / "requirements.txt").open() as f:
    requirements = f.read().splitlines()

setup(
    name="pystream",
    version="0.0.2",
    description="Java like Stream pystream for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zahash/pystream",
    author="zahash",
    author_email="zahash.z@gmail.com",
    license="MIT",
    python_requires='>=3.7',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["pystream"],
    include_package_data=True,
    install_requires=requirements,
)
