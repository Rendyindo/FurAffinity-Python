import requests, time

def RateLimit(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimit(2)
def getpost(id, logincookie):
    r = requests.get("http://www.furaffinity.net/view/" + id, cookies=logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()

@RateLimit(2)
def getuser(id, logincookie):
    r = requests.get("http://www.furaffinity.net/user/" + id, cookies=logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()

@RateLimit(2)
def getjournal(id, logincookie):
    r = requests.get("http://www.furaffinity.net/journal/" + id, cookies=logincookie)
    if r.status_code == 200:
        return r.text
    else:
        return r.raise_for_status()
