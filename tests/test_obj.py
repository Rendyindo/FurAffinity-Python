from fa import FurAffinity
from fa.objects import *
from cfg import logincookie
import pytest
import types
import pickle

def objcheck(obj, expectation):
    result = list()
    for prop in [ a for a in dir(obj) if not a.startswith("_") ]:
        attr = getattr(obj, prop)
        if not hasattr(attr, "__call__"):
            result.append(attr)
    return result == expectation
    
@pytest.fixture
def fa():
    return FurAffinity(**logincookie)

@pytest.mark.post
def test_postcheck(fa):
    p = fa.show("5128889")
    with open("tests\post.dat", "rb") as f:
        post_expected = pickle.load(f)
    objcheck(p, post_expected)
    