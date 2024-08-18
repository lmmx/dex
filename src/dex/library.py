from __future__ import annotations

import re
from dataclasses import dataclass
from functools import partial
from pathlib import Path

from .data_model import DocTreeDoc, LayoutLMDoc
from .dewarping import dewarp_and_save
from .isbn_utils import BookMetadata, get_isbn_metadata
from .log_utils import Console
from .multiproc_utils import batch_multiprocess, batch_multiprocess_with_return
from .path_utils import dewarped_path, has_been_dewarped, shelves_path

__all__ = ["load_library"]

logger = Console(name=__name__).logger


def load_library(n: int = 0) -> Library:
    """Pass ``n`` to just load that number of shelves (used for fast dev iteration)."""
    shelf_dirs = list(filter(Path.is_dir, shelves_path.iterdir()))
    if n > 0:
        shelf_dirs = shelf_dirs[:n]
    lib = Library.from_shelves(shelf_dirs)
    return lib


@dataclass
class Library:
    items: list[LibraryItem]

    def __repr__(self):
        n = len(self.items)
        return f"Library of {n} book{'s'[:n-1]}" if n else "Empty library"

    @classmethod
    def from_shelves(cls, shelf_dirs: list[Path], parallel: bool = False):
        if parallel:
            shelf_items = batch_multiprocess_with_return(
                function_list=[partial(LibraryItem.from_shelf, sd) for sd in shelf_dirs]
            )
        else:
            shelf_items = [LibraryItem.from_shelf(sd) for sd in shelf_dirs]
        shelf_items = [i for i in shelf_items if i is not None]  # Omit returned None
        return cls(items=shelf_items)

    def scan(self):
        for i in self.items:
            i.scan_images()

    @property
    def sorted_items(self) -> list[LibraryItem]:
        return sorted(self.items, key=LibraryItem._sortable_metadata)


class IndexedItem:
    isbn_regex = r"[0-9]{10,13}"
    scanned: DocTreeDoc | LayoutLMDoc

    @property
    def is_shelved(self) -> bool:
        return self.shelf is not None


@dataclass
class LibraryItem(IndexedItem):
    metadata: BookMetadata
    shelf: Path | None

    @classmethod
    def from_isbn(cls, isbn_code: str, shelf: Path | None = None) -> LibraryItem:
        metadata = get_isbn_metadata(isbn_code)
        return cls(metadata=metadata, shelf=shelf)

    @classmethod
    def from_shelf(cls, shelf_dir: Path) -> LibraryItem:
        try:
            isbn_code = next(re.finditer(cls.isbn_regex, shelf_dir.stem)).group()
        except StopIteration:
            logger.warning(
                f"Could not detect ISBN in filename {shelf_dir.stem} (omitting)"
            )
        else:
            return cls.from_isbn(isbn_code=isbn_code, shelf=shelf_dir)

    def scan_images(self, layoutlm: bool = True) -> None:
        """
        Save dewarped versions of the images for this item if any have not been made
        yet. If any can't be dewarped, warn the user but continue anyway.

        Scan the text in the images into the :attr:`scanned` attribute.

        If ``layoutlm`` is passed as True (default: False) then use the LayoutLMv3
        model rather than Mindee docTR (ResNet detection/VGG recognition).
        """
        image_suffixes = ".png .jpg .jpeg".split()
        item_images = [p for p in self.shelf.iterdir() if p.suffix in image_suffixes]
        item_images_to_dewarp = [p for p in item_images if not has_been_dewarped(p)]
        dewarp_funcs = [partial(dewarp_and_save, p) for p in item_images_to_dewarp]
        if dewarp_funcs:
            batch_multiprocess(dewarp_funcs)
        # Sort so that the scanned results will also be sorted
        dewarped_images = sorted(  # noqa: F841
            [dewarped_path(p) for p in item_images if has_been_dewarped(p)]
        )
        unfixed = [p for p in item_images if not has_been_dewarped(p)]
        if any(unfixed):
            logger.warning(f"Failed to dewarp all images for item {self.shelf.stem}")
            logger.info(f"Undewarped images: {unfixed}")
        else:
            logger.debug(f"Dewarped all images for item {self.shelf.stem}")
        self.scanned = []  # Removed LayoutLMv3 capabilities here
        return

    def _sortable_metadata(self) -> tuple[str, str]:
        return (self.metadata.first_author_surname, self.metadata.title)
