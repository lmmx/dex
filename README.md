# dex

Library index:

- Reliable metadata handling from ISBN numbers
- Robust modern OCR of book indexes from neural networks pretrained for document image analysis
- Data are managed as 'shelves':
  - If installing from a clone of the git repo, the files will be stored within the repo
  - If installing from PyPI, you must set the `DEX_SHELVES` environment variable with a path to
    locate the source files

Further handling of the data remains to be done:
- [ ] Clean up errors in the transcription (punctuation etc.) as far as possible
  - Perhaps use low confidence to assist manual corrections if viable?
  - It may also be useful to try `layoutparser` as a '2nd opinion' (but the interface seems more complicated).
- [ ] Geometry has been commented out of the data model, this could be useful to parse the layout. I
  would prefer to try avoiding this using simple alphabetical heuristics.


Additionally, I suggest serialising the outputs to JSON and storing alongside the images, to avoid
reloading from the images each time.

## Requires

- Python 3.10+

## Installation

> _dex_ is available from [PyPI](https://pypi.org/project/spindex), and
> the code is on [GitHub](https://github.com/lmmx/dex)

In theory you can install as follows:

```sh
pip install spindex[surya]
```

In practice, the suggested installation is stored in `CONDA_SETUP.md`:

```
conda create -n dex python=3.10 -y
conda activate dex
conda install pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
pip install spindex[surya]
```

See the PyTorch docs for other ways to install the PyTorch dependency.

## Usage

To prepare your library, photograph the index pages and store them in folders named by the ISBNs of
the books. You then load your library metadata in `dex` like so:

```py
>>> import dex
>>> l = dex.load_library()
>>> l
Library of 6 books
>>> l.items[0].metadata
'📖: Szeliski (2010) Computer Vision - Algorithms And Applications'
>>> l.items[0].metadata.title
'Computer Vision - Algorithms And Applications'
>>> l.items[0].metadata.first_author
'Richard Szeliski'
>>> l.items[0].metadata.first_author.surname
'Szeliski'
```

There's a helper method to scan the images of all the items in the library, `Library.scan()`
(**deprecated**)

For a sense of what's inside, here's a "manual" version for one book:

To show a bit more, you can see there's a bit more work to be done in cleaning up this output but
the results are very promising.

The first step of the following [dense] snippet is to:
- process the library's ISBNs (the `l = dex.load_library()` helper function)),
- take the first item in the library (`i = l.items[0]`)
- and scan its page images (`i.scan_images()`)

We can then group its words together by line, taking the first page image as example
(iterating through all the 'blocks' identified on it by the page layout detection algorithm)

An error creeps in here where the entry for "Alternating minimization" has 4 page numbers: 97, 106,
199, 252. The first three are on the same line as the entry label, but the 252 spills onto another
line and is split apart by the layout parsing algorithm. Fortunately this can be detected in a
couple of ways:

- The alphabetical order in an index should be monotonic (obviously), and there are multiple chances
  to establish this in each block
- The only time a number would appear in a block on its own would be if it was the page number or if
  one had been split apart like this.
- Note that the block from 'Averages' through to 'Bregman distance' got inserted in between, and
  this is in fact the entire right column of the page: so shifting it after the next alphabetically
  preceding block (the end of the block from "Antisymmetric" through "Average pooling") would place
  it in the correct position.
- Care must be taken as a page number could also appear at the top of the page. I suspect this will
  end up being unambiguous, however a multi-page processor should be able to identify monotonically
  increasing sequences of consecutive numbers and label them as page numbers of the index.

---

**DEPRECATED**

Previously the `DocTreeDoc` class (a nested data structure with all the words, lines, etc.) is stored
on the `scanned` attribute of each `Book` in the `Library` object you get from
`dex.load_library()`.

A naive approach can work with these to create the labels, but it helps to use geometry for c(l)ues.

The geometry bounding boxes are the (x,y) coordinates of the top-left and bottom-right corners.
It's clear that the first and second row are aligned on their left-hand side as the x value of their
top-left is very similar: 0.1044, 0.1035 mostly. However the second block also has 0.140 and 0.141,
which could either be a column or an indent in the entry.

An indent in the entry can either be a sub-entry or the continuation of the line (in which case
you'd expect it to be a numeric string, though possibly Roman numeric!)
