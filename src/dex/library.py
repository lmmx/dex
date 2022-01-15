from __future__ import annotations

from .log_utils import Console
from .path_utils import shelves_path

__all__ = ["load_library"]

logger = Console(name=__name__).logger


def load_library() -> None:
    pattern = "dex*.zip"
    zipfiles = [*shelves_path.glob(pattern)]
    if zipfiles:
        logger.info(f"Library contains {len(zipfiles)} files")
    else:
        logger.info("Nothing to do")
    return
