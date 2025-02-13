from pathlib import Path

from dex import load_library
from fieldrouter import Routing, RoutingModel

library = load_library(n=1)
assert len(library.items) == 1, f"Library is {library}"

for idx, book in enumerate(library.items):
    print(f"{idx+1}. {book}")


class IndexedBook(RoutingModel):
    book: Routing(dict, ".")
    meta: Routing(dict, ".book.metadata")
    shelf: Routing(dict, ".book.shelf")
    shelftop: Routing(Path, ".shelf.top")
    ocr: Routing(Path, ".shelf.surya_ocr_results")


indexed = IndexedBook.model_validate(book.model_dump())
