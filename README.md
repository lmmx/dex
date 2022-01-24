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

```py
>>> i = items[0]
>>> i.scan_images()
>>> p1 = i.scanned.pages[0]
>>> print(p1.page_idx) # 0
>>> b1, b2, b3 = p1.blocks[0:3]
>>> [w.value for w in b1.lines[0].words]
['Index']
```

To show a bit more, you can see there's a bit more work to be done in cleaning up this output but
the results are very promising.

The first step of the following [dense] snippet is to:
- process the library's ISBNs (the `l = dex.load_library()` helper function)),
- take the first item in the library (`i = l.items[0]`)
- and scan its page images (`i.scan_images()`)

> Note: there's a helper method to scan the images of all the items in the library, `Library.scan()`

We can then group its words together by line, taking the first page image as example
(iterating through all the 'blocks' identified on it by the page layout detection algorithm)

```py 
>>> import dex; l = dex.load_library(); i = l.items[0]; i.scan_images()
>>> from pprint import pprint; pp = lambda p: pprint(p, sort_dicts=False)
>>> pp([[[w.value for w in line.words] for line in b.lines] for b in i.scanned.pages[0].blocks])
[[['Index']],
 [['Accelerated', 'descent,', '352,353'],
  ['Accuracy,', '384'],
  ['Activation,', 'iv,', '375,376'],
  ['AD,', '397'],
  ['ADAGRAD,', '366'],
  ['ADAM,', '322,', '356,366'],
  ['Adaptive,', '407'],
  ['Adaptive', 'descent,', '356,', '361'],
  ['ADI', 'method,', '182'],
  ['Adjacency', 'matrix,', '203,', '240,', '291'],
  ['Adjoint', 'equation,', '405'],
  ['Adjoint', 'methods,', '404'],
  ['ADMM,', '99,', '185,', '187,', '188'],
  ['Affine,', 'ili'],
  ['AlexNet,', 'ix,', '373,415'],
  ['Aliasing,', '234'],
  ['AlphaGo', 'Zero,', '394,412'],
  ['Alternating', 'direction,', '185,', '191'],
  ['Alternating', 'minimization,', '97,', '106,', '199,']],
 [['Averages,', '236,', '365'],
  ['Back', 'substitution,', '25'],
  ['Backpropagation,', '102,', '344,371,'],
  ['Backslash,', '113,', '184'],
  ['Backtracking,', '328,', '351'],
  ['Backward', 'difference,', '123'],
  ['Backward-mode,', '397'],
  ['Banach', 'space,', '91'],
  ['Banded,', '203,', '232'],
  ['Bandpass', 'filter,', '233'],
  ['Basis,', '4,', '5,', '15,204,', '239'],
  ['Basis', 'pursuit,', '184,', '195'],
  ['Batch', 'mode,', '361'],
  ['Batch', 'normalization,', 'X,', '409,', '412'],
  ['Bayes', 'Theorem,', '303'],
  ['Bell-shaped', 'curve,', '279'],
  ['Bernoulli,', '287'],
  ['BFGS', 'quasi-Newton),', '165'],
  ['Bias,', 'in,', '375'],
  ['Bias-variance,', '374,', '412'],
  ['Bidiagonal', 'matrix,', '120'],
  ['Big', 'picture,', '14,', '18,', '31'],
  ['Binomial,', '270,', '271,', '275,', '287'],
  ['Binomial', 'theorem,', '385'],
  ['Bipartite', 'graph,', '256,', '340'],
  ['Block', 'Toeplitz,', '389'],
  ['BLUE', 'theorem,', '308'],
  ['Bootstrap,', '408'],
  ['Boundary', 'condition,', '229'],
  ['Bounded', 'variation,', '193,194'],
  ['Bowl,', '49'],
  ['Bregman', 'distance,', '192']],
 [['252']],
 [['Antisymmetric,', '52'],
  ['Approximate', 'SVD,', '144,', '155'],
  ['Approximation,', '384'],
  ['Architecture,', '413'],
  ['Argmin,', '186,', '322'],
  ['Arnoldi,', '116,', '117'],
  ['Artificial', 'intelligence,', '371'],
  ['Associative', 'Law,', '13,', '163'],
  ['Asymptotic', 'rank,', '79'],
  ['Augmented', 'Lagrangian,', '185,', '187'],
  ['Autocorrelation,', '220'],
  ['Automatic', 'differentiation,', '371,397'],
  ['Average', 'pooling,', '379']],
 [['423']]]
```

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
