from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from isbnlib import Isbn, meta
from isbnlib._exceptions import NotValidISBNError

__all__ = ["validate_isbn", "get_isbn_metadata", "BookMetadata"]


def validate_isbn(isbn_code: str) -> bool:
    try:
        Isbn(isbn_code)
    except NotValidISBNError:
        is_isbn = False
    else:
        is_isbn = True
    return is_isbn


class TitledEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.title()

    @classmethod
    def names2values(cls) -> list[str]:
        return {m.name: v for v, m in cls._value2member_map_.items()}


class MetaEnum(TitledEnum):
    """
    Internal representations of keys from the :class:`isbnlib.Isbn` class.
    """

    title = auto()
    authors = auto()
    year = auto()
    isbn_13 = "ISBN-13"
    publisher = auto()


def get_isbn_metadata(isbn_code: str) -> dict[str, str | list[str]]:
    book_metadata = meta(isbn_code)
    # title, authors, year, isbn_13, publisher = map(book_metadata.get, MetaEnum.values())
    book_meta_kwargs = {
        name: book_metadata.get(value)
        for name, value in MetaEnum.names2values().items()
    }
    meta_cls = BookMetadata(**book_meta_kwargs)
    return meta_cls


class IndexedBook:
    @property
    def first_author(self):
        return self.authors[0]

    @property
    def first_author_surname(self) -> str:
        return self.author_surname(self.first_author)

    @staticmethod
    def author_surname(name: str) -> str:
        return name.split(" ")[-1]

    @property
    def short_fmt(self) -> str:
        return f"{self.first_author_surname} ({self.year}) {self.title}"


@dataclass
class BookMetadata(IndexedBook):
    title: str
    authors: list[str]
    year: int
    publisher: str
    isbn_13: str

    def __repr__(self) -> str:
        return f"'\N{open book}: {self.short_fmt}'"
