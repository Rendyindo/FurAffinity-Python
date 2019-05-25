import fa.exceptions
import requests
from bs4 import BeautifulSoup
from fa import account as my_account
import fa.helper
from fa.objects import FASubmission, SearchResults, FAUser, Account

class FurAffinity():
    def __init__(self, a="", b="", cfuid=""):
        try:
            my_account.login(a, b, cfuid)
        except:
            print("Token may be invalid, will use guest for this session.")
            print("If you think this is a mistake, try to recheck your cookie again!")
    
    def show(self, id):
        id = str(id)
        r = fa.helper.getpost(id)
        if "registered users only" in r:
            raise fa.exceptions.Forbidden("You need to login to view this user!")
        if "not allowed to view this image due to the content filter" in r:
            raise fa.exceptions.Forbidden("You need to apply your current content filter settings!")
        if "The submission you are trying to find is not in our database" in r:
            raise fa.exceptions.NotFound("Submission cannot be found!")
        return FASubmission(r)

    @property
    def my_user(self):
        try:
            r = fa.helper.getuser(my_account.username)
            return Account(r)
        except:
            return None

    def recent(self, limit=48):
        r = requests.get("http://www.furaffinity.net/browse", cookies=my_account.logincookie)
        if r.status_code == 200:
            pass
        else:
            return r.raise_for_status()
        s = BeautifulSoup(r.text, "html.parser")
        postlist = []
        for post in s.findAll("figure")[:limit]:
            r = fa.helper.getpost(post.a.get("href").replace("/view/", ""))
            postlist.append(FASubmission(r))
        return postlist

    def search(self, *query, page=1, sort="relevancy", order="desc"):
        validsorts = ['relevancy', 'date', 'popularity']
        if sort not in validsorts:
            raise fa.exceptions.InvalidParameter("Invalid sort type: " + sort)
        if order not in ['asc', 'desc']:
            raise fa.exceptions.InvalidParameter("Invalid order: " + order)
        if page < 0 or page == 0:
            raise fa.exceptions.InvalidParameter("Invalid page number: " + page)
        postdata = {'q': '+'.join(query), 'perpage': '48', 'order-by': sort, 'order-direction': order, \
                    'do_search': 'Search', 'range': 'all', 'rating-general': 'on', 'type-art': 'on', \
                    'type-flash': 'on', 'type-photo': 'on', 'type-music': 'on', 'type-story': 'on', \
                    'type-poetry': 'on', 'mode': 'extended', 'page': page}
        r = requests.post("http://www.furaffinity.net/search/", data=postdata, cookies=my_account.logincookie)
        return SearchResults(r.text, postdata)

    def user(self, name):
        if "_" in name:
            name = name.replace("_", "")
        r = fa.helper.getuser(name)
        if "This user cannot be found." in r:
            raise fa.exceptions.NotFound("User cannot be found!")
        if "registered users only" in r:
            raise fa.exceptions.Forbidden("You need to login to view this user!")
        return FAUser(r)