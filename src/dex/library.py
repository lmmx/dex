from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from .data_model import Book, Library, Shelving
from .isbn_utils import get_isbn_metadata, isbn_ta
from .log_utils import Console

__all__ = ["load_library"]

logger = Console(name=__name__).logger


def load_library(n: int | None = None) -> Library:
    """Pass ``n`` to just load that number of shelves (used for fast dev iteration)."""
    dirs = Shelving().shelves[:n]
    # Filter non-null results from calling `Book.from_shelf` on all `shelf_dirs`
    return Library(items=filter(None, map(take_book_from_shelf, dirs)))


def take_book_from_shelf(shelf_dir: Path) -> Book | None:
    """TODO: this should not be a class method, make a `shelves` module."""
    dir_name = shelf_dir.stem
    try:
        isbn_code = isbn_ta.validate_strings(dir_name)
    except ValidationError:
        logger.warning(f"Could not detect ISBN in {dir_name=} (omitting)")
        return None
    else:
        metadata = get_isbn_metadata(isbn_code)
        return Book(metadata=metadata, shelf=shelf_dir)
