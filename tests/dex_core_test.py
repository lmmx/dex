from pysnooper import snoop
from pytest import importorskip


@snoop(depth=10)
def test_library_load():
    importorskip("examples.load_entire_library")
