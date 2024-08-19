# from pysnooper import snoop
from pytest import importorskip


# @snoop(depth=10)
def test_library_load():
    importorskip("examples.load_entire_library")


def test_book_load():
    importorskip("examples.load_one_book")
