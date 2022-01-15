from __future__ import annotations

from pathlib import Path

from . import __path__

__all__ = ["load_library"]

pkg_path = Path(*__path__)

LIBRARY_PATH = pkg_path.parent.parent / "data" / "shelves"

def load_library() -> None:
    if not LIBRARY_PATH.exists():
        err_msg = "Package daa directory handling in distributed package not yet set up"
        raise NotImplementedError(err_msg)
    return
