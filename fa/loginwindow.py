from tkinter import *
from PIL import Image, ImageTk
import requests, time, os

def loginw(username, password):
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
    image = None
    def get_capctha():
        download_file("https://www.furaffinity.net/captcha.jpg?random=" + str(int(time.time())))
        image = ImageTk.PhotoImage(Image.open("captcha.jpg"))

    class CaptchaFrame(Frame):
        def __init__(self, root):
            self.root = root
            super().__init__(root)

            get_capctha()
            self.imgpanel = Label(root, image=image)
            self.imgpanel.grid(row=0)

            Label(root, text="Captcha").grid(row=1)

            self.entry = Entry(root)
            self.entry.grid(row=1, column=1)

            Button(root, text='Submit', command=self.post).grid(row=3, column=0, sticky=W, pady=4)
            Button(root, text='Refresh Captcha', command=self.post).grid(row=3, column=0, sticky=W, pady=4)

        def refresh(self):
            get_capctha()
            self.imgpanel.configure(image=image)
            self.imgpanel.image = image
        
        def post(self):
            cookie['captcha'] = self.entry.get()
            ra = s.post("https://www.furaffinity.net/login/", data=cookie)
            self.root.destroy()
            os.remove("captcha.jpg")
            if "erroneous" in ra.text:
                raise Exception("Wrong captcha or password")

    root = Tk()
    CaptchaFrame(root)
    root.title("Captcha")
    root.mainloop()
    cookies = requests.utils.dict_from_cookiejar(s.cookies)
    return cookies if len(cookies) != 2 else None