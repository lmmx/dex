from __future__ import annotations

import re
from dataclasses import dataclass
from functools import partial
from pathlib import Path

from .isbn_utils import BookMetadata, get_isbn_metadata
from .log_utils import Console
from .multiproc_utils import batch_multiprocess_with_return
from .ocr_utils import scan_text_in_images
from .path_utils import shelves_path

__all__ = ["load_library"]

logger = Console(name=__name__).logger


def load_library() -> Library:
    shelf_dirs = list(filter(Path.is_dir, shelves_path.iterdir()))
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
        return cls(items=shelf_items)


class IndexedItem:
    isbn_regex = r"[0-9]{10,13}"

    @property
    def is_shelved(self) -> bool:
        return self.shelf is not None


@dataclass
class LibraryItem(IndexedItem):
    metadata: BookMetadata
    shelf_path: Path | None

    @classmethod
    def from_isbn(cls, isbn_code: str, shelf_path: Path | None = None) -> LibraryItem:
        metadata = get_isbn_metadata(isbn_code)
        return cls(metadata=metadata, shelf_path=shelf_path)

    @classmethod
    def from_shelf(cls, shelf_dir: Path) -> LibraryItem:
        try:
            isbn_code = next(re.finditer(cls.isbn_regex, shelf_dir.stem)).group()
        except StopIteration:
            logger.error(f"Could not detect ISBN in filename {zipfile.stem} (omitting)")
        else:
            return cls.from_isbn(isbn_code=isbn_code, shelf_path=shelf_dir)
