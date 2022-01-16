# dex

Library index:

- Data managed as ZIP files
  - If installing from a clone of the git repo, the files will be stored within the repo
  - If installing from PyPI, you must set the `DEX_SHELVES` environment variable with a path to
    locate the source files

## TODO

- [x] Find how to get metadata from ISBN
- [ ] Choose robust modern OCR method

## Requires

- Python 3.9+

## Installation

```sh
pip install spindex
```

> _dex_ is available from [PyPI](https://pypi.org/project/spindex), and
> the code is on [GitHub](https://github.com/lmmx/dex)

## Usage

```py
>>> import dex
>>> dex.load_library()
[INFO] Library contains 1 files
[[LibraryItem(metadata='📖: Strang (2019) Linear Algebra And Learning From Data',
archive_path=PosixPath('/home/louis/dev/dex/data/shelves/dex9780692196380.zip'))]]
```
