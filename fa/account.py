from fa.exceptions import Forbidden, NotLoggedIn
from bs4 import BeautifulSoup
import requests
import time
from tkinter import *
import os

logincookie = None
username = None

def login(a="", b="", cfuid=""):
    global logincookie
    global username
    temp_cookie = { 'b' : b, 'a' : a, '__cfuid' : cfuid}
    r = requests.get("http://www.furaffinity.net/", cookies=temp_cookie)
    if r.status_code == 200:
        pass
    else:
        r.raise_for_status()
    s = BeautifulSoup(r.text, "html.parser")
    try:
        username = s.find(attrs={'id' : 'my-username'}).text.replace('~', '')
    except:
        raise NotLoggedIn("Invalid cookie.")
    logincookie = temp_cookie

def login_password(username, password):
    from PIL import Image, ImageTk
    
    s = requests.session()

    def download_file(url):
        local_filename = "captcha.jpg"
        with s.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)

    cookie = {
        "action":"login",
        "name":username,
        "pass":password,
        "g-recaptcha-response":"",
        "use_old_captcha":1,
        "captcha":None,
        "login":"Login+to%C2%A0FurAffinity"
    }
    s.get("https://www.furaffinity.net/login/") # Just to get a and __cfduid cookie :3c
    download_file("https://www.furaffinity.net/captcha.jpg?random=" + str(int(time.time())))

    class CaptchaFrame(Frame):
        def __init__(self, root):
            self.root = root
            super().__init__(root)

            self.image = ImageTk.PhotoImage(Image.open("captcha.jpg"))
            self.imgpanel = Label(root, image=self.image).grid(row=0)
            Label(root, text="Captcha").grid(row=1)
            self.entry = Entry(root)
            self.entry.grid(row=1, column=1)
            #self.contents = StringVar()
            #self.entry["textvariable"] = self.contents
            Button(root, text='Submit', command=self.post).grid(row=3, column=0, sticky=W, pady=4)

        def post(self):
            cookie['captcha'] = self.entry.get()
            ra = s.post("https://www.furaffinity.net/login/", data=cookie)
            self.root.destroy()
            os.remove("captcha.jpg")
            if "erroneous" in ra.text:
                raise Exception("Wrong captcha or password")

    root = Tk()
    lf = CaptchaFrame(root)
    root.title("Captcha")
    root.mainloop()
    cookies = requests.utils.dict_from_cookiejar(s.cookies)
    return cookies if len(cookies) != 2 else None