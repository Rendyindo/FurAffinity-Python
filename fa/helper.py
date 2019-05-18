import requests, time
from fa import account

def RateLimit(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.perf_counter() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimit(4)
def getpost(id):
    r = requests.get("http://www.furaffinity.net/view/" + id, cookies=account.logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()

@RateLimit(4)
def getuser(id):
    r = requests.get("http://www.furaffinity.net/user/" + id, cookies=account.logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()

@RateLimit(4)
def getjournal(id):
    r = requests.get("http://www.furaffinity.net/journal/" + id, cookies=account.logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()
