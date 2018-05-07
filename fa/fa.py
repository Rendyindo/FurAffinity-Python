from bs4 import BeautifulSoup
import requests, object, helper

class FurAffinity():
    def __init__(self, a, b, cfuid):
        self.logincookie = { 'b' : b, 'a' : a, '__cfuid' : cfuid}
    
    def show(self, id):
        r = helper.getpost(id)
        return object.FASubmission(r.text, self.logincookie)

    def username(self):
        r = requests.get("http://www.furaffinity.net/", cookies=self.logincookie)
        if r.status_code == 200:
            pass
        else:
            return r.raise_for_status()
        s = BeautifulSoup(r.text, "html.parser")
        return s.find(attrs={'id' : 'my-username'}).text.replace('~', '')



    