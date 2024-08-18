from __future__ import annotations

from contextlib import suppress
from functools import cached_property
from pathlib import Path
from typing import ClassVar, Iterator

from pydantic import (
    BaseModel,
    DirectoryPath,
    FilePath,
    RootModel,
    ValidationError,
    field_validator,
)

from .isbn_utils import BookMetadata, get_isbn_metadata, isbn_ta
from .log_utils import Console
from .path_utils import shelves_path

__all__ = ["load_library"]

logger = Console(name=__name__).logger


def load_library(n: int | None = None) -> Library:
    """Pass ``n`` to just load that number of shelves (used for fast dev iteration)."""
    dirs = Shelving().shelves[:n]
    # Filter non-null results from calling `Book.from_shelf` on all `shelf_dirs`
    return Library(items=filter(None, map(Book.from_shelf, dirs)))


class Shelving(BaseModel):
    root_dir: DirectoryPath = shelves_path

    @property
    def shelves(self) -> list[DirectoryPath]:
        return [p for p in self.root_dir.iterdir() if p.is_dir()]


class Library(BaseModel):
    items: list[Book]

    def __repr__(self):
        n = len(self.items)
        return f"Library of {n} book{'s'[:n-1]}" if n else "Empty library"

    @property
    def sorted_items(self) -> list[Book]:
        return sorted(self.items, key=Book._sort_by)


class Book(BaseModel):
    metadata: BookMetadata
    shelf: Shelf
    # scanned: None

    @cached_property
    def images(self) -> list[Photo]:
        return list(self.shelf.iter_images())

    @classmethod
    def from_shelf(cls, shelf_dir: Path) -> Book | None:
        """TODO: this should not be a class method, make a `shelves` module."""
        dir_name = shelf_dir.stem
        try:
            isbn_code = isbn_ta.validate_strings(dir_name)
        except ValidationError:
            logger.warning(f"Could not detect ISBN in {dir_name=} (omitting)")
            return None
        else:
            metadata = get_isbn_metadata(isbn_code)
            return cls(metadata=metadata, shelf=shelf_dir)

    def _sort_by(self) -> tuple[str, str]:
        return (self.metadata.first_author.surname, self.metadata.title)


class Shelf(RootModel):
    root: Path

    def iter_images(self) -> Iterator[Photo]:
        """A more structured alternative to iterating over file extensions."""
        for path in self.root.iterdir():
            with suppress(ValidationError):
                yield Photo(path)


class Photo(RootModel):
    """An existing file path with PNG/JPG suffix."""

    suffixes: ClassVar[str] = [".png", ".jpg", ".jpeg"]

    root: FilePath

    @field_validator("root", mode="after")
    @classmethod
    def is_image(cls, v: FilePath) -> FilePath:
        if v.suffix not in cls.suffixes:
            raise ValueError(f"File suffix {v.suffix} is not in {cls.suffixes}")
        return v
