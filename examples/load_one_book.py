from dex import load_library

library = load_library(n=1)
assert len(library.items) == 1, f"Library is {library}"

for idx, book in enumerate(library.items):
    print(f"{idx+1}. {book}")
