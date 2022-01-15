from __future__ import annotations

from .path_utils import get_shelves_path

__all__ = ["load_library"]


def load_library() -> None:
    library_path = get_shelves_path()
    assert library_path.exists(), "Internal error in library path resolution"
    return
