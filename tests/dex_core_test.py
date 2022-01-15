from pytest import fixture, mark

from dex import load_library

def test_library_load():
    load_library()
