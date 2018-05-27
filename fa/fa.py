from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests, fa.object, fa.helper, fa.exceptions

class FurAffinity():
    def __init__(self, a="", b="", cfuid=""):
        self.logincookie = { 'b' : b, 'a' : a, '__cfuid' : cfuid}
        if self.username == "Not logged in":
            print("Token may be invalid, will use guest for this session.")
            print("If you think this is a mistake, try to recheck your cookie again!")
    
    def show(self, id):
        r = fa.helper.getpost(id, self.logincookie)
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

    def search(self, *query, page=1, sort="relevancy", order="descending"):
        
        validsorts = ['relevancy', 'date', 'popularity']
        if sort not in validsorts:
            raise fa.exceptions.InvalidParameter("Invalid sort type: " + sort)
        if order not in ['ascending', 'descending']:
            raise fa.exceptions.InvalidParameter("Invalid order: " + order)
        if page > 1 or sort is not "relevancy" or order is not "descending":
            resubmitdata = True
        else:
            resubmitdata = False
        if page < 0 or page == 0:
            print("Dude no")
            raise fa.exceptions.InvalidParameter("Invalid page number: " + page)
        b = webdriver.Chrome()
        b.get("http://www.furaffinity.net/search/?q=" + '%20'.join(query))
        browsercookie = fa.helper.split_dict_equally(self.logincookie)
        for semicookie in browsercookie:
            for a,c in semicookie.items():
                cookie = { 'name': a, 'value': c }
                b.add_cookie(cookie)
        if resubmitdata:
            pageelem = b.find_element_by_xpath("""//*[@id="page"]""")
            pageelem.send_keys(page)
            sortelem = Select(b.find_element_by_xpath("""//*[@id="search-form"]/fieldset/select[2]"""))
            sortelem.select_by_visible_text(sort)
            orderelem = Select(b.find_element_by_xpath("""//*[@id="search-form"]/fieldset/select[3]"""))
            orderelem.select_by_visible_text(order)
            b.find_elements_by_xpath("""//*[@id="search-form"]/fieldset/input[3]""").click()
        return fa.object.SearchResults(b, b.page_source, self.logincookie)

    def user(self, name):
        if "_" in name:
            name = name.replace("_", "")
        r = fa.helper.getuser(name, self.logincookie)
        if "This user cannot be found." in r:
            raise fa.exceptions.UserNotFound("User cannot be found!")
        if "registered users only" in r:
            raise fa.exceptions.Forbidden("You need to login to view this user!")
        return fa.object.FAUser(r, self.logincookie)