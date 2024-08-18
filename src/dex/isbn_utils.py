from __future__ import annotations

from isbnlib import meta
from pydantic import BaseModel, Field, RootModel, TypeAdapter
from pydantic_extra_types.isbn import ISBN

from .caching import ISBNCache

__all__ = ["isbn_ta", "AuthorName", "BookMetadata", "get_isbn_metadata"]


isbn_ta = TypeAdapter(ISBN)


class AuthorName(RootModel):
    root: str

    @property
    def surname(self) -> str:
        return self.root.split(" ")[-1]


class BookMetadata(BaseModel):
    """Model of the keys from the :class:`isbnlib.Isbn` dict type."""

    title: str = Field(alias="Title")
    authors: list[AuthorName] = Field(alias="Authors")
    year: int = Field(alias="Year")
    publisher: str = Field(alias="Publisher")
    isbn_13: ISBN = Field(alias="ISBN-13")

    @property
    def first_author(self) -> AuthorName:
        return self.authors[0]

    def __repr__(self) -> str:
        return (
            f"'\N{OPEN BOOK}: {self.first_author.surname} ({self.year}) {self.title}'"
        )


def get_isbn_metadata(isbn_code: str, use_cache=True) -> BookMetadata:
    """If cache unavailable, downloads over the network using `isbnlib`."""
    if use_cache:
        # Touch the cache directory for this ISBN
        meta_cache = ISBNCache(isbn_code=isbn_code)
        if (cache_path := meta_cache.json_path).exists():
            # Access cache JSON
            meta_model = BookMetadata.model_validate_json(cache_path.read_text())
        else:
            # Access network
            isbn_metadata = meta(isbn_code)
            meta_model = BookMetadata.model_validate(isbn_metadata)
            # Write to cache so next time doesn't use the network
            json_text = meta_model.model_dump_json(by_alias=True)
            cache_path.write_text(json_text)
    else:
        isbn_metadata = meta(isbn_code)
        meta_model = BookMetadata.model_validate(isbn_metadata)
    return meta_model
