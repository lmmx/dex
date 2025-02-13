from __future__ import annotations

from pathlib import Path
from collections.abc import Iterator

from pydantic import ValidationError

from .data_model import Book, Library, Shelf, Shelving
from .isbn_utils import get_isbn_metadata, isbn_ta
from .log_utils import Console

__all__ = ["load_library", "take_books_from_shelves"]

logger = Console(name=__name__).logger


def load_library(n: int | None = None) -> Library:
    """Pass ``n`` to just load that number of shelves (used for fast dev iteration)."""
    dirs = Shelving().shelves[:n]
    # Filter non-null results from calling `Book.from_shelf` on all `shelf_dirs`
    return Library(items=take_books_from_shelves(dirs))


def take_books_from_shelves(shelves: list[Path]) -> Iterator[Book]:
    """TODO: this should not be a class method, make a `shelves` module."""
    for shelf_dir in shelves:
        dir_name = shelf_dir.stem
        try:
            isbn_code = isbn_ta.validate_strings(dir_name)
        except ValidationError:
            logger.warning(f"Could not detect ISBN in {dir_name=} (omitting)")
        else:
            metadata = get_isbn_metadata(isbn_code)
            yield Book(metadata=metadata, shelf=Shelf(top=shelf_dir))
