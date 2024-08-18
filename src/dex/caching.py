from pydantic import (
    BaseModel,
    DirectoryPath,
    FilePath,
    NewPath,
    computed_field,
    model_validator,
)
from pydantic_extra_types.isbn import ISBN

from .path_utils import pkg_cache_dir


class ISBNCache(BaseModel):
    isbn_code: ISBN
    parent_dir: DirectoryPath | NewPath = pkg_cache_dir

    @computed_field
    @property
    def json_path(self) -> FilePath | NewPath:
        return (self.parent_dir / self.isbn_code).with_suffix(".json")

    @model_validator(mode="after")
    def ensure_dir(self) -> None:
        self.parent_dir.mkdir(parents=True, exist_ok=True)
        return
