from __future__ import annotations

from os import environ
from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError

from . import __path__

__all__ = ["get_shelves_path"]

pkg_path = Path(*__path__)


def get_shelves_path() -> Path:
    """
    If the package is installed from the git repo, we can
    """
    env_var = "DEX_SHELVES"
    grandparent_dir = pkg_path.parent.parent

    if grandparent_dir.exists():
        try:
            Repo(grandparent_dir)
        except InvalidGitRepositoryError:
            is_git_repo = False
        else:
            is_git_repo = True
            shelves_path = grandparent_dir / "data" / "shelves"
    if not is_git_repo:
        if env_var in environ:
            shelves_path = Path(environ[env_var])
            if not shelves_path.exists():
                err_msg = f"{shelves_path=} set from {env_var=} does not exist"
                raise FileNotFoundError(err_msg)
        else:
            err_msg = (
                "Package data directory handling in distributed package not set up. "
                f"Please set a storage path as the '{env_var}' environment variable."
            )
            raise NotImplementedError(err_msg)
    return shelves_path
