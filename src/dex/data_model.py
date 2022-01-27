from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from typing import Iterator

import ujson
from dataclass_wizard import JSONWizard

from .heuristics import likely_page_number

# from typing import Any


__all__ = ["DocTreeDoc", "Page", "Block", "Line", "Word"]


@dataclass
class DocTreeDoc(JSONWizard):
    pages: list[Page] = field(default_factory=list)

    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_dump = "SNAKE"

    def dump_json(self):
        return ujson.dumps({"pages": [p.serialise() for p in self.pages]})


@dataclass
class Page:
    page_idx: int
    dimensions: tuple[int, int]
    # orientation: dict[str, Any]
    # language: dict[str, Any]
    blocks: list[Block]
    page_no_estim: list[int] = field(default_factory=list)

    @property
    def page_no(self):
        """Not yet implemented: detect page number."""
        return None

    def serialise(self):
        return {
            "page_idx": self.page_idx,
            "page_no": self.page_no,
            "words": self.all_words(),
        }

    @property
    def sorted_block_order(self) -> Iterator[int]:
        """The permutation that gives the sorted blocks"""
        # May not include all elements: exclude non-entry blocks
        # e.g. page number
        n_blocks = len(self.blocks)
        sort_order = (i for i in range(n_blocks))
        return sort_order

    def sorted_blocks(self) -> Iterator[Block]:
        """
        Not yet fully implemented: detect block order.

        :meth:`is_marginalia` will append to the :attr:`page_no_estim` list but will not
        make a decision unless certain. Once all blocks have been passed over by this
        method, the list will be fully populated and can then be checked again (if it
        has a single value, it can be used, if multiple, the previous pages' page
        numbers can be used to narrow the guess).
        """
        non_marginalia_idx = [
            idx
            for idx in self.sorted_block_order
            if not self.is_marginalia(block_idx=idx)
        ]
        # Handle `page_no_estim` here...
        return (self.blocks[idx] for idx in non_marginalia_idx)

    def all_words(self) -> list[str]:
        return list(chain.from_iterable(b.iter_words() for b in self.sorted_blocks()))

    def is_marginalia(self, block_idx: int) -> bool:
        """If a block has just 1 line, check its words (e.g. may say 'Index')."""
        block = self.blocks[block_idx]
        lines = block.lines
        if len(lines) == 1:
            decision = self.detect_marginalia(block_idx=block_idx, words=lines[0].words)
        else:
            decision = False
        return decision

    def detect_marginalia(self, block_idx: int, words: list[Word]) -> bool:
        decision = False
        if len(words) == 1:
            if words[0].value == "Index":
                decision = True
            else:
                num = likely_page_number(words[0].value)
                if num is not None:
                    self.page_no_estim.append((block_idx, num))
                    # How to handle multiple choice? Lookbehind at prev page for clue?
                # Should this if be elif? No decision taken on num yet but...
                if self.is_cornermost_block(self):
                    decision = True
        return decision


@dataclass
class Block:
    # geometry: tuple[tuple[float, float], tuple[float, float]]
    lines: list[Line]

    def iter_words(self) -> Iterator[str]:
        """
        Should be rewritten to use yield.
        Should be rewritten to attempt to group words and use a :class:`LineEntry`
        object to structure the page number.
        """
        # TODO: handle the value: currently it is trivially passed through
        return (LineEntry.estimate_from_line(line).serialise() for line in self.lines)


@dataclass
class Line:
    geometry: tuple[tuple[float, float], tuple[float, float]]
    words: list[Word]


class RomanNumeral:
    pass  # Need to implement for lower cases


# To be used in the `Block.iter_words` method to roll up lines into entries.
@dataclass
class LineEntry:
    title: str
    page_numbers: list[RomanNumeral | int]

    @classmethod
    def estimate_from_line(cls, line: Line) -> LineEntry:
        """
        Very naively checks for numeric characters to identify a page number.
        Does not yet handle Roman numerals.
        """
        estimated_title_parts = []
        estimated_entry_numbers = []
        for w in line.words:
            if (num := likely_page_number(w)) is not None:
                estimated_entry_numbers.append(num)
            else:
                estimated_title_parts.append(w)
        title = " ".join(estimated_title_parts)
        return cls(title=title, page_numbers=estimated_entry_numbers)

    def serialise(self):
        return {self.title: self.page_numbers}


@dataclass
class Word:
    value: str
    # confidence: float
    geometry: tuple[tuple[float, float], tuple[float, float]]
