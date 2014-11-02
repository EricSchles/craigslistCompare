import requests
import lxml.html
import pickle
import grequests
import pandas as pd
import time
import os
class Scraper:
    def __init__(self):
        pass

    def setup(self,num_pages=2):
        craigslists= ["http://newyork.craigslist.org/","http://cnj.craigslist.org/","http://jerseyshore.craigslist.org/","http://newjersey.craigslist.org/","http://southjersey.craigslist.org/"]
        casual_encounters = []
        ads = []
        for site in craigslists:
            base = site
            site = site+"search/w4m"
            urls = []
            for i in xrange(num_pages):
                if i == 0:
                    urls.append(site)
                else:
                    urls.append(site+"?s="+str(i)+"00&")
            rs = (grequests.get(u) for u in urls)
            responses = grequests.map(rs)
            for r in responses:
                html = lxml.html.fromstring(r.text)
                links = html.xpath("//a/@href")
                for link in links:
                    if "search" in link:
                        continue
                    if "http" in  link:
                        continue
                    if "w4m" in link:
                        link = "http://"+r.url.split("/")[-3]+link
                        if not link in ads:
                            ads.append(link)
        return ads
    
    #found here: http://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
    def is_ascii(self,s):
        return all(ord(c) < 128 for c in s)

    def parse(self,r):
        values = {}
        text = r.text.encode("ascii","ignore")
        if not self.is_ascii(text):
            print r.url
        html = lxml.html.fromstring(text)
        values["title"] = [i.text_content() for i in html.xpath('//h2[@class="postingtitle"]')]
        values["body"] = [i.text_content() for i in html.xpath('//section[@id="postingbody"]')][0] 
        values["phone_number"] = self.phone_number_grab(values["body"])
        return values

    def save(self,r):
        name = "_".join(r.url.split("/")[-2:])
        text = r.text.encode("ascii","ignore")
        with open(name,"w") as f:
            f.write(text)

    def letter_to_number(self,text):
        text= text.upper()
        text = text.replace("ONE","1")
        text = text.replace("TWO","2")
        text = text.replace("THREE","3")
        text = text.replace("FOUR","4")
        text = text.replace("FIVE","5")
        text = text.replace("SIX","6")
        text = text.replace("SEVEN","7")
        text = text.replace("EIGHT","8")
        text = text.replace("NINE","9")
        text = text.replace("ZERO","0")
        return text
        
    def phone_number_grab(self,text):
        if text == '':
            return ''
        text = self.letter_to_number(text)
        phone = []
        counter = 0
        found = False
        for ind,letter in enumerate(text):
            if letter.isdigit():
                phone.append(letter)
                found = True
            else:
                if found:
                    counter += 1
                if counter > 8 and found:
                    phone = []
                    counter = 0
                    found = False

            if len(phone) == 10:
                return ''.join(phone)

        return ''

    def run(self):
        ads = self.setup()
        df = pd.DataFrame()
        rs = (grequests.get(u) for u in ads)
        responses = grequests.map(rs)
        now = time.strftime("%m_%d_%y_%H")
        folder = "craigslist"+now
        if not os.path.exists(folder):
            os.mkdir(folder)
        os.chdir(folder)
        if not os.path.exists("ads"):
            os.mkdir("ads")
        os.chdir("ads")
        for r in responses:
            if '<span id="has_been_removed"></span>' in r.text:
                continue
            self.save(r)
            df = df.append(self.parse(r),ignore_index=True)
        
        os.chdir("../")
        df.to_csv("craigslist_data.csv")
        
        
