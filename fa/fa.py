from bs4 import BeautifulSoup
import requests, object, helper

class FurAffinity():
    def __init__(self, a, b, cfuid):
        self.logincookie = { 'b' : b, 'a' : a, '__cfuid' : cfuid}
        if self.username == "Not logged in":
            print("Token may be invalid, will use guest for this session.")
            print("If you think this is a mistake, try to recheck your cookie again!")
    
    def show(self, id):
        r = helper.getpost(id)
        return object.FASubmission(r.text, self.logincookie)

    @property
    def username(self):
        r = requests.get("http://www.furaffinity.net/", cookies=self.logincookie)
        if r.status_code == 200:
            pass
        else:
            return r.raise_for_status()
        s = BeautifulSoup(r.text, "html.parser")
        if not s.find(attrs={'id' : 'my-username'}).text.replace('~', ''):
            return "Not logged in"
        return s.find(attrs={'id' : 'my-username'}).text.replace('~', '')



    