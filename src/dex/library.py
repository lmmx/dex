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
    pattern = "dex*.zip"
    zipfiles = [*shelves_path.glob(pattern)]
    lib = Library.from_zips(zipfiles)
    return lib


class Library(list):
    def __init__(self, library_items: list[LibraryItem]):
        if not library_items:
            logger.info("Library is empty")
        else:
            logger.info(f"Library contains {len(library_items)} files")
        self.append(library_items)

    @classmethod
    def from_zips(cls, zipfiles: list[Path], parallel: bool = False):
        if parallel:
            zip_items = batch_multiprocess_with_return(
                function_list=[partial(LibraryItem.from_zip, zf) for zf in zipfiles]
            )
        else:
            zip_items = [LibraryItem.from_zip(zf) for zf in zipfiles]
        return cls(library_items=zip_items)


class IndexedItem:
    isbn_regex = r"[0-9]{10,13}"

    @property
    def is_archived(self) -> bool:
        return self.archive is not None

    @classmethod
    def from_isbn(cls, isbn_code: str, archive_path: Path | None = None) -> LibraryItem:
        metadata = get_isbn_metadata(isbn_code)
        return cls(metadata=metadata, archive_path=archive_path)

    @classmethod
    def from_zip(cls, zipfile: Path) -> LibraryItem:
        suffixes = [".zip"]
        if zipfile.suffix not in suffixes:
            raise ValueError(f"{zipfile} not recognised as a ZIP file")
        try:
            isbn_code = next(re.finditer(cls.isbn_regex, zipfile.stem)).group()
        except StopIteration:
            logger.error(f"Could not detect ISBN in filename {zipfile.stem} (omitting)")
        else:
            return cls.from_isbn(isbn_code=isbn_code, archive_path=zipfile)


@dataclass
class LibraryItem(IndexedItem):
    metadata: BookMetadata
    archive_path: Path | None
