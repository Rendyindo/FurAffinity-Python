from bs4 import BeautifulSoup
import requests, helper
class FASubmission(object):
    def __init__(self, data, logincookie):
        self.data = data
        self.s = BeautifulSoup(self.data, 'html.parser')
        self.logincookie = logincookie
    
    def __repr__(self):
        return self.title + " by " + self.artist

    @property
    def imglink(self):
        return self.s.find(attrs={'class' : 'alt1 actions aligncenter'}).findAll('b')[1].a.get('href')
    
    @property
    def title(self):
        return self.s.find(attrs={'class' : 'cat'}).string.strip()

    @property
    def artist(self):
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
    def rating(self, id):
        r = helper.getpost(id, self.logincookie)
        if "/themes/classic/img/labels/general.gif" in r:
            return "General"
        elif "/themes/classic/img/labels/mature.gif" in r:
            return "Questionable/Mature"
        elif "/themes/classic/img/labels/adult.gif" in r:
            return "Adult"

    def info(self):
        a = self.s.find(attrs={ 'class' : 'alt1 stats-container'}).text.replace(u'\xa0', u' ').strip().split("\n")
        self.postdate = self.s.find(attrs={ 'class' : 'alt1 stats-container'}).find('span').get('title')
        self.category = a[2].strip().replace("Category: ", "")
        self.theme = a[3].strip().replace('Theme: ', '')
        self.species = a[4].strip().replace('Species: ', '')
        self.gender = a[4].strip().replace('Gender: ', '')
        self.favorites = int(a[6])
        self.comments = int(a[7].strip().replace('Comments: ', ''))
        self.views = int(a[8].strip().replace('Views: ', ''))
        self.reso = a[12].strip().replace('Resolution: ', '')

    def addfav(self):
        url = "https://furaffinity.net" + self.s.find(attrs={'class' : 'alt1 actions aligncenter'}).find('b').a.get('href')
        r = requests.get(url, cookies=self.logincookie)
        if r.status_code == 200:
            pass
        else:
            return r.raise_for_status()

class SearchResults(object):
    def __init__(self, browser, source, logincookie):
        self.browser = browser
        self.page_source = source
        self.logincookie = logincookie
    
    @property
    def posts(self):
        s = BeautifulSoup(self.page_source, "html.parser")
        postlist = []
        for post in s.findAll("figure"):
            r = helper.getpost(post.a.get("href").replace("/view/", ""), self.logincookie)
            print(r)
            print(post.a.get("href").replace("/view/", ""))
            postlist.append(FASubmission(r, self.logincookie))
        return postlist
    
    def next(self):
        btn = self.browser.find_elements_by_name("next_page")[0]
        btn.click()
        return SearchResults(self.browser, self.browser.page_source, self.logincookie)
    
    def close(self):
        self.browser.close()
        pass

class FAUser(object):
    def __init__(self, data, logincookie):
        self.data = data
        self.s = BeautifulSoup(self.data, 'html.parser')
        self.logincookie = logincookie
        self.info = self.s.find(attrs={ 'class' : 'ldot' }).text.split("\n")

    def __repr__(self):
        return "User profile of"

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
