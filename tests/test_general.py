from fa import FurAffinity
from fa.objects import *
from cfg import logincookie
import pytest

@pytest.fixture
def fa():
    return FurAffinity(**logincookie)

@pytest.mark.general
def test_guest():
    assert FurAffinity().my_user == None

@pytest.mark.general
def test_login():
    assert FurAffinity(**logincookie).my_user.username == "Error-", "Failed to log in!"

@pytest.mark.general
def test_getpost(fa):
    assert type(fa.show(str(6847764))) == FASubmission, "Failed to get post!"

@pytest.mark.general
def test_recents(fa):
    assert fa.recent()

@pytest.mark.general
def test_search(fa):
    assert fa.search("gay")

@pytest.mark.general
def test_getuser(fa):
    assert fa.user("slyus").username == "slyus"
