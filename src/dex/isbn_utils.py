from __future__ import annotations

from isbnlib import Isbn, meta


def validate_isbn(isbn_code: str) -> bool:
    try:
        Isbn(isbn_code)
    except NotValidISBNError:
        is_isbn = False
    else:
        is_isbn = True
    return is_isbn


def get_isbn_metadata(isbn_code: str) -> dict[str, str | list[str]]:
    book_metadata = meta(isbn_code)
    meta_keys = "Title Authors Year ISBN-13".split()
    title, authors, year, isbn_13 = map(book_metadata.get, meta_keys)
    meta_cls = BookMetadata(title=title, authors=authors, year=year, isbn_13=isbn_13)
    return meta_cls


@dataclass
class BookMetadata:
    title: str
    authors: list[str]
    year: int
    publisher: str
    isbn_13: str
