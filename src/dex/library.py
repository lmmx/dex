from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from pathlib import Path

from pydantic import BaseModel, DirectoryPath, ValidationError

from .dewarping import dewarp_and_save
from .isbn_utils import BookMetadata, get_isbn_metadata, isbn_ta
from .log_utils import Console
from .multiproc_utils import batch_multiprocess
from .path_utils import dewarped_path, has_been_dewarped, shelves_path

__all__ = ["load_library"]

logger = Console(name=__name__).logger


def load_library(n: int | None = None) -> Library:
    """Pass ``n`` to just load that number of shelves (used for fast dev iteration)."""
    dirs = Shelving().shelves[:n]
    # Filter non-null results from calling `LibraryItem.from_shelf` on all `shelf_dirs`
    return Library(items=filter(None, map(LibraryItem.from_shelf, dirs)))


class Shelving(BaseModel):
    root_dir: DirectoryPath = shelves_path

    @property
    def shelves(self) -> list[DirectoryPath]:
        return [p for p in self.root_dir.iterdir() if p.is_dir()]


class Library(BaseModel):
    items: list[LibraryItem]

    def __repr__(self):
        n = len(self.items)
        return f"Library of {n} book{'s'[:n-1]}" if n else "Empty library"

    def scan(self) -> None:
        for i in self.items:
            i.scan_images()

    @property
    def sorted_items(self) -> list[LibraryItem]:
        return sorted(self.items, key=LibraryItem._sort_by)


@dataclass
class LibraryItem:
    metadata: BookMetadata
    shelf: Path | None
    # scanned: None

    @classmethod
    def from_shelf(cls, shelf_dir: Path) -> LibraryItem | None:
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

    def scan_images(self) -> None:
        """
        Save dewarped versions of the images for this item if any have not been made
        yet. If any can't be dewarped, warn the user but continue anyway.

        Scan the text in the images into the :attr:`scanned` attribute.
        """
        image_suffixes = ".png .jpg .jpeg".split()
        item_images = [p for p in self.shelf.iterdir() if p.suffix in image_suffixes]
        item_images_to_dewarp = [p for p in item_images if not has_been_dewarped(p)]
        dewarp_funcs = [partial(dewarp_and_save, p) for p in item_images_to_dewarp]
        if dewarp_funcs:
            batch_multiprocess(dewarp_funcs)
        # Sort so that the scanned results will also be sorted
        dewarped_images = sorted(  # noqa: F841
            [dewarped_path(p) for p in item_images if has_been_dewarped(p)],
        )
        unfixed = [p for p in item_images if not has_been_dewarped(p)]
        if any(unfixed):
            logger.warning(f"Failed to dewarp all images for item {self.shelf.stem}")
            logger.info(f"Undewarped images: {unfixed}")
        else:
            logger.debug(f"Dewarped all images for item {self.shelf.stem}")
        # self.scanned = None  # Removed LayoutLMv3 capabilities here
        return

    def _sort_by(self) -> tuple[str, str]:
        return (self.metadata.first_author.surname, self.metadata.title)
