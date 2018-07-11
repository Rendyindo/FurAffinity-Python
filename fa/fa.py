from bs4 import BeautifulSoup
import requests, fa.object, fa.helper, fa.exceptions

class FurAffinity():
    def __init__(self, a="", b="", cfuid=""):
        self.logincookie = { 'b' : b, 'a' : a, '__cfuid' : cfuid}
        if self.username == "Not logged in":
            print("Token may be invalid, will use guest for this session.")
            print("If you think this is a mistake, try to recheck your cookie again!")
    
    def show(self, id):
        r = fa.helper.getpost(id, self.logincookie)
        if "registered users only" in r:
            raise fa.exceptions.Forbidden("You need to login to view this user!")
        if "not allowed to view this image due to the content filter" in r:
            raise fa.exceptions.Forbidden("You need to apply your current content filter settings!")
        return fa.object.FASubmission(r, self.logincookie)

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
        for post in s.findAll("figure")[:limit]:
            r = fa.helper.getpost(post.a.get("href").replace("/view/", ""), self.logincookie)
            postlist.append(fa.object.FASubmission(r, self.logincookie))
        return postlist

    def search(self, *query, page=1, sort="relevancy", order="desc"):
        validsorts = ['relevancy', 'date', 'popularity']
        if sort not in validsorts:
            raise fa.exceptions.InvalidParameter("Invalid sort type: " + sort)
        if order not in ['asc', 'desc']:
            raise fa.exceptions.InvalidParameter("Invalid order: " + order)
        if page < 0 or page == 0:
            raise fa.exceptions.InvalidParameter("Invalid page number: " + page)
        postdata = {'q': '+'.join(query), 'perpage': '24', 'order-by': sort, 'order-direction': order, \
                    'do_search': 'Search', 'range': 'all', 'rating-general': 'on', 'type-art': 'on', \
                    'type-flash': 'on', 'type-photo': 'on', 'type-music': 'on', 'type-story': 'on', \
                    'type-poetry': 'on', 'mode': 'extended', 'page': page}
        r = requests.post("http://www.furaffinity.net/search/", data=postdata)
        return fa.object.SearchResults(r.text, self.logincookie, postdata)

    def user(self, name):
        if "_" in name:
            name = name.replace("_", "")
        r = fa.helper.getuser(name, self.logincookie)
        if "This user cannot be found." in r:
            raise fa.exceptions.UserNotFound("User cannot be found!")
        if "registered users only" in r:
            raise fa.exceptions.Forbidden("You need to login to view this user!")
        return fa.object.FAUser(r, self.logincookie)