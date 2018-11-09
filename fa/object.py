import requests
from bs4 import BeautifulSoup

import fa
import fa.helper


class FASubmission(object):
    def __init__(self, data, logincookie, postid=0, title=None, artist=None):
        self._title = title
        self._artist = artist
        self.data = data
        if data:
            self.s = BeautifulSoup(self.data, 'html.parser')
        self.logincookie = logincookie
    
    def __repr__(self):
        return self.title + " by " + self.artist

    @property
    def imglink(self):
        return self.s.find(attrs={'class' : 'alt1 actions aligncenter'}).findAll('b')[1].a.get('href')
    
    @property
    def title(self):
        if self._title: return self._title
        return self.s.findAll(attrs={'class' : 'cat'})[1].b.string

    @property
    def artist(self):
        if self._artist: return self._artist
        return self.s.findAll(attrs={'class' : 'cat'})[1].find('a').string
    
    @property
    def keywords(self):
        keywords = []
        try:
            for kw in self.s.find(attrs={'id' : 'keywords'}).findAll('a'):
                keywords.append(kw.string)
        except:
            keywords.append("Unspecified")
        return keywords

    @property
    def rating(self):
        if "/themes/classic/img/labels/general.gif" in self.data:
            return "General"
        elif "/themes/classic/img/labels/mature.gif" in self.data:
            return "Questionable/Mature"
        elif "/themes/classic/img/labels/adult.gif" in self.data:
            return "Adult"

    def info(self):
        a = self.s.find(attrs={ 'class' : 'alt1 stats-container'}).text.replace(u'\xa0', u' ').strip().split("\n")
        self.postdate = self.s.find(attrs={ 'class' : 'alt1 stats-container'}).find('span').get('title')
        self.category = a[2].strip().replace("Category: ", "")
        self.theme = a[3].strip().replace('Theme: ', '')
        self.species = a[4].strip().replace('Species: ', '')
        self.gender = a[5].strip().replace('Gender: ', '')
        self.favorites = int(a[7])
        self.comments = int(a[8].strip().replace('Comments: ', ''))
        self.views = int(a[9].strip().replace('Views: ', ''))
        self.resolution = a[12].strip().replace('Resolution: ', '')

    def addfav(self):
        url = "https://furaffinity.net" + self.s.find(attrs={'class' : 'alt1 actions aligncenter'}).find('b').a.get('href')
        r = requests.get(url, cookies=self.logincookie)
        if r.status_code == 200:
            pass
        else:
            return r.raise_for_status()

class SearchResults(object):
    def __init__(self, source, logincookie, postdata):
        self.page_source = source
        self.logincookie = logincookie
        self.postdata = postdata
    
    @property
    def posts(self):
        s = BeautifulSoup(self.page_source, "html.parser")
        postlist = []
        for post in s.findAll("figure"):
            r = fa.helper.getpost(post.a.get("href").replace("/view/", ""), self.logincookie)
            if "registered users only" in r:
                pass
            elif "not allowed to view this image due to the content filter" in r:
                pass
            else:
                postlist.append(FASubmission(r, self.logincookie))
        return postlist
    
    def next(self):
        self.postdata['page'] =+ 1
        r = requests.post("http://www.furaffinity.net/search/", data=self.postdata)
        self.page_source = r.text

class FAUser(object):
    def __init__(self, data, logincookie):
        self.data = data
        self.s = BeautifulSoup(self.data, 'html.parser')
        self.logincookie = logincookie
        self.info = self.s.find(attrs={ 'class' : 'ldot' }).text.split("\n")

    def __repr__(self):
        return "User profile of " + self.username

    @property
    def username(self):
        return self.s.title.text.replace("Userpage of ", "").replace(" -- Fur Affinity [dot] net", "")

    @property
    def full_name(self):
        return self.info[1].replace("Full Name: ", "")

    @property
    def title(self):
        return self.info[2].replace("User Title: ", "")

    @property
    def registime(self):
        return self.info[3].replace("Registered since: ", "")

    @property
    def profile(self):
        return r'\n'.join(self.info[6:])

    @property
    def mood(self):
        return self.info[4].replace("Current mood: ", "")

    @property
    def featured_journal(self):
        id = self.s.find(attrs={ 'class': 'no_overflow'}).a.get('href').replace("/journal/", "")
        return Journal(fa.helper.getjournal(id, self.logincookie), self.logincookie)

    @property
    def featured_submission(self):
        id = self.s.find(attrs={'class': 'flow userpage-featured-submission'}).s.a.get('href').replace("/view/", "")
        return FASubmission(fa.helper.getpost(id, self.logincookie), self.logincookie)

    def gallery(self):
        url = "http://www.furaffinity.net/gallery/" + self.username
        b = requests.get(url, cookies=self.logincookie)
        return Gallery(url, b.text, self.logincookie)

    def scraps(self):
        url = "http://www.furaffinity.net/scraps/" + self.username
        b = requests.get(url, self.logincookie)
        return Gallery(url, b.text, self.logincookie)

    def watch(self):
        try:
            watchurl = self.s.find(attrs={'class':"tab"}).findAll("b")[-1].a.get("href")
        except:
            raise fa.exceptions.Forbidden("You're not logged in.")
        url = "http://www.furaffinity.net" + watchurl
        requests.get(url, cookies=self.logincookie)

    def commission(self):
        url = "http://www.furaffinity.net/commissions/" + self.username
        r = BeautifulSoup(requests.get(url, cookies=self.logincookie).text, 'html.parser')
        c = []
        for info in r.find(attrs={'class':"types-table"}).findAll("tr"):
            c.append(Commission(info, self.logincookie))
        return c

    def favorites(self):
        url = "http://www.furaffinity.net/favorites/" + self.username
        b = requests.get(url, cookies=self.logincookie)
        return Favorites(url, b.text, self.logincookie)

class Journal(object):
    def __init__(self, data, logincookie):
        self.data = data
        self.s = BeautifulSoup(self.data, 'html.parser')
        self.logincookie = logincookie

    def __repr__(self):
        return self.title

    @property
    def title(self):
        return self.s.find(attrs={ 'class': 'no_overflow'}).text.strip()

    @property
    def owner(self):
        return fa.FurAffinity().user(self.s.find(attrs={ 'class': 'journal-title-box'}).a.get('href').replace("/user/", ""))

    @property
    def content(self):
        try:
            head = self.s.find(attrs={ 'class': 'journal-header'}).text.strip()
        except:
            head = ''
        try:
            footer = self.s.find(attrs={ 'class': 'journal-footer'}).text.strip()
        except:
            footer = ''
        try:
            body = self.s.find(attrs={ 'class': 'journal-body'}).text.strip()
        except:
            body = ''
        return head + "|" + body + "|" + footer

    @property
    def postdate(self):
        return self.s.find(attrs={ 'class': 'journal-title-box'}).span.get('title')

class Gallery(object):
    def __init__(self, url, source, logincookie):
        self.url = url
        self.page_source = source
        self.logincookie = logincookie

    @property
    def posts(self):
        s = BeautifulSoup(self.page_source, "html.parser")
        postlist = []
        for post in s.findAll("figure"):
            r = fa.helper.getpost(post.a.get("href").replace("/view/", ""), self.logincookie)
            print(r)
            print(post.a.get("href").replace("/view/", ""))
            postlist.append(FASubmission(r, self.logincookie))
        return postlist
    
    def next(self):
        page = int(self.url.split("/")[-1])
        url = self.url + str(page + 1)
        r = requests.get(url)
        self.page_source = r.text

class Commission(object):
    def __init__(self, source, logincookie):
        self.source = BeautifulSoup(source, 'html.parser')
        self.tds = self.source.findAll("td")
        self.logincookie = logincookie

    @property
    def preview(self):
        post = self.source.th.center.b.u.s.a.get("href")
        if "#" not in post:
            return FASubmission(fa.helper.getpost(id, self.logincookie), self.logincookie)
        else:
            return None

    @property
    def price(self):
        return self.tds[0].dl.findAll('dd')[0].text.replace("Price: ", "")

    @property
    def slot(self):
        return self.tds[0].dl.findAll('dd')[1].text.replace("Slots: ", "")

    @property
    def description(self):
        return self.tds[1].text
        
class Favorites(object):
    def __init__(self, url, source, logincookie):
        self.url = url
        self.page_source = source
        self.logincookie = logincookie

    @property
    def posts(self):
        s = BeautifulSoup(self.page_source, "html.parser")
        postlist = []
        for post in s.findAll("figure"):
            r = fa.helper.getpost(post.a.get("href").replace("/view/", ""), self.logincookie)
            print(r)
            print(post.a.get("href").replace("/view/", ""))
            postlist.append(FASubmission(r, self.logincookie))
        return postlist
    
    def next(self):
        s = BeautifulSoup(self.page_source, "html.parser")
        url = "http://www.furaffinity.net" + s.find(attrs={'class':'button-link right'}).get("href")
        r = requests.get(url)
        self.page_source = r.text