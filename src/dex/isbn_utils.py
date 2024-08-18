from __future__ import annotations

from isbnlib import meta
from pydantic import BaseModel, Field, RootModel, TypeAdapter
from pydantic_extra_types.isbn import ISBN

__all__ = ["isbn_ta", "AuthorName", "BookMetadata", "get_isbn_metadata"]


isbn_ta = TypeAdapter(ISBN)


class AuthorName(RootModel):
    root: str

    @property
    def surname(self) -> str:
        return self.root.split(" ")[-1]


class BookMetadata(BaseModel):
    """Model of the keys from the :class:`isbnlib.Isbn` dict type."""

    title: str = Field(validation_alias="Title")
    authors: list[AuthorName] = Field(validation_alias="Authors")
    year: int = Field(validation_alias="Year")
    publisher: str = Field(validation_alias="Publisher")
    isbn_13: ISBN = Field(validation_alias="ISBN-13")

    @property
    def first_author(self) -> AuthorName:
        return self.authors[0]

    def __repr__(self) -> str:
        return (
            f"'\N{OPEN BOOK}: {self.first_author.surname} ({self.year}) {self.title}'"
        )


def get_isbn_metadata(isbn_code: str) -> BookMetadata:
    isbn_metadata = meta(isbn_code)  # Downloads over the network!
    return BookMetadata.model_validate(isbn_metadata)
