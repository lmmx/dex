from __future__ import annotations

from dataclasses import dataclass, field

from dataclass_wizard import JSONWizard

# from typing import Any


__all__ = ["DocTreeDoc", "Page", "Block", "Line", "Word"]


@dataclass
class DocTreeDoc(JSONWizard):
    pages: list[Page] = field(default_factory=list)

    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_dump = "SNAKE"


@dataclass
class Page:
    page_idx: int
    dimensions: tuple[int, int]
    # orientation: dict[str, Any]
    # language: dict[str, Any]
    blocks: list[Block]


@dataclass
class Block:
    # geometry: tuple[tuple[float, float], tuple[float, float]]
    lines: list[Line]


@dataclass
class Line:
    # geometry: tuple[tuple[float, float], tuple[float, float]]
    words: list[Word]


@dataclass
class Word:
    value: str
    confidence: float
    # geometry: tuple[tuple[float, float], tuple[float, float]]
