from dex import load_library

library = load_library()
assert len(library.items) == 6, f"Library is {library}"

for idx, book in enumerate(library.sorted_items):
    print(f"{idx+1}. {book}")
