from __future__ import annotations

__all__ = ["likely_page_number"]

def likely_page_number(value: str) -> int | None:
    """
    Guess if a word value is likely to be a page number by checking for numeric values,
    ensuring they are proper [consecutive character] substrings, and returning the
    integer.
    """
    alphanum_chars = "".join(c for c in value if c.isalnum())
    if alphanum_chars in value and alphanum_chars.isnumeric():
        guess = int(alphanum_chars)
    else:
        guess = None
    return guess
