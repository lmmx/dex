# dex

Library index:

- Reliable metadata handling from ISBN numbers
- Robust modern OCR of book indexes from neural networks pretrained for document image analysis
- Data are managed as 'shelves':
  - If installing from a clone of the git repo, the files will be stored within the repo
  - If installing from PyPI, you must set the `DEX_SHELVES` environment variable with a path to
    locate the source files


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

To prepare your library, photograph the index pages and store them in folders named by the ISBNs of
the books. You then load your library metadata in `dex` like so:

```py
>>> import dex
>>> l = dex.load_library()
>>> l
Library of 1 book
>>> l.items
[LibraryItem(metadata='📖: Strang (2019) Linear Algebra And Learning From Data', shelf_path=PosixPath('/home/louis/dev/dex/data/shelves/9780692196380'))]
>>> l.items[0].metadata
'📖: Strang (2019) Linear Algebra And Learning From Data'
>>> l.items[0].metadata.title
'Linear Algebra And Learning From Data'
>>> l.items[0].metadata.first_author
'Gilbert Strang'
>>> l.items[0].metadata.first_author_surname
'Strang'
```

The next step is to scan the images in these directories.
