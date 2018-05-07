import requests

def getpost(id):
	r = requests.get("http://www.furaffinity.net/view/" + id, cookies=self.logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()