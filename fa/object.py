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