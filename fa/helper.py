import requests

def getpost(id, logincookie):
    r = requests.get("http://www.furaffinity.net/view/" + id, cookies=logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()