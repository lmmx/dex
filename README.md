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

For a sense of what's inside, here's a "manual" version for one book:

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

---

Currently the `DocTreeDoc` class (a nested data structure with all the words, lines, etc.) is stored
on the `scanned` attribute of each `LibraryItem` in the `Library` object you get from
`dex.load_library()`.

```py
>>> i = l.items[0]
>>> i.scan_images()
>>> for b in i.scanned.pages[0].blocks:
...     for line in b.lines: print([w.value for w in line.words])
...     print()
...
['Index']

['3D', 'Rotations,', 'see', 'Rotations']
['3D', 'alignment,', '283']
['absolute', 'orientation,', '283,', '515']
['orthogonal', 'Procrustes,', '283']
['3D', 'photography,', '537']
['3D', 'video,', '564']

['Applications,', '5']

['3D', 'model', 'reconstruction,', '319,327']
['3D', 'photography,', '537']
['augmented', 'reality,', '287,', '325']
['automotive', 'safety,', '5']
['background', 'replacement,', '489']
['biometrics,', '588']
['colorization,', '442']
['de-interlacing,', '364']
['digital', 'heritage,', '517']
['document', 'scanning,', '379']
['edge', 'editing,', '219']
['facial', 'animation,', '528']
['flash', 'photography,', '434']
['frame', 'interpolation,', '368']
['gaze', 'correction,', '483']
['head', 'tracking,', '483']
['hole', 'filling,', '457']
['image', 'restoration,', '169']
['image', 'search,', '630']
['industrial,', '5']
['intelligent', 'photo', 'editing,', '621']
['Internet', 'photos,', '327']
['location', 'recognition,', '609']
['machine', 'inspection,', '5']
['match', 'move,', '324']
['medical', 'imaging,', '5,', '268,358']
['morphing,', '152']
['mosaic-based', 'video', 'compression,', '383']
['non-photorealistic', 'rendering,', '458']
['Optical', 'character', 'recognition', '(OCR),', '5']
['panography,', '277']
['performance-driven', 'animation,', '209']
['photo', 'pop-up,', '623']

['Absolute', 'orientation,', '283,', '515']
['Active', 'appearance', 'model', '(AAM),598']
['Active', 'contours,', '238']
['Active', 'illumination,', '512']
['Active', 'rangefinding,', '512']
['Active', 'shape', 'model', '(ASM),', '243,598']
['Activity', 'recognition,', '534']
['Adaptive', 'smoothing,', '111']
['Affine', 'transforms,', '34,37']
['Affinities', '(segmentation),', '260']
['normalizing,', '262']
['Algebraic', 'multigrid,', '254']
['Algorithms']
['testing,', 'viii']
['Aliasing,', '69,', '417']
['Alignment,', 'see', 'Image', 'alignment']
['Alpha']
['opacity,', '93']
['pre-mulupled,', '93']
['Alpha', 'matte,', '93']
['Ambient', 'illumination,', '58']
['Analog', 'to', 'digital', 'conversion', '(ADC),', '68']
['Anisotropic', 'diffusion,', '111']
['Anisotropic', 'filtering,', '148']
['Anti-aliasing', 'filter,', '70,', '417']
['Aperture,', '62']
['Aperture', 'problem,', '347']
```

A naive approach can work with these to create the labels, but it helps to use geometry for c(l)ues.

```
>>> for b in i.scanned.pages[0].blocks:
...     for line in b.lines: print([(w.value, w.geometry) for w in line.words])
...     print()
...
[('Index', ((0.1044921875, 0.115234375), (0.2236328125, 0.146484375)))]

[('3D', ((0.103515625, 0.2265625), (0.130859375, 0.2421875))), ('Rotations,', ((0.1318359375, 0.224609375), (0.212890625, 0.2421875))), ('see', ((0.212890625, 0.2265625), (0.244140625, 0.2412109375))), ('Rotations', ((0.2451171875, 0.2255859375), (0.3232421875, 0.2392578125)))]
[('3D', ((0.103515625, 0.24609375), (0.130859375, 0.26171875))), ('alignment,', ((0.130859375, 0.2451171875), (0.21484375, 0.2626953125))), ('283', ((0.216796875, 0.244140625), (0.2509765625, 0.259765625)))]
[('absolute', ((0.140625, 0.2646484375), (0.2080078125, 0.279296875))), ('orientation,', ((0.2099609375, 0.2646484375), (0.3017578125, 0.279296875))), ('283,', ((0.3046875, 0.2646484375), (0.3427734375, 0.2802734375))), ('515', ((0.3427734375, 0.2626953125), (0.3779296875, 0.28125)))]
[('orthogonal', ((0.1416015625, 0.28515625), (0.2265625, 0.2998046875))), ('Procrustes,', ((0.2294921875, 0.283203125), (0.3193359375, 0.30078125))), ('283', ((0.3212890625, 0.283203125), (0.3544921875, 0.298828125)))]
[('3D', ((0.103515625, 0.3046875), (0.130859375, 0.3203125))), ('photography,', ((0.130859375, 0.3037109375), (0.234375, 0.3212890625))), ('537', ((0.236328125, 0.302734375), (0.2705078125, 0.318359375)))]
[('3D', ((0.103515625, 0.3232421875), (0.1298828125, 0.33984375))), ('video,', ((0.12890625, 0.322265625), (0.181640625, 0.33984375))), ('564', ((0.181640625, 0.322265625), (0.2158203125, 0.337890625)))]

[('Applications,', ((0.5517578125, 0.228515625), (0.6572265625, 0.24609375))), ('5', ((0.6591796875, 0.2275390625), (0.673828125, 0.244140625)))]

[('3D', ((0.5888671875, 0.2470703125), (0.6181640625, 0.263671875))), ('model', ((0.619140625, 0.248046875), (0.6708984375, 0.2626953125))), ('reconstruction,', ((0.671875, 0.25), (0.7900390625, 0.263671875))), ('319,327', ((0.7919921875, 0.2470703125), (0.865234375, 0.265625)))]
[('3D', ((0.5888671875, 0.2666015625), (0.6181640625, 0.283203125))), ('photography,', ((0.6201171875, 0.26953125), (0.72265625, 0.2841796875))), ('537', ((0.724609375, 0.267578125), (0.7578125, 0.283203125)))]
[('augmented', ((0.58984375, 0.2890625), (0.677734375, 0.3037109375))), ('reality,', ((0.6787109375, 0.287109375), (0.7373046875, 0.3046875))), ('287,', ((0.7392578125, 0.287109375), (0.7763671875, 0.302734375))), ('325', ((0.7763671875, 0.287109375), (0.8095703125, 0.302734375)))]
[('automotive', ((0.58984375, 0.3076171875), (0.6796875, 0.3212890625))), ('safety,', ((0.6806640625, 0.3056640625), (0.7353515625, 0.32421875))), ('5', ((0.736328125, 0.3056640625), (0.7509765625, 0.322265625)))]
[('background', ((0.5908203125, 0.3271484375), (0.68359375, 0.341796875))), ('replacement,', ((0.6865234375, 0.3271484375), (0.7890625, 0.341796875))), ('489', ((0.791015625, 0.3251953125), (0.8251953125, 0.3408203125)))]
[('biometrics,', ((0.58984375, 0.3466796875), (0.6787109375, 0.361328125))), ('588', ((0.681640625, 0.3447265625), (0.71484375, 0.3603515625)))]
[('colorization,', ((0.58984375, 0.3662109375), (0.689453125, 0.380859375))), ('442', ((0.69140625, 0.3642578125), (0.7255859375, 0.3798828125)))]
[('de-interlacing,', ((0.58984375, 0.3857421875), (0.7041015625, 0.400390625))), ('364', ((0.70703125, 0.3837890625), (0.7412109375, 0.3994140625)))]
[('digital', ((0.587890625, 0.4033203125), (0.6416015625, 0.421875))), ('heritage,', ((0.642578125, 0.404296875), (0.71484375, 0.421875))), ('517', ((0.7158203125, 0.4033203125), (0.75, 0.4189453125)))]
[('document', ((0.5888671875, 0.4248046875), (0.6689453125, 0.4384765625))), ('scanning,', ((0.669921875, 0.4248046875), (0.748046875, 0.439453125))), ('379', ((0.7509765625, 0.4228515625), (0.783203125, 0.4384765625)))]
[('edge', ((0.587890625, 0.4423828125), (0.6298828125, 0.4609375))), ('editing,', ((0.62890625, 0.4423828125), (0.6923828125, 0.4599609375))), ('219', ((0.693359375, 0.4423828125), (0.7275390625, 0.4580078125)))]
[('facial', ((0.58984375, 0.4619140625), (0.6337890625, 0.4775390625))), ('animation,', ((0.63671875, 0.462890625), (0.72265625, 0.4775390625))), ('528', ((0.724609375, 0.4619140625), (0.7587890625, 0.4775390625)))]
[('flash', ((0.5888671875, 0.4814453125), (0.62890625, 0.4970703125))), ('photography,', ((0.630859375, 0.4833984375), (0.7353515625, 0.498046875))), ('434', ((0.736328125, 0.4794921875), (0.7724609375, 0.498046875)))]
[('frame', ((0.5888671875, 0.5009765625), (0.63671875, 0.515625))), ('interpolation,', ((0.640625, 0.501953125), (0.7470703125, 0.5166015625))), ('368', ((0.7490234375, 0.5009765625), (0.783203125, 0.5166015625)))]
[('gaze', ((0.587890625, 0.5224609375), (0.62890625, 0.537109375))), ('correction,', ((0.6298828125, 0.521484375), (0.7158203125, 0.5361328125))), ('483', ((0.7177734375, 0.5205078125), (0.751953125, 0.53515625)))]
[('head', ((0.587890625, 0.5390625), (0.6298828125, 0.5537109375))), ('tracking,', ((0.630859375, 0.5390625), (0.703125, 0.556640625))), ('483', ((0.703125, 0.5380859375), (0.7392578125, 0.556640625)))]
[('hole', ((0.5888671875, 0.55859375), (0.626953125, 0.5732421875))), ('filling,', ((0.626953125, 0.55859375), (0.6826171875, 0.576171875))), ('457', ((0.681640625, 0.5576171875), (0.7177734375, 0.576171875)))]
[('image', ((0.58984375, 0.5791015625), (0.640625, 0.595703125))), ('restoration,', ((0.642578125, 0.580078125), (0.7333984375, 0.5947265625))), ('169', ((0.7373046875, 0.5771484375), (0.7724609375, 0.595703125)))]
[('image', ((0.5888671875, 0.59765625), (0.6416015625, 0.615234375))), ('search,', ((0.640625, 0.59765625), (0.701171875, 0.615234375))), ('630', ((0.703125, 0.59765625), (0.736328125, 0.61328125)))]
[('industrial,', ((0.58984375, 0.6181640625), (0.671875, 0.6328125))), ('5', ((0.6728515625, 0.6171875), (0.6875, 0.6328125)))]
[('intelligent', ((0.5908203125, 0.63671875), (0.6728515625, 0.654296875))), ('photo', ((0.67578125, 0.638671875), (0.7236328125, 0.654296875))), ('editing,', ((0.724609375, 0.6376953125), (0.7880859375, 0.65625))), ('621', ((0.7900390625, 0.6376953125), (0.8232421875, 0.6552734375)))]
[('Internet', ((0.5908203125, 0.6572265625), (0.6552734375, 0.671875))), ('photos,', ((0.6572265625, 0.6572265625), (0.7177734375, 0.6748046875))), ('327', ((0.7177734375, 0.65625), (0.7529296875, 0.6748046875)))]
[('location', ((0.5908203125, 0.6767578125), (0.6572265625, 0.69140625))), ('recognition,', ((0.658203125, 0.677734375), (0.7578125, 0.6953125))), ('609', ((0.7578125, 0.677734375), (0.79296875, 0.6923828125)))]
[('machine', ((0.5908203125, 0.6962890625), (0.6611328125, 0.7109375))), ('inspection,', ((0.662109375, 0.697265625), (0.751953125, 0.71484375))), ('5', ((0.7529296875, 0.697265625), (0.767578125, 0.712890625)))]
[('match', ((0.5908203125, 0.716796875), (0.642578125, 0.7314453125))), ('move,', ((0.642578125, 0.71875), (0.6953125, 0.7333984375))), ('324', ((0.697265625, 0.716796875), (0.7314453125, 0.732421875)))]
[('medical', ((0.591796875, 0.736328125), (0.65625, 0.7509765625))), ('imaging,', ((0.658203125, 0.736328125), (0.7314453125, 0.7548828125))), ('5,', ((0.732421875, 0.736328125), (0.7548828125, 0.75390625))), ('268,358', ((0.7509765625, 0.7353515625), (0.8251953125, 0.7529296875)))]
[('morphing,', ((0.591796875, 0.7578125), (0.6748046875, 0.7724609375))), ('152', ((0.6787109375, 0.755859375), (0.7119140625, 0.771484375)))]
[('mosaic-based', ((0.591796875, 0.7763671875), (0.701171875, 0.7900390625))), ('video', ((0.7041015625, 0.775390625), (0.7509765625, 0.7900390625))), ('compression,', ((0.7529296875, 0.77734375), (0.857421875, 0.7919921875))), ('383', ((0.8583984375, 0.7734375), (0.89453125, 0.7919921875)))]
[('non-photorealistic', ((0.5927734375, 0.796875), (0.736328125, 0.810546875))), ('rendering,', ((0.7392578125, 0.794921875), (0.8232421875, 0.8125))), ('458', ((0.8232421875, 0.794921875), (0.857421875, 0.810546875)))]
[('Optical', ((0.5908203125, 0.8134765625), (0.65234375, 0.8310546875))), ('character', ((0.654296875, 0.81640625), (0.73046875, 0.8291015625))), ('recognition', ((0.7314453125, 0.814453125), (0.82421875, 0.83203125))), ('(OCR),', ((0.826171875, 0.8134765625), (0.892578125, 0.8310546875))), ('5', ((0.8857421875, 0.8134765625), (0.9013671875, 0.8291015625)))]
[('panography,', ((0.5908203125, 0.833984375), (0.6904296875, 0.8515625))), ('277', ((0.69140625, 0.833984375), (0.7255859375, 0.849609375)))]
[('performance-driven', ((0.591796875, 0.8544921875), (0.7490234375, 0.869140625))), ('animation,', ((0.751953125, 0.8544921875), (0.837890625, 0.869140625))), ('209', ((0.83984375, 0.853515625), (0.873046875, 0.869140625)))]
[('photo', ((0.5908203125, 0.873046875), (0.6396484375, 0.888671875))), ('pop-up,', ((0.640625, 0.875), (0.705078125, 0.8896484375))), ('623', ((0.70703125, 0.873046875), (0.740234375, 0.888671875)))]

[('Absolute', ((0.1044921875, 0.36328125), (0.1728515625, 0.3779296875))), ('orientation,', ((0.17578125, 0.3623046875), (0.26953125, 0.3798828125))), ('283,', ((0.271484375, 0.36328125), (0.30859375, 0.37890625))), ('515', ((0.310546875, 0.36328125), (0.3447265625, 0.37890625)))]
[('Active', ((0.103515625, 0.3828125), (0.1552734375, 0.3974609375))), ('appearance', ((0.15625, 0.384765625), (0.248046875, 0.3994140625))), ('model', ((0.25, 0.3828125), (0.3037109375, 0.3974609375))), ('(AAM),598', ((0.3046875, 0.3828125), (0.40625, 0.400390625)))]
[('Active', ((0.103515625, 0.40234375), (0.1552734375, 0.4169921875))), ('contours,', ((0.158203125, 0.4052734375), (0.2314453125, 0.4169921875))), ('238', ((0.234375, 0.40234375), (0.267578125, 0.4169921875)))]
[('Active', ((0.103515625, 0.421875), (0.1552734375, 0.4365234375))), ('illumination,', ((0.1572265625, 0.4228515625), (0.259765625, 0.4365234375))), ('512', ((0.2626953125, 0.421875), (0.2978515625, 0.4365234375)))]
[('Active', ((0.1025390625, 0.44140625), (0.1552734375, 0.4560546875))), ('rangefinding,', ((0.15625, 0.44140625), (0.2646484375, 0.458984375))), ('512', ((0.265625, 0.44140625), (0.30078125, 0.45703125)))]
[('Active', ((0.1025390625, 0.4609375), (0.1552734375, 0.4755859375))), ('shape', ((0.15625, 0.4619140625), (0.2041015625, 0.4775390625))), ('model', ((0.2060546875, 0.4609375), (0.259765625, 0.4755859375))), ('(ASM),', ((0.2607421875, 0.4609375), (0.3271484375, 0.478515625))), ('243,598', ((0.3271484375, 0.4619140625), (0.3984375, 0.4765625)))]
[('Activity', ((0.1025390625, 0.48046875), (0.16796875, 0.498046875))), ('recognition,', ((0.169921875, 0.482421875), (0.2666015625, 0.4970703125))), ('534', ((0.26953125, 0.48046875), (0.302734375, 0.49609375)))]
[('Adaptive', ((0.1025390625, 0.5), (0.1728515625, 0.5185546875))), ('smoothing,', ((0.1767578125, 0.501953125), (0.2666015625, 0.5166015625))), ('111', ((0.2705078125, 0.5), (0.302734375, 0.515625)))]
[('Affine', ((0.1015625, 0.5205078125), (0.15234375, 0.53515625))), ('transforms,', ((0.1552734375, 0.5205078125), (0.24609375, 0.53515625))), ('34,37', ((0.248046875, 0.5185546875), (0.3037109375, 0.5361328125)))]
[('Affinities', ((0.1025390625, 0.5400390625), (0.1767578125, 0.5546875))), ('(segmentation),', ((0.1796875, 0.541015625), (0.3037109375, 0.5556640625))), ('260', ((0.306640625, 0.5390625), (0.341796875, 0.5546875)))]
[('normalizing,', ((0.1396484375, 0.560546875), (0.240234375, 0.5751953125))), ('262', ((0.244140625, 0.55859375), (0.2783203125, 0.57421875)))]
[('Algebraic', ((0.1025390625, 0.5791015625), (0.1787109375, 0.5966796875))), ('multigrid,', ((0.1826171875, 0.5791015625), (0.2646484375, 0.5966796875))), ('254', ((0.265625, 0.5791015625), (0.2998046875, 0.5947265625)))]
[('Algorithms', ((0.103515625, 0.5986328125), (0.1923828125, 0.6162109375)))]
[('testing,', ((0.138671875, 0.619140625), (0.19921875, 0.63671875))), ('viii', ((0.2001953125, 0.6181640625), (0.2314453125, 0.6337890625)))]
[('Aliasing,', ((0.1025390625, 0.6376953125), (0.173828125, 0.6552734375))), ('69,', ((0.17578125, 0.638671875), (0.2041015625, 0.6552734375))), ('417', ((0.2041015625, 0.638671875), (0.2392578125, 0.654296875)))]
[('Alignment,', ((0.1025390625, 0.658203125), (0.19140625, 0.67578125))), ('see', ((0.1923828125, 0.66015625), (0.22265625, 0.6748046875))), ('Image', ((0.22265625, 0.658203125), (0.2763671875, 0.67578125))), ('alignment', ((0.27734375, 0.658203125), (0.3603515625, 0.67578125)))]
[('Alpha', ((0.1025390625, 0.6767578125), (0.15234375, 0.6953125)))]
[('opacity,', ((0.1396484375, 0.69921875), (0.203125, 0.7138671875))), ('93', ((0.2041015625, 0.697265625), (0.2294921875, 0.7138671875)))]
[('pre-mulupled,', ((0.1416015625, 0.71875), (0.2666015625, 0.7333984375))), ('93', ((0.259765625, 0.716796875), (0.2841796875, 0.7333984375)))]
[('Alpha', ((0.1044921875, 0.736328125), (0.15234375, 0.751953125))), ('matte,', ((0.1533203125, 0.73828125), (0.2041015625, 0.7529296875))), ('93', ((0.205078125, 0.736328125), (0.23046875, 0.7529296875)))]
[('Ambient', ((0.10546875, 0.7568359375), (0.171875, 0.7685546875))), ('illumination,', ((0.17578125, 0.7568359375), (0.27734375, 0.771484375))), ('58', ((0.279296875, 0.755859375), (0.3037109375, 0.7724609375)))]
[('Analog', ((0.103515625, 0.7744140625), (0.1630859375, 0.79296875))), ('to', ((0.162109375, 0.775390625), (0.18359375, 0.7919921875))), ('digital', ((0.18359375, 0.775390625), (0.2373046875, 0.79296875))), ('conversion', ((0.23828125, 0.7763671875), (0.3271484375, 0.791015625))), ('(ADC),', ((0.328125, 0.775390625), (0.3916015625, 0.79296875))), ('68', ((0.3916015625, 0.7744140625), (0.4169921875, 0.791015625)))]
[('Anisotropic', ((0.103515625, 0.7939453125), (0.1962890625, 0.8115234375))), ('diffusion,', ((0.19921875, 0.7958984375), (0.275390625, 0.810546875))), ('111', ((0.279296875, 0.794921875), (0.3095703125, 0.810546875)))]
[('Anisotropic', ((0.103515625, 0.814453125), (0.1962890625, 0.83203125))), ('filtering,', ((0.19921875, 0.814453125), (0.2685546875, 0.83203125))), ('148', ((0.2705078125, 0.814453125), (0.3037109375, 0.830078125)))]
[('Anti-aliasing', ((0.1044921875, 0.833984375), (0.2060546875, 0.8515625))), ('filter,', ((0.208984375, 0.8349609375), (0.2529296875, 0.8505859375))), ('70,', ((0.25390625, 0.833984375), (0.283203125, 0.8505859375))), ('417', ((0.2822265625, 0.833984375), (0.3173828125, 0.849609375)))]
[('Aperture,', ((0.1025390625, 0.853515625), (0.1787109375, 0.87109375))), ('62', ((0.1796875, 0.853515625), (0.2041015625, 0.8701171875)))]
[('Aperture', ((0.1025390625, 0.873046875), (0.173828125, 0.890625))), ('problem,', ((0.17578125, 0.8740234375), (0.2490234375, 0.8916015625))), ('347', ((0.2509765625, 0.873046875), (0.2841796875, 0.888671875)))]
```

The geometry bounding boxes are the (x,y) coordinates of the top-left and bottom-right corners.
It's clear that the first and second row are aligned on their left-hand side as the x value of their
top-left is very similar: 0.1044, 0.1035 mostly. However the second block also has 0.140 and 0.141,
which could either be a column or an indent in the entry.

An indent in the entry can either be a sub-entry or the continuation of the line (in which case
you'd expect it to be a numeric string, though possibly Roman numeric!)
