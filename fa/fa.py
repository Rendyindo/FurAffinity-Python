from bs4 import BeautifulSoup
import requests, object, helper

class FurAffinity():
    def __init__(self, a="", b="", cfuid=""):
        self.logincookie = { 'b' : b, 'a' : a, '__cfuid' : cfuid}
        if self.username == "Not logged in":
            print("Token may be invalid, will use guest for this session.")
            print("If you think this is a mistake, try to recheck your cookie again!")
    
    def show(self, id):
        r = helper.getpost(id, self.logincookie)
        return object.FASubmission(r, self.logincookie)

    @property
    def username(self):
        r = requests.get("http://www.furaffinity.net/", cookies=self.logincookie)
        if r.status_code == 200:
            pass
        else:
            return r.raise_for_status()
        s = BeautifulSoup(r.text, "html.parser")
        try:
            user = s.find(attrs={'id' : 'my-username'}).text.replace('~', '')
        except:
            user = "Not logged in"
        return user

    def recent(self, limit=48):
        r = requests.get("http://www.furaffinity.net/browse", cookies=self.logincookie)
        if r.status_code == 200:
            pass
        else:
            return r.raise_for_status()
        s = BeautifulSoup(r.text, "html.parser")
        postlist = []
        print(len(s.findAll("figure")))
        for post in s.findAll("figure")[:limit]:
            r = helper.getpost(post.a.get("href").replace("/view/", ""), self.logincookie)
            postlist.append(object.FASubmission(r, self.logincookie))
        return postlist



    