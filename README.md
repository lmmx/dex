# dex

Library index:

- Data managed as ZIP files
  - If installing from a clone of the git repo, the files will be stored within the repo
  - If installing from PyPI, you must set the `DEX_SHELVES` environment variable with a path to
    locate the source files

## Key features

- Reliable metadata handling from ISBN numbers
- Robust modern OCR of book indexes from neural networks pretrained for document image analysis

## Requires

- Python 3.9+

## Installation

> _dex_ is available from [PyPI](https://pypi.org/project/spindex), and
> the code is on [GitHub](https://github.com/lmmx/dex)

In theory you can install as follows:

```sh
pip install spindex
```

In practice, the suggested installation is stored in `CONDA_SETUP.md`:

```
conda create -n dex "python=3.9"
conda activate dex
conda install -y pytorch torchvision cudatoolkit=11.3 -c pytorch
pip install -r requirements.txt
```

For earlier versions of CUDA:
```
conda install -y "cudatoolkit<11.2" -c conda-forge
conda install -y pytorch torchvision -c pytorch
```

## Usage

```py
>>> import dex
>>> dex.load_library()
[INFO] Library contains 1 files
[[LibraryItem(metadata='📖: Strang (2019) Linear Algebra And Learning From Data',
archive_path=PosixPath('/home/louis/dev/dex/data/shelves/dex9780692196380.zip'))]]
```
