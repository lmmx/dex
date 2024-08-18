from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from pydantic import (
    FilePath,
    RootModel,
    field_validator,
)


__all__ = ["Image", "Photo", "Dewarped"]


class Image(RootModel):
    """An existing file path with PNG/JPG suffix."""

    suffixes: ClassVar[str] = [".png", ".jpg", ".jpeg"]

    root: FilePath

    @field_validator("root", mode="after")
    @classmethod
    def is_image(cls, v: FilePath) -> FilePath:
        if v.suffix not in cls.suffixes:
            raise ValueError(f"File suffix {v.suffix} is not in {cls.suffixes}")
        return v


class Photo(Image):
    """A source photograph of a book page."""

    @property
    def _dewarped_path(self) -> Path:
        return self.root.parent / "dewarped" / self.root.name

    @property
    def has_been_dewarped(self) -> bool:
        return self._dewarped_path.exists()


class Dewarped(Image):
    """A dewarped photograph of a book page."""

    @property
    def _original_photo(self) -> Path:
        return self.root.parent / self.root.name

    @property
    def has_original_photo(self) -> bool:
        return self._original_photo.exists()
