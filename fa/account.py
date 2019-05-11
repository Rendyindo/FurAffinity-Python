from fa.exceptions import Forbidden, NotLoggedIn
from bs4 import BeautifulSoup
import requests

logincookie = None
username = None

def login(a="", b="", cfuid=""):
    global logincookie
    global username
    temp_cookie = { 'b' : b, 'a' : a, '__cfuid' : cfuid}
    r = requests.get("http://www.furaffinity.net/", cookies=temp_cookie)
    if r.status_code == 200:
        pass
    else:
        r.raise_for_status()
    s = BeautifulSoup(r.text, "html.parser")
    try:
        username = s.find(attrs={'id' : 'my-username'}).text.replace('~', '')
    except:
        raise NotLoggedIn("Invalid cookie.")
    logincookie = temp_cookie

