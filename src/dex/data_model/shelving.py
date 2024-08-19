from __future__ import annotations

from contextlib import suppress
from functools import cached_property
from pathlib import Path
from typing import Iterator

from pydantic import (
    BaseModel,
    DirectoryPath,
    RootModel,
    ValidationError,
    computed_field,
)

from ..isbn_utils import BookMetadata
from ..path_utils import shelves_path
from .images import Dewarped, Photo

__all__ = ["Shelving", "Library", "Book", "Shelf"]


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

    @computed_field
    @property
    def has_ocr(self) -> bool:
        return self.shelf.surya_ocr_results.exists()

    @cached_property
    def images(self) -> list[Photo]:
        return list(self.shelf.iter_images(dewarped=False))

    @cached_property
    def dewarped_images(self) -> list[Dewarped]:
        return list(self.shelf.iter_images(dewarped=True))

    def _sort_by(self) -> tuple[str, str]:
        return (self.metadata.first_author.surname, self.metadata.title)


class Shelf(RootModel):
    root: Path

    @property
    def dewarped_dir(self) -> Path:
        return self.root / "dewarped"

    @property
    def surya_ocr_results(self) -> Path:
        return self.dewarped_dir / "results" / "surya" / "results.json"

    def iter_images(self, dewarped=False) -> Iterator[Photo] | Iterator[Dewarped]:
        """A more structured alternative to iterating over file extensions."""
        source_dir = self.dewarped_dir if dewarped else self.root
        if source_dir.exists():
            for path in source_dir.iterdir():
                with suppress(ValidationError):
                    yield Dewarped(path) if dewarped else Photo(path)
